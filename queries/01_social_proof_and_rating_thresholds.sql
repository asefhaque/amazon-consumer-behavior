-- ==============================================================================
-- Query 1: Social Proof Thresholds & The 4.0-Star "Rating Cliff"
-- Psychological Concept: Social Proof & Threshold Heuristics
-- Question: Do consumers exhibit a sharp drop in demand below the 4.0 star barrier?
-- ==============================================================================

WITH rating_summary AS (
    SELECT 
        rating_tier,
        COUNT(*) AS product_count,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(AVG(review_count), 0) AS avg_reviews_per_product,
        ROUND(AVG(discounted_price_usd), 2) AS avg_selling_price_usd,
        ROUND(AVG(est_monthly_units_sold), 0) AS avg_monthly_units_sold,
        ROUND(SUM(est_monthly_revenue_usd), 2) AS total_monthly_revenue_usd
    FROM products
    GROUP BY rating_tier
)
SELECT 
    rating_tier,
    product_count,
    avg_rating,
    avg_reviews_per_product,
    avg_selling_price_usd,
    avg_monthly_units_sold,
    total_monthly_revenue_usd,
    ROUND(total_monthly_revenue_usd * 100.0 / SUM(total_monthly_revenue_usd) OVER (), 2) AS pct_total_revenue
FROM rating_summary
ORDER BY avg_rating DESC;
