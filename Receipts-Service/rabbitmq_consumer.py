import pika
import json
import os
import functools 
from dotenv import load_dotenv
from pika.exceptions import AMQPConnectionError, AMQPChannelError
from sqlalchemy.exc import SQLAlchemyError
from pika.adapters.blocking_connection import BlockingConnection
from models.receipts import Receipts 
from db import db 

def receive_event(app, ch, method, properties, body):
    
    print(f"message received: {body.decode()} ")
    
    with app.app_context():
        try:
            data = json.loads(body.decode())
          
            if not all(key in data for key in ['user_id', 'order_id', 'total_amount']):
                raise ValueError("Dados da mensagem incompletos.")

            new_receipt = Receipts(
                user_id=str(data.get('user_id')),
                username=data.get('username'),
                order_id=data.get('order_id'),
                ammount=data.get('total_amount'),  
                items=data.get('items')
            )

            db.session.add(new_receipt)
            db.session.commit()
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f" [✓] Recibo criado e ACK enviado: ID {new_receipt.id}")
            
        except json.JSONDecodeError:
            print(" [!] ERRO: Falha ao decodificar JSON da mensagem. Rejeitando permanentemente.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) 
        
        except (SQLAlchemyError, ValueError) as e:
            print(f" [!] ERRO CRÍTICO no DB/Dados: {e}. Revertendo e Re-enfileirando.")
            db.session.rollback()
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        except Exception as e:
            print(f" [!] ERRO INESPERADO: {e}. Re-enfileirando.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_consumer_loop(app):
    QUEUE_REQUEST = os.getenv("QUEUE_REQUEST")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    
    if not QUEUE_REQUEST or not RABBITMQ_HOST:
        print(" [!] Configurações do RabbitMQ ausentes (QUEUE_REQUEST ou RABBITMQ_HOST). Verifique seu .env.")
        return

    try:
        connection = BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_REQUEST, durable=True)
    
        on_message_callback_final = functools.partial(receive_event, app) 

        channel.basic_consume(
            queue=QUEUE_REQUEST,
            on_message_callback=on_message_callback_final,
            auto_ack=False
        )
        
        print(f' [*] Conectado ao RabbitMQ em {RABBITMQ_HOST}. Aguardando eventos na fila "{QUEUE_REQUEST}".')
        channel.start_consuming()

    except AMQPConnectionError as e:
        print(f" [X] ERRO: Não foi possível conectar ao RabbitMQ no host {RABBITMQ_HOST}. Verifique se o Orders-service está rodando. Erro: {e}")
    except AMQPChannelError as e:
        print(f" [X] ERRO: Problema no canal AMQP: {e}")
    except KeyboardInterrupt:
        print(" [!] Consumidor encerrado.")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()