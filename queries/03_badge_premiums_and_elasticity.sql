-- ==============================================================================
-- Query 3: Badge Heuristics & The Price Premium of Endorsement
-- Psychological Concept: Authority Heuristic & Choice Reduction
-- Question: Does an "Amazon's Choice" or "Best Seller" badge command
--           both higher sales velocity and higher average selling prices?
-- ==============================================================================

WITH badge_metrics AS (
    SELECT 
        badge_type,
        COUNT(*) AS catalog_count,
        ROUND(AVG(rating), 2) AS mean_rating,
        ROUND(AVG(review_count), 0) AS mean_reviews,
        ROUND(AVG(discounted_price_usd), 2) AS avg_price_usd,
        ROUND(AVG(est_monthly_units_sold), 0) AS avg_sales_velocity,
        ROUND(SUM(est_monthly_revenue_usd), 2) AS monthly_revenue
    FROM products
    GROUP BY badge_type
),
baseline AS (
    SELECT avg_price_usd AS standard_price, avg_sales_velocity AS standard_velocity
    FROM badge_metrics
    WHERE badge_type = 'Standard'
)
SELECT 
    b.badge_type,
    b.catalog_count,
    ROUND(b.catalog_count * 100.0 / (SELECT SUM(catalog_count) FROM badge_metrics), 1) AS pct_of_catalog,
    b.mean_rating,
    b.mean_reviews,
    b.avg_price_usd,
    ROUND((b.avg_price_usd - base.standard_price) * 100.0 / base.standard_price, 1) AS price_premium_pct,
    b.avg_sales_velocity,
    ROUND((b.avg_sales_velocity - base.standard_velocity) * 100.0 / base.standard_velocity, 1) AS velocity_lift_pct,
    b.monthly_revenue
FROM badge_metrics b
CROSS JOIN baseline base
ORDER BY b.avg_sales_velocity DESC;
