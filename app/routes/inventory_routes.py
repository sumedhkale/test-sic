from flask import Blueprint, jsonify, request, make_response
from app import RestError, db
from app.dao.inventory_dao import inventory_dao
from app.models import *

# Blueprint Configuration
inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='templates',
    # static_folder='static',
    url_prefix='/inventory'
)


@inventory_bp.route('/')
def index():
    return "In inventory bp "


@inventory_bp.route('/create', methods=['POST'])
def create_inventory():
    try:
        inventory_obj = inventory_dao.create(**request.get_json())
        return make_response(jsonify({
            "inventory_id": inventory_obj.id
        }), 202)
    except Exception as f:
        raise RestError(err_message='Unable to create inventory. Error : %r' % f)


@inventory_bp.route('/<int:inventory_id>/update', methods=['POST'])
def update_inventory(inventory_id):
    try:
        inv_obj = inventory_dao.get_by_id(inventory_id)
        if inv_obj.inventory_state == InventoryState.INACTIVE:
            raise Exception("Error in finding inventory item")

        inventory_obj = inventory_dao.update_by_id(inventory_id, **request.get_json())
        return make_response(jsonify({
            "inventory_id": inventory_obj.id
        }), 202)
    except Exception as f:
        raise RestError(err_message=f'Unable to update inventory with id = {inventory_id}. Reason: %r' % str(f))


@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
def get_by_id(inventory_id):
    try:
        inventory_obj = inventory_dao.get_by_id(inventory_id)
        if not inventory_obj:
            raise Exception("Error in finding inventory item")
        return jsonify(inventory_obj.as_dict())
    except Exception as f:
        raise RestError(err_message=f'Unable to get inventory with id = {inventory_id}. Reason: %r' % str(f))


@inventory_bp.route('/<int:inventory_id>/delete', methods=['POST'])
def delete_inventory(inventory_id):
    try:
        inv_obj = inventory_dao.get_by_id(inventory_id)

        if (not inv_obj) or (inv_obj.inventory_state == InventoryState.INACTIVE):
            raise Exception("Error in finding inventory item")

        request_dict = request.get_json()
        request_dict['inventory_state'] = InventoryState.INACTIVE
        request_dict['last_deletion_time'] = db.func.now()

        inventory_obj = inventory_dao.update_by_id(inventory_id, **request_dict)

        return make_response(jsonify({
            "inventory_id": inventory_obj.id
        }), 202)
    except Exception as f:
        raise RestError(err_message=f'Unable to delete inventory with id = {inventory_id}. Reason: %r' % str(f))


@inventory_bp.route('/<int:inventory_id>/undelete', methods=['POST'])
def undelete_inventory(inventory_id):
    try:
        inv_obj = inventory_dao.get_by_id(inventory_id)
        if not inv_obj or inv_obj.inventory_state == InventoryState.ACTIVE:
            raise Exception("Error in finding inventory item")

        request_dict = request.get_json()
        request_dict['inventory_state'] = InventoryState.ACTIVE
        request_dict['last_deletion_comment'] = None
        request_dict['last_deletion_time'] = None
        request_dict['last_undeleted_time'] = db.func.now()

        inventory_obj = inventory_dao.update_by_id(inventory_id, **request_dict)

        return make_response(jsonify({
            "inventory_id": inventory_obj.id
        }), 202)
    except Exception as f:
        raise RestError(err_message=f'Unable to recover inventory with id = {inventory_id}. Reason: %r' % str(f))


@inventory_bp.route('/all', methods=['GET'])
def get_all_inventory():
    try:
        print(request.args.to_dict())
        if request.args.to_dict():
            video_list = inventory_dao.get_all_filtered(**request.args.to_dict())
        else:
            video_list = inventory_dao.get_all()
        resp = []
        for video in video_list:
            resp.append(video.as_dict())
        return jsonify(resp)
    except Exception as f:
        raise RestError(err_message='Unable to get inventory. Reason: %r' % f)
