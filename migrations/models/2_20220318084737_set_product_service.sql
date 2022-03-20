-- upgrade --
ALTER TABLE "product" ADD "service" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "product" DROP COLUMN "service";
