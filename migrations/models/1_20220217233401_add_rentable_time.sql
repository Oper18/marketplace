-- upgrade --
ALTER TABLE "productitems" ADD "rent_time_stop" DATE;
ALTER TABLE "productitems" ADD "rent_time_start" DATE;
-- downgrade --
ALTER TABLE "productitems" DROP COLUMN "rent_time_stop";
ALTER TABLE "productitems" DROP COLUMN "rent_time_start";
