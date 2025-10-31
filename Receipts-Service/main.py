import os
import sys
from flask import Flask
from flask_migrate import Migrate
from models.receipts import Receipts
from dotenv import load_dotenv
from db import db
from rabbitmq_consumer import start_consumer_loop

app = Flask(__name__)

load_dotenv(dotenv_path=".environment/postgres/.env.postgres")
load_dotenv(dotenv_path=".environment/flask/.env.flask", override=True)
load_dotenv(dotenv_path=".environment/rabbitmq/.env.rabbitmq", override=True) 

db_url = os.getenv("DB_URL")
if not db_url:
    raise ValueError("DB_URL not found in environment variables.")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

from routes import *

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'consumer':
        with app.app_context():
            try:
                db.create_all() 
                print(" [DB] Tabelas verificadas/criadas.")
            except Exception as e:
                print(f" [DB] Erro ao criar tabelas: {e}")

        print("--- INICIANDO RABBITMQ CONSUMER ---")
        start_consumer_loop(app=app) 

    else:
        debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
        port = int(os.getenv("FLASK_PORT", 3000))
        host = os.getenv("FLASK_HOST", "0.0.0.0")

        print("--- INICIANDO FLASK WEB SERVER ---")
        app.run(debug=debug, port=port, host=host)