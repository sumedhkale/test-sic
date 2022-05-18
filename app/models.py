from app import db
import enum


class BaseModel:
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class InventoryState(enum.IntEnum):
    ACTIVE = 1
    INACTIVE = 2


class Inventory(db.Model, BaseModel):
    """inventory  model."""
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    display_name = db.Column(db.String(100), unique=False, nullable=False)
    quantity = db.Column(db.Integer, index=False, nullable=True, default=0)
    inventory_state = db.Column(db.Enum(InventoryState), server_default='ACTIVE')

    last_deletion_comment = db.Column(db.String(200), nullable=True)
    last_deletion_time = db.Column(db.DateTime)
    last_undeleted_time = db.Column(db.DateTime)
    last_inventory_history_id = db.Column(db.Integer, nullable=True)

    created_on = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return "<Video(id='%s', display_name='%s', quantity='%s', inventory_state=%s, last_deletion_comment='%s', " \
               "last_deletion_time='%s', last_undeleted_time='%s', last_inventory_history_id='%s', created_on='%s')>" \
               % (self.id, self.display_name, self.quantity, self.inventory_state, self.last_deletion_comment,
                  self.last_deletion_time, self.last_undeleted_time, self.last_inventory_history_id, self.created_on)
