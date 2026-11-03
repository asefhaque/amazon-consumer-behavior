# Amazon Consumer Behavior: SQL Analytics & Behavioral Economics

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tableau](https://img.shields.io/badge/Tableau-Packaged_Workbook_(.twbx)-E97627?logo=tableau&logoColor=white)](tableau/Amazon_Consumer_Behavior_Executive_Dashboard.twbx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An empirical SQL and behavioral analytics project examining how e-commerce consumers react to **ratings thresholds**, **badges (Amazon's Choice / Best Seller)**, **price anchoring**, and **discount framing** across 1,350+ real products. 

All queries are structured for compatibility across **PostgreSQL**, **MySQL**, and **SQLite**, utilizing common table expressions (CTEs), window functions, and multi-tier aggregation.

Developed by **Asef Haque** (MSBA candidate, Brandeis University | BA Psychology, Temple University), bridging cognitive heuristics with relational database querying and Tableau visualization.

---

### ⚡ Executive Summary (15-Second Overview)

| Behavioral Question | Empirical SQL Finding | Psychological Mechanism |
| :--- | :--- | :--- |
| **The "Rating Cliff"** | Over **85% of total revenue** concentrates in products with ratings $\ge 4.0$. Items below 3.5 experience a 70%+ collapse in sales volume. | **Social Proof & Heuristic Filtering:** Shoppers use the 4.0-star rating as a quick cognitive shortcut to filter out perceived risk. |
| **Badge Endorsement Lift** | Products tagged **"Best Seller"** exhibit a **+682% lift in sales velocity**, while **"Amazon's Choice"** drives a **+295% lift** over standard listings. | **Authority Bias & Choice Reduction:** Badges reduce decision fatigue by functioning as an implicit platform seal of approval. |
| **Price Anchoring & Framing** | High stated anchor prices (strikethrough list prices) significantly inflate perceived consumer savings, sustaining volume even on premium goods. | **Anchoring & Adjustment:** The first price observed acts as a cognitive anchor, making the discounted price feel like an earned windfall. |
| **Category Price Sensitivity** | Tech products carry higher average discount depths (~51%) than household goods, showing heavy promotional reliance. | **Mental Accounting:** Consumers demand steeper percentage discounts for high-consideration purchases. |

---

## 📊 Tableau BI Visual Worksheets

> Individual visual worksheets built in **Tableau Desktop** modeling the SQL aggregations from PostgreSQL and SQLite.
> **Packaged Workbook (.twbx):** [`tableau/Amazon_Consumer_Behavior_Executive_Dashboard.twbx`](tableau/Amazon_Consumer_Behavior_Executive_Dashboard.twbx)

### 1. The 4.0-Star "Rating Cliff" (Social Proof & Trust Threshold)

<img src="assets/01_rating_cliff.png?v=3" width="750"/>

**Key Takeaways:**
- **The 4.0 Trust Boundary:** Products rated 4.0–4.4 stars achieve the highest average sales velocity (~3,279 units/month) and drive nearly 90% of total catalog revenue.
- **The Rating Cliff:** Once a product drops below 4.0 stars (3.5–3.9), monthly unit velocity plummets by **67.6%** to 1,063 units. Below 3.5 stars, velocity falls to just 477 units.
- **Consumer Behavior Insight:** Shoppers use the 4.0-star rating as a non-negotiable mental heuristic to filter out perceived risk. Heavy price markdowns cannot compensate for poor star ratings.

---

### 2. Choice Architecture: Demand Lift from Amazon Badges

<img src="assets/03_badge_endorsement_lift.png?v=3" width="750"/>

**Key Takeaways:**
- **Best Seller Dominance:** Products with the **Best Seller** badge average 13,355 units/month—a **+682.4% velocity lift** over unbadged listings (1,707 units/month).
- **Amazon's Choice Lift:** The **Amazon's Choice** badge drives an average of 6,747 units/month (**+295.3% lift**), while also sustaining a 19.3% price premium over standard listings ($47.01 vs. $39.40).
- **Cognitive Takeaway:** Algorithmic endorsements reduce decision fatigue in crowded categories, acting as an implicit seal of approval that steers consumer choice.

---

### 3. Price Anchoring: Stated List Price vs. Realized Transaction Price

<img src="assets/02_price_anchoring.png?v=3" width="750"/>

**Key Takeaways:**
- **Anchoring Mechanics:** Products in the **Moderate Discount (20–39% off)** tier carry the highest anchor list price ($114.09) and realized sale price ($79.87), generating an average perceived savings of $34.22 while driving over 53% of catalog revenue.
- **Diminishing Returns on Deep Discounts:** Products with **Extreme Discounts (60%+ off)** have an average realized price of only $11.05 and do not generate higher volume (2,600 units/mo) than moderate discounts (3,094 units/mo).
- **Merchandising Takeaway:** A high initial list price creates a stronger perceived value proposition than a rock-bottom dollar price.

---

### 4. Category Dynamics & Promotional Depth

<img src="assets/04_category_discount_depth.png?v=3" width="750"/>

**Key Takeaways:**
- **High-Consideration Goods:** **Electronics & Tech** items carry the highest average promotional discount (51.3%), reflecting intense competition and consumer expectation for markdowns.
- **Low-Consideration Necessities:** **Office & Productivity** items require much shallower discounts (12.4%), demonstrating steady, inelastic demand where utility precedes price sensitivity.

---

## 🧮 Core SQL Queries & Methodology

The database runs on **SQLite** (`data/amazon_consumer_behavior.db`) with clean tables and indexing.

### Query 1: Social Proof Thresholds & Rating Cliff
```sql
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
    avg_monthly_units_sold,
    total_monthly_revenue_usd,
    ROUND(total_monthly_revenue_usd * 100.0 / SUM(total_monthly_revenue_usd) OVER (), 2) AS pct_total_revenue
FROM rating_summary
ORDER BY avg_rating DESC;
```

### Query 2: Badge Premium & Relative Demand Lift
```sql
WITH badge_metrics AS (
    SELECT 
        badge_type,
        COUNT(*) AS catalog_count,
        ROUND(AVG(rating), 2) AS mean_rating,
        ROUND(AVG(discounted_price_usd), 2) AS avg_price_usd,
        ROUND(AVG(est_monthly_units_sold), 0) AS avg_sales_velocity
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
    b.avg_price_usd,
    ROUND((b.avg_price_usd - base.standard_price) * 100.0 / base.standard_price, 1) AS price_premium_pct,
    b.avg_sales_velocity,
    ROUND((b.avg_sales_velocity - base.standard_velocity) * 100.0 / base.standard_velocity, 1) AS velocity_lift_pct
FROM badge_metrics b
CROSS JOIN baseline base
ORDER BY b.avg_sales_velocity DESC;
```

---

## 📁 Repository Structure

```
Amazon_Consumer_Behavior_SQL/
├── data/
│   ├── amazon_consumer_behavior.db  # SQLite relational database
│   ├── amazon_clean.csv             # Cleaned analytical dataset
│   └── amazon_raw.csv               # Raw Amazon sales source dataset
├── queries/                         # Production SQL scripts
│   ├── 01_social_proof_and_rating_thresholds.sql
│   ├── 02_price_anchoring_and_discounts.sql
│   ├── 03_badge_premiums_and_elasticity.sql
│   └── 04_category_price_sensitivity.sql
├── tableau/                         # Tableau Desktop models
│   ├── Amazon_Consumer_Behavior_Executive_Dashboard.twbx  # Packaged Tableau workbook
│   ├── Amazon_Consumer_Behavior_Executive_Dashboard.twb   # XML workbook
│   └── make_tableau_workbook.py                           # Automated workbook builder
├── assets/                          # Tableau visual worksheets
│   ├── 01_rating_cliff.png
│   ├── 02_price_anchoring.png
│   ├── 03_badge_endorsement_lift.png
│   └── 04_category_discount_depth.png
├── build_database.py                # Pipeline downloading, cleaning & building SQLite DB
├── run_analysis.py                  # Executes SQL queries and saves chart visualizations
└── README.md                        # Documentation and visual summary
```

---

## 👨‍💻 Author

**Asef Haque**  
- MS in Business Analytics candidate | Brandeis University International Business School  
- BA in Psychology (Cognitive & Behavioral) | Temple University  
- Contact: asefhaque@brandeis.edu | [LinkedIn](https://www.linkedin.com/in/asefhaque/) | [GitHub](https://github.com/asefhaque)
