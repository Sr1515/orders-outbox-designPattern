from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.environment', '.env.relay')) 

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
QUEUE_REQUEST = os.getenv("QUEUE_REQUEST")
QUEUE_RESPONSE = os.getenv("QUEUE_RESPONSE")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 5))
DB_URL = os.getenv("DB_URL")

