from app.models import *


class BaseDAO:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return db.session.query(self.model).all()

    def get_all_filtered(self, **kwargs):
        return self.model.query.filter_by(**kwargs).all()

    def create(self, **kwargs):
        try:
            obj = self.model(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as f:
            raise

    def update_by_id(self, obj_id, **kwargs):
        try:
            obj = self.model.query.filter_by(id=obj_id).one_or_none()
            if not obj:
                raise Exception("Cannot find obj to update. Please create obj first")

            video_columns = self.model.__table__.columns.keys()
            for prop_key, prop_value in kwargs.items():
                setattr(obj, prop_key, prop_value)

            db.session.commit()
            return obj

        except Exception as f:
            raise

    def delete_all(self):
        try:
            num_rows_deleted = db.session.query(self.model).delete()
            db.session.commit()
        except:
            db.session.rollback()

    def delete_by_id(self, obj_id):
        try:
            self.model.query.filter_by(id=obj_id).delete()
            db.session.commit()
        except Exception as f:
            raise

    def get_by_id(self, obj_id):
        return db.session.query(self.model).filter_by(id=obj_id).first()


class InventoryDAO(BaseDAO):

    def __init__(self, model):
        super().__init__(model)

    def get_all(self):
        return self.get_all_filtered(inventory_state='ACTIVE')

inventory_dao = InventoryDAO(Inventory)
