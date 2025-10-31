from sqlalchemy.dialects.postgresql import UUID, NUMERIC, JSONB, TEXT
from sqlalchemy import func
from db import db

class Receipts(db.Model):
    __tablename__ = 'receipts'
    
    id = db.Column(
        UUID(as_uuid=True), 
        primary_key=True,
        default =func.uuid_generate_v4()
    )
    
    username = db.Column(TEXT)
    
    # change for uuid after
    user_id = db.Column(db.Integer)
    
    order_id = db.Column(
        UUID(as_uuid=True),
    )
    
    ammount = db.Column(NUMERIC(10, 2))
    items = db.Column(JSONB)
    
    def as_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "order_id": str(self.order_id),
            "ammount": self.order_id,
            "items": self.items
        }
    