import uuid
from .db import db

class Item(db.Model):
    __tablename__ = 'inventory_table'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    last_updated_dt = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Item {self.name}>"