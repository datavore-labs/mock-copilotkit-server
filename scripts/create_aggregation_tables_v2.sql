-- ============================================================================
-- Enhanced BigQuery Aggregation Script for Mock Data Generation
-- Generates summary tables that match MockDataClient output format
-- Idempotent script - safe to run multiple times
-- ============================================================================

-- ============================================================================
-- Cleanup: Drop existing tables if they exist
-- ============================================================================
DROP TABLE IF EXISTS `audience-builder-tintash.retail_transactions_enhanced.brand_performance_by_category_20250724`;
DROP TABLE IF EXISTS `audience-builder-tintash.retail_transactions_enhanced.spending_distribution_20250724`;
DROP TABLE IF EXISTS `audience-builder-tintash.retail_transactions_enhanced.purchase_recency_20250724`;
DROP TABLE IF EXISTS `audience-builder-tintash.retail_transactions_enhanced.category_summary_20250724`;

-- ============================================================================
-- Table 1: Brand Performance by Category (for get_brand_data)
-- ============================================================================
CREATE TABLE `audience-builder-tintash.retail_transactions_enhanced.brand_performance_by_category_20250724`
(
  category STRING,
  brand STRING,
  total_records INT64,
  total_quantity INT64,
  total_receipts INT64,
  total_price FLOAT64,
  category_percentage FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY category, brand
OPTIONS(
  description="Brand performance metrics by category for frontend integration"
);

-- Populate brand performance table
INSERT INTO `audience-builder-tintash.retail_transactions_enhanced.brand_performance_by_category_20250724` (
  category,
  brand,
  total_records,
  total_quantity,
  total_receipts,
  total_price,
  category_percentage,
  created_at
)
WITH category_totals AS (
  SELECT
    LOWER(COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY)) as category,
    SUM(NUM_RECORDS) as category_total_records
  FROM `audience-builder-tintash.retail_transactions_enhanced.ibotta_enhanced_20250724`
  WHERE COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY) IS NOT NULL
    AND COALESCE(AD_BRAND_NAME, BRAND_NAME) IS NOT NULL
  GROUP BY LOWER(COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY))
),
brand_metrics AS (
  SELECT
    LOWER(COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY)) as category,
    COALESCE(AD_BRAND_NAME, BRAND_NAME) as brand,
    SUM(NUM_RECORDS) as total_records,
    SUM(SUM_QUANTITY) as total_quantity,
    SUM(NUM_RECEIPT_IDS) as total_receipts,
    SUM(SUM_PRICE) as total_price
  FROM `audience-builder-tintash.retail_transactions_enhanced.ibotta_enhanced_20250724`
  WHERE COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY) IS NOT NULL
    AND COALESCE(AD_BRAND_NAME, BRAND_NAME) IS NOT NULL
  GROUP BY
    LOWER(COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY)),
    COALESCE(AD_BRAND_NAME, BRAND_NAME)
)
SELECT
  bm.category,
  bm.brand,
  bm.total_records,
  bm.total_quantity,
  bm.total_receipts,
  bm.total_price,
  ROUND(SAFE_DIVIDE(bm.total_records, ct.category_total_records) * 100, 1) as category_percentage,
  CURRENT_TIMESTAMP() as created_at
FROM brand_metrics bm
JOIN category_totals ct ON bm.category = ct.category
WHERE bm.total_records >= 1000  -- Filter for meaningful data
ORDER BY bm.category, bm.total_records DESC;


