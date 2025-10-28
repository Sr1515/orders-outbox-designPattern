from sqlalchemy import create_engine, Column, Boolean, JSON, select, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, Session
from config import DB_URL
import uuid

Base = declarative_base()
engine = create_engine(DB_URL)

class OutboxEvent(Base):
    __tablename__ = "outbox_outboxevent"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    processed = Column(Boolean, default=False)
    body = Column(JSON)
    
def get_unprocessed_events(session):
    stmt = select(OutboxEvent).where(OutboxEvent.processed == False)
    return session.scalars(stmt).all()

def mark_event_processed(session, event_id):
    stmt = update(OutboxEvent).where(OutboxEvent.id == event_id).values(processed=True)
    session.execute(stmt)
    session.commit()