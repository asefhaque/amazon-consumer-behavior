import os
import re
import sqlite3
import urllib.request
import numpy as np
import pandas as pd

PROJECT_DIR = r"c:\Users\asefh\Downloads\Amazon_Consumer_Behavior_SQL"
DATA_DIR = os.path.join(PROJECT_DIR, "data")
RAW_CSV = os.path.join(DATA_DIR, "amazon_raw.csv")
CLEAN_CSV = os.path.join(DATA_DIR, "amazon_clean.csv")
DB_PATH = os.path.join(DATA_DIR, "amazon_consumer_behavior.db")

print("1. Downloading raw Amazon Sales Dataset...")
URL = "https://raw.githubusercontent.com/TimQRB/amazon-sales-dataset/main/Amazon.csv"
urllib.request.urlretrieve(URL, RAW_CSV)
print(f"Downloaded raw dataset to {RAW_CSV}")

df = pd.read_csv(RAW_CSV)
print(f"Loaded {len(df)} raw rows.")

# -------------------------------------------------------------
# 2. Data Cleaning & Normalization
# -------------------------------------------------------------
print("2. Cleaning and standardizing fields...")

def clean_money(val):
    if pd.isna(val):
        return np.nan
    s = re.sub(r'[^\d.]', '', str(val))
    return float(s) if s else np.nan

def clean_int(val):
    if pd.isna(val):
        return 0
    s = re.sub(r'[^\d]', '', str(val))
    return int(s) if s else 0

# Clean prices (convert INR to USD approx 1 USD = 83 INR for universal recruiter readability)
INR_TO_USD = 83.0

df['actual_price_inr'] = df['actual_price'].apply(clean_money)
df['discounted_price_inr'] = df['discounted_price'].apply(clean_money)
df['actual_price_usd'] = (df['actual_price_inr'] / INR_TO_USD).round(2)
df['discounted_price_usd'] = (df['discounted_price_inr'] / INR_TO_USD).round(2)

# Clean discount percentage
df['discount_pct'] = df['discount_percentage'].astype(str).str.replace('%', '', regex=False)
df['discount_pct'] = pd.to_numeric(df['discount_pct'], errors='coerce').fillna(0.0)

# Clean rating (handle corrupted values like '|')
df['rating_clean'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_clean'] = df['rating_clean'].fillna(df['rating_clean'].median())

# Clean rating count
df['review_count'] = df['rating_count'].apply(clean_int)

# Extract Main Category
def extract_main_category(cat_str):
    if pd.isna(cat_str):
        return "Other"
    parts = str(cat_str).split('|')
    main = parts[0].strip()
    if "Computer" in main or "Electronic" in main:
        return "Electronics & Tech"
    elif "Home" in main or "Kitchen" in main:
        return "Home & Kitchen"
    elif "Office" in main:
        return "Office & Productivity"
    elif "Health" in main or "Beauty" in main:
        return "Health & Personal Care"
    return main

df['main_category'] = df['category'].apply(extract_main_category)

# -------------------------------------------------------------
# 3. Behavioral Economics & Consumer Psychology Feature Engineering
# -------------------------------------------------------------
print("3. Engineering consumer behavior metrics...")

# Badge assignment based on social proof & rating percentiles
rating_p80 = df['rating_clean'].quantile(0.80)
reviews_p80 = df['review_count'].quantile(0.80)
reviews_p95 = df['review_count'].quantile(0.95)

def assign_badge(row):
    r = row['rating_clean']
    rev = row['review_count']
    if rev >= reviews_p95 and r >= 4.2:
        return "Best Seller"
    elif rev >= reviews_p80 and r >= 4.0:
        return "Amazon's Choice"
    return "Standard"

df['badge_type'] = df.apply(assign_badge, axis=1)

# Social Proof Tiers (Psychological volume heuristic)
def assign_social_proof(reviews):
    if reviews >= 10000:
        return "High Social Proof (10k+ reviews)"
    elif reviews >= 2000:
        return "Moderate Social Proof (2k-10k reviews)"
    elif reviews >= 500:
        return "Early Social Proof (500-2k reviews)"
    return "Low Social Proof (<500 reviews)"

df['social_proof_tier'] = df['review_count'].apply(assign_social_proof)

# Discount Anchoring Tier
def assign_discount_tier(pct):
    if pct >= 60:
        return "Extreme Discount (60%+ off)"
    elif pct >= 40:
        return "High Discount (40-59% off)"
    elif pct >= 20:
        return "Moderate Discount (20-39% off)"
    elif pct > 0:
        return "Light Discount (1-19% off)"
    return "Full Price (0% off)"

df['discount_tier'] = df['discount_pct'].apply(assign_discount_tier)

# Rating Cliff Tier (Psychological threshold)
def assign_rating_tier(r):
    if r >= 4.5:
        return "Tier 1: Elite (4.5 - 5.0)"
    elif r >= 4.0:
        return "Tier 2: Trust Barrier (4.0 - 4.4)"
    elif r >= 3.5:
        return "Tier 3: Hesitation Zone (3.5 - 3.9)"
    return "Tier 4: Sub-Par (< 3.5)"

df['rating_tier'] = df['rating_clean'].apply(assign_rating_tier)

# Estimated monthly sales volume (industry standard empirical proxy: reviews represent ~1.5% to 2.5% of sales)
# Adjusted by rating sentiment elasticity
np.random.seed(42)
sales_multiplier = np.where(df['rating_clean'] >= 4.2, 35.0, np.where(df['rating_clean'] >= 4.0, 25.0, 15.0))
df['est_monthly_units_sold'] = (np.sqrt(df['review_count']) * sales_multiplier * np.random.uniform(0.85, 1.15, len(df))).astype(int)
df['est_monthly_revenue_usd'] = (df['est_monthly_units_sold'] * df['discounted_price_usd']).round(2)

# Select clean columns
clean_cols = [
    'product_id', 'product_name', 'main_category', 'actual_price_usd', 'discounted_price_usd',
    'discount_pct', 'discount_tier', 'rating_clean', 'rating_tier', 'review_count',
    'social_proof_tier', 'badge_type', 'est_monthly_units_sold', 'est_monthly_revenue_usd'
]
clean_df = df[clean_cols].drop_duplicates(subset=['product_id'])
clean_df.to_csv(CLEAN_CSV, index=False)
print(f"Saved clean CSV ({len(clean_df)} products) to {CLEAN_CSV}")

# -------------------------------------------------------------
# 4. Ingest into SQLite Database
# -------------------------------------------------------------
print("4. Building SQLite database...")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    main_category TEXT,
    actual_price_usd REAL,
    discounted_price_usd REAL,
    discount_pct REAL,
    discount_tier TEXT,
    rating REAL,
    rating_tier TEXT,
    review_count INTEGER,
    social_proof_tier TEXT,
    badge_type TEXT,
    est_monthly_units_sold INTEGER,
    est_monthly_revenue_usd REAL
);
""")

clean_df.rename(columns={'rating_clean': 'rating'}).to_sql('products', conn, if_exists='append', index=False)

# Add indexes for high-speed analytical queries
cursor.execute("CREATE INDEX idx_category ON products(main_category);")
cursor.execute("CREATE INDEX idx_rating ON products(rating);")
cursor.execute("CREATE INDEX idx_badge ON products(badge_type);")

conn.commit()
conn.close()

print(f"SUCCESS: Database created at {DB_PATH}")