-- ============================================================================
-- Table 2: Spending Distribution by Category (for get_spending_data)
-- ============================================================================
CREATE TABLE `audience-builder-tintash.retail_transactions_enhanced.spending_distribution_20250724`
(
  category STRING,
  spending_range STRING,
  total_records INT64,
  total_receipts INT64,
  category_percentage FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY category
OPTIONS(
  description="Spending distribution by category and price ranges"
);

-- Populate spending distribution table
INSERT INTO `audience-builder-tintash.retail_transactions_enhanced.spending_distribution_20250724` (
  category,
  spending_range,
  total_records,
  total_receipts,
  category_percentage,
  created_at
)
WITH spending_buckets AS (
  SELECT
    LOWER(COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY)) as category,
    CASE
      WHEN SAFE_DIVIDE(SUM_PRICE, SUM_QUANTITY) <= 10 THEN '$0-10'
      WHEN SAFE_DIVIDE(SUM_PRICE, SUM_QUANTITY) <= 25 THEN '$10-25'
      WHEN SAFE_DIVIDE(SUM_PRICE, SUM_QUANTITY) <= 50 THEN '$25-50'
      ELSE '$50+'
    END as spending_range,
    NUM_RECORDS,
    NUM_RECEIPT_IDS
  FROM `audience-builder-tintash.retail_transactions_enhanced.ibotta_enhanced_20250724`
  WHERE COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY) IS NOT NULL
    AND SUM_PRICE IS NOT NULL
    AND SUM_QUANTITY IS NOT NULL
    AND SUM_PRICE > 0
    AND SUM_QUANTITY > 0
),
category_totals AS (
  SELECT
    category,
    SUM(NUM_RECORDS) as category_total_records
  FROM spending_buckets
  GROUP BY category
),
range_aggregates AS (
  SELECT
    category,
    spending_range,
    SUM(NUM_RECORDS) as total_records,
    SUM(NUM_RECEIPT_IDS) as total_receipts
  FROM spending_buckets
  GROUP BY category, spending_range
)
SELECT
  ra.category,
  ra.spending_range,
  ra.total_records,
  ra.total_receipts,
  ROUND(SAFE_DIVIDE(ra.total_records, ct.category_total_records) * 100, 1) as category_percentage,
  CURRENT_TIMESTAMP() as created_at
FROM range_aggregates ra
JOIN category_totals ct ON ra.category = ct.category
WHERE ra.total_records >= 100  -- Filter for meaningful data
ORDER BY ra.category,
  CASE ra.spending_range
    WHEN '$0-10' THEN 1
    WHEN '$10-25' THEN 2
    WHEN '$25-50' THEN 3
    WHEN '$50+' THEN 4
  END;


-- ============================================================================
-- Table 3: Purchase Recency Analysis (for get_purchase_recency_data)
-- ============================================================================
CREATE TABLE `audience-builder-tintash.retail_transactions_enhanced.purchase_recency_20250724`
(
  category STRING,
  recency_period STRING,
  total_records INT64,
  total_receipts INT64,
  category_percentage FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY category
OPTIONS(
  description="Purchase recency analysis by category"
);

-- Populate purchase recency table
INSERT INTO `audience-builder-tintash.retail_transactions_enhanced.purchase_recency_20250724` (
  category,
  recency_period,
  total_records,
  total_receipts,
  category_percentage,
  created_at
)
WITH recency_analysis AS (
  SELECT
    LOWER(COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY)) as category,
    CASE
      WHEN DATE_DIFF(CURRENT_DATE(), MAX_PURCHASE_DATE, DAY) <= 30 THEN '0-30 Days'
      WHEN DATE_DIFF(CURRENT_DATE(), MAX_PURCHASE_DATE, DAY) <= 60 THEN '30-60 Days'
      WHEN DATE_DIFF(CURRENT_DATE(), MAX_PURCHASE_DATE, DAY) <= 90 THEN '60-90 Days'
      WHEN DATE_DIFF(CURRENT_DATE(), MAX_PURCHASE_DATE, DAY) <= 180 THEN '90-180 Days'
      ELSE '180+ Days'
    END as recency_period,
    NUM_RECORDS,
    NUM_RECEIPT_IDS
  FROM `audience-builder-tintash.retail_transactions_enhanced.ibotta_enhanced_20250724`
  WHERE COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY) IS NOT NULL
    AND MAX_PURCHASE_DATE IS NOT NULL
),
category_totals AS (
  SELECT
    category,
    SUM(NUM_RECORDS) as category_total_records
  FROM recency_analysis
  GROUP BY category
),
period_aggregates AS (
  SELECT
    category,
    recency_period,
    SUM(NUM_RECORDS) as total_records,
    SUM(NUM_RECEIPT_IDS) as total_receipts
  FROM recency_analysis
  GROUP BY category, recency_period
)
SELECT
  pa.category,
  pa.recency_period,
  pa.total_records,
  pa.total_receipts,
  ROUND(SAFE_DIVIDE(pa.total_records, ct.category_total_records) * 100, 1) as category_percentage,
  CURRENT_TIMESTAMP() as created_at
