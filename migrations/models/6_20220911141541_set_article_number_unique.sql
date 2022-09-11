-- upgrade --
CREATE UNIQUE INDEX "uid_product_article_a687b8" ON "product" ("article_number");
-- downgrade --
DROP INDEX "idx_product_article_a687b8";
