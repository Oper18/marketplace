-- upgrade --
ALTER TABLE "productitems" ALTER COLUMN "rent_time_start" TYPE TIMESTAMPTZ USING "rent_time_start"::TIMESTAMPTZ;
ALTER TABLE "productitems" ALTER COLUMN "rent_time_stop" TYPE TIMESTAMPTZ USING "rent_time_stop"::TIMESTAMPTZ;
-- downgrade --
ALTER TABLE "productitems" ALTER COLUMN "rent_time_start" TYPE DATE USING "rent_time_start"::DATE;
ALTER TABLE "productitems" ALTER COLUMN "rent_time_stop" TYPE DATE USING "rent_time_stop"::DATE;