FROM period_aggregates pa
JOIN category_totals ct ON pa.category = ct.category
WHERE pa.total_records >= 100  -- Filter for meaningful data
ORDER BY pa.category,
  CASE pa.recency_period
    WHEN '0-30 Days' THEN 1
    WHEN '30-60 Days' THEN 2
    WHEN '60-90 Days' THEN 3
    WHEN '90-180 Days' THEN 4
    WHEN '180+ Days' THEN 5
  END;

-- ============================================================================
-- Table 4: Category Summary (Overall category performance)
-- ============================================================================
CREATE TABLE `audience-builder-tintash.retail_transactions_enhanced.category_summary_20250724`
(
  category STRING,
  total_records INT64,
  total_receipts INT64,
  total_quantity INT64,
  total_price FLOAT64,
  unique_brands INT64,
  unique_products INT64,
  avg_price_per_item FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY category
OPTIONS(
  description="Overall category performance summary"
);

-- Populate category summary table
INSERT INTO `audience-builder-tintash.retail_transactions_enhanced.category_summary_20250724` (
  category,
  total_records,
  total_receipts,
  total_quantity,
  total_price,
  unique_brands,
  unique_products,
  avg_price_per_item,
  created_at
)
SELECT
  LOWER(COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY)) as category,
  SUM(NUM_RECORDS) as total_records,
  SUM(NUM_RECEIPT_IDS) as total_receipts,
  SUM(SUM_QUANTITY) as total_quantity,
  SUM(SUM_PRICE) as total_price,
  COUNT(DISTINCT COALESCE(AD_BRAND_NAME, BRAND_NAME)) as unique_brands,
  COUNT(DISTINCT COALESCE(AD_PRODUCT_NAME, PRODUCT_NAME)) as unique_products,
  ROUND(SAFE_DIVIDE(SUM(SUM_PRICE), SUM(SUM_QUANTITY)), 2) as avg_price_per_item,
  CURRENT_TIMESTAMP() as created_at
FROM `audience-builder-tintash.retail_transactions_enhanced.ibotta_enhanced_20250724`
WHERE COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY) IS NOT NULL
GROUP BY LOWER(COALESCE(AD_CATEGORY_COMBINED, PRIMARY_CATEGORY))
HAVING SUM(NUM_RECORDS) >= 1000  -- Filter for meaningful categories
ORDER BY total_records DESC;

-- ============================================================================
-- Query Examples for Frontend Integration
-- ============================================================================

-- Example 1: Get brand data for cookies category (matches get_brand_data format)
/*
SELECT
  brand,
  total_records as count,
  category_percentage as percentage
FROM `audience-builder-tintash.retail_transactions_enhanced.brand_performance_by_category_20250724`
WHERE category = 'cookies'
ORDER BY total_records DESC
LIMIT 10;
*/

-- Example 2: Get spending data for beer category (matches get_spending_data format)
/*
SELECT
  spending_range as range,
  total_records as count,
  category_percentage as percentage
FROM `audience-builder-tintash.retail_transactions_enhanced.spending_distribution_20250724`
WHERE category = 'beer'
ORDER BY
  CASE spending_range
    WHEN '$0-10' THEN 1
    WHEN '$10-25' THEN 2
    WHEN '$25-50' THEN 3
    WHEN '$50+' THEN 4
  END;
*/

-- Example 3: Get purchase recency data (matches get_purchase_recency_data format)
/*
SELECT
  recency_period as period,
  total_records as count,
  category_percentage as percentage
FROM `audience-builder-tintash.retail_transactions_enhanced.purchase_recency_20250724`
WHERE category = 'cosmetics'
ORDER BY
  CASE recency_period
    WHEN '0-30 Days' THEN 1
    WHEN '30-60 Days' THEN 2
    WHEN '60-90 Days' THEN 3
    WHEN '90-180 Days' THEN 4
    WHEN '180+ Days' THEN 5
  END;
*/
