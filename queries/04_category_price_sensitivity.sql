-- ==============================================================================
-- Query 4: Category Dynamics & Consumer Price Elasticity
-- Psychological Concept: Mental Accounting & Category Framing
-- Question: How do consumer price tolerances and discount dependencies vary
--           across high-consideration tech vs. low-consideration household goods?
-- ==============================================================================

WITH cat_analysis AS (
    SELECT 
        main_category,
        COUNT(*) AS total_items,
        ROUND(AVG(rating), 2) AS category_avg_rating,
        ROUND(AVG(actual_price_usd), 2) AS avg_list_price,
        ROUND(AVG(discounted_price_usd), 2) AS avg_sale_price,
        ROUND(AVG(discount_pct), 1) AS avg_discount_depth,
        ROUND(AVG(est_monthly_units_sold), 0) AS avg_units_sold_per_item,
        ROUND(SUM(est_monthly_revenue_usd), 2) AS category_total_revenue
    FROM products
    GROUP BY main_category
)
SELECT 
    main_category,
    total_items,
    category_avg_rating,
    avg_list_price,
    avg_sale_price,
    avg_discount_depth,
    avg_units_sold_per_item,
    category_total_revenue,
    RANK() OVER (ORDER BY category_total_revenue DESC) AS revenue_rank
FROM cat_analysis
ORDER BY category_total_revenue DESC;
