import json
import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError, NackError, UnroutableError
from sqlalchemy.exc import SQLAlchemyError
from pika.adapters.blocking_connection import BlockingConnection
from config import RABBITMQ_HOST, QUEUE_REQUEST
from db import Session, engine, get_unprocessed_events, mark_event_processed, OutboxEvent

def setup_channel(connection: BlockingConnection):
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_REQUEST, durable=True)
    channel.confirm_delivery()
    return channel

def send_to_queue_and_confirm(channel, event: OutboxEvent):
    properties = pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        message_id=str(event.id)
    )
    message = json.dumps(event.body)
    try:
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_REQUEST,
            body=message,
            properties=properties,
            mandatory=True
        )
        print(f"✅ Sent OutboxEvent {event.id} successfully.")
        return True
    except NackError:
        print(f"⚠️  Message for event {event.id} was NACKed by broker.")
        raise
    except UnroutableError:
        print(f"⚠️  Message for event {event.id} was unroutable (no queue).")
        raise
    except Exception as e:
        print(f"❌ Publish failed for event {event.id}: {e}")
        raise

def process_outbox_events_with_connection(connection: BlockingConnection):
    try:
        channel = setup_channel(connection)
    except (AMQPChannelError, AMQPConnectionError) as e:
        print(f"CRITICAL: Falha ao configurar canal na conexão ativa. {e}")
        raise
    with Session(engine) as session:
        try:
            events = get_unprocessed_events(session)
        except SQLAlchemyError as e:
            print(f"CRITICAL: Erro ao buscar eventos no banco de dados: {e}")
            return
        if not events:
            print("No unprocessed events found.")
            return
        print(f"Found {len(events)} unprocessed events.")
        for event in events:
            try:
                if send_to_queue_and_confirm(channel, event):
                    mark_event_processed(session, event.id)
                    session.commit()
            except (NackError, UnroutableError) as e:
                print(f"WARNING: RabbitMQ did not confirm event {event.id}: {e}")
                session.rollback()
            except (AMQPChannelError, AMQPConnectionError) as e:
                print(f"CRITICAL: Conexão RabbitMQ quebrada durante envio. {e}")
                raise
            except Exception as e:
                print(f"CRITICAL: Falha no envio/processamento do evento {event.id}: {e}")
                raise
