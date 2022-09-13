-- upgrade --
ALTER TABLE "product" ADD "size" VARCHAR(64);
ALTER TABLE "productitems" DROP COLUMN "size";
ALTER TABLE "productitems" DROP COLUMN "serial_number";
-- downgrade --
ALTER TABLE "product" DROP COLUMN "size";
ALTER TABLE "productitems" ADD "size" VARCHAR(64);
ALTER TABLE "productitems" ADD "serial_number" VARCHAR(256);
