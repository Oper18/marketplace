from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "admin" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(200) NOT NULL,
    "email" VARCHAR(256) NOT NULL UNIQUE,
    "last_login" TIMESTAMPTZ NOT NULL,
    "external_id" INT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "admin"."last_login" IS 'Last Login';
CREATE TABLE IF NOT EXISTS "brandname" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "logo" VARCHAR(64),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "product" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "description" TEXT NOT NULL,
    "color" VARCHAR(64),
    "sex" SMALLINT NOT NULL,
    "age" SMALLINT NOT NULL,
    "article_number" VARCHAR(256)  UNIQUE,
    "size" VARCHAR(64),
    "price" DECIMAL(10,2),
    "currency" VARCHAR(16),
    "discount" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "rent" BOOL NOT NULL  DEFAULT False,
    "service" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "brand_name_id" INT NOT NULL REFERENCES "brandname" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "product"."sex" IS 'male: 1\nfemale: 2\nunisex: 3';
COMMENT ON COLUMN "product"."age" IS 'adult: 1\nchild: 2\ncommon: 3';
CREATE TABLE IF NOT EXISTS "productgallery" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "img" VARCHAR(64) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "productitems" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "sold" BOOL NOT NULL  DEFAULT False,
    "buyer" INT,
    "salesman" INT,
    "rent_time_start" TIMESTAMPTZ,
    "rent_time_stop" TIMESTAMPTZ,
    "payed_amount" DECIMAL(10,2),
    "payment_type" INT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "product_category" (
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
