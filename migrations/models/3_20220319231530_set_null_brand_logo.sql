-- upgrade --
ALTER TABLE "brandname" ALTER COLUMN "logo" DROP NOT NULL;
-- downgrade --
ALTER TABLE "brandname" ALTER COLUMN "logo" SET NOT NULL;
