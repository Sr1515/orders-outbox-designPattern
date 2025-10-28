import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.environment', '.env.django'))

pg_env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.environment', '.env.postgres'))