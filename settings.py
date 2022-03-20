# coding: utf-8

import os

DATABASE = {
    "user": os.environ.get('DB_USER', 'marketplace'),
    "password": os.environ.get('DB_PASSWORD', 'marketplace'),
    "address": os.environ.get('DB_HOST', 'marketplace_db'),
    "name": os.environ.get('DB_NAME', 'marketplace'),
    "port": os.environ.get('DB_PORT', '5432'),
}

DATABASE_CONFIG = {
    "connections": {"default": "postgres://{}:{}@{}:5432/{}".format(
        DATABASE["user"],
        DATABASE["password"],
        DATABASE["address"],
        DATABASE["name"],
    )},
    "apps": {
        "models": {
            "models": ["models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

REDIS = os.environ.get("REDIS_HOST", "marketplace_redis")

LOCAL_SALT = os.getenv('SERVER_SALT', '6d5d1be29a494dc8ad70a766ba07814a')
SERVER_SECRET = os.getenv('SERVER_SECRET', '6d5d1be29a494dc8ad70a766ba07814a')
ACCESS_TOKEN_LIFETIME = 24*60*60
REFRESH_TOKEN_LIFETIME = 24*60*60*60

BASEDIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASEDIR, "static")
os.makedirs(os.path.join(BASEDIR, "static"), exist_ok=True)
STATIC_PATH = "/static"

IMG_DIR = os.path.join(STATIC_DIR, "img")
IMG_PATH = os.path.join(STATIC_PATH, "img")
os.makedirs(os.path.join(STATIC_DIR, "img"), exist_ok=True)
