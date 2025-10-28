import time
import sys
import pika
from relay import process_outbox_events_with_connection
from config import POLL_INTERVAL, RABBITMQ_HOST
from pika.exceptions import AMQPConnectionError

def get_new_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        socket_timeout=20,
        heartbeat=60
    ))

def main():
    print("-------------------------------------------------------")
    print(f"Relay Outbox iniciado - verificando a cada {POLL_INTERVAL} segundos.")
    print(f"RabbitMQ Host: {RABBITMQ_HOST}")
    print("-------------------------------------------------------")
    connection = None
    while True:
        try:
            if connection is None or connection.is_closed:
                print("Attempting to connect to RabbitMQ...")
                connection = get_new_connection()
                print("Connection established successfully.")
            process_outbox_events_with_connection(connection)
        except (AMQPConnectionError, Exception) as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERRO CRÍTICO (Conexão Quebrada): {e}", file=sys.stderr)
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass
            connection = None
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nRelay Outbox interrompido pelo usuário.")
        sys.exit(0)
