-- ==============================================================================
-- Query 2: Price Anchoring & The Discount Framing Heuristic
-- Psychological Concept: Anchoring & Decoy Pricing
-- Question: Does a higher original anchor price drive higher sales volume
--           even when the actual final price paid is higher?
-- ==============================================================================

WITH discount_brackets AS (
    SELECT 
        discount_tier,
        COUNT(*) AS total_products,
        ROUND(AVG(actual_price_usd), 2) AS avg_anchor_price_usd,
        ROUND(AVG(discounted_price_usd), 2) AS avg_realized_price_usd,
        ROUND(AVG(actual_price_usd - discounted_price_usd), 2) AS avg_perceived_dollar_savings,
        ROUND(AVG(discount_pct), 1) AS avg_discount_pct,
        ROUND(AVG(est_monthly_units_sold), 0) AS avg_monthly_units_sold,
        ROUND(SUM(est_monthly_revenue_usd), 2) AS total_revenue_usd
    FROM products
    GROUP BY discount_tier
)
SELECT 
    discount_tier,
    total_products,
    avg_anchor_price_usd,
    avg_realized_price_usd,
    avg_perceived_dollar_savings,
    avg_discount_pct,
    avg_monthly_units_sold,
    total_revenue_usd,
    ROUND(total_revenue_usd * 100.0 / SUM(total_revenue_usd) OVER (), 2) AS revenue_share_pct
FROM discount_brackets
ORDER BY avg_discount_pct DESC;
