-- upgrade --
ALTER TABLE "productitems" ALTER COLUMN "payed_amount" TYPE DECIMAL(13,2) USING "payed_amount"::DECIMAL(13,2);
-- downgrade --
ALTER TABLE "productitems" ALTER COLUMN "payed_amount" TYPE INT USING "payed_amount"::INT;
