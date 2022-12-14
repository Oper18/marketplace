-- upgrade --
ALTER TABLE "productitems" ADD "payment_type" INT;
ALTER TABLE "productitems" ADD "payed_amount" INT;
-- downgrade --
ALTER TABLE "productitems" DROP COLUMN "payment_type";
ALTER TABLE "productitems" DROP COLUMN "payed_amount";
