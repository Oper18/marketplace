-- upgrade --
ALTER TABLE "productitems" ADD "salesman" INT;
-- downgrade --
ALTER TABLE "productitems" DROP COLUMN "salesman";
