import os
import zipfile
import shutil

PROJECT_DIR = r"C:\Users\asefh\Downloads\Evaluating Projects\Amazon_Consumer_Behavior_SQL"
TABLEAU_DIR = os.path.join(PROJECT_DIR, "tableau")
os.makedirs(TABLEAU_DIR, exist_ok=True)

CSV_SRC = os.path.join(PROJECT_DIR, "data", "amazon_clean.csv")
TWB_FILE = os.path.join(TABLEAU_DIR, "Amazon_Consumer_Behavior_Executive_Dashboard.twb")
TWBX_FILE = os.path.join(TABLEAU_DIR, "Amazon_Consumer_Behavior_Executive_Dashboard.twbx")

twb_xml = """<?xml version='1.0' encoding='utf-8' ?>
<workbook original-version='18.1' source-build='2025.2.2' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <AnimationOnByDefault />
    <MarkAnimation />
    <ObjectModelEncapsulateLegacy />
    <ObjectModelTableType />
    <SchemaViewerObjectModel />
    <SheetIdentifierTracking />
    <WindowsPersistSimpleIdentifiers />
  </document-format-change-manifest>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='amazon_clean' inline='true' name='federated.amazon_data_source' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='amazon_clean' name='textscan.amazon_clean_conn'>
            <connection class='textscan' cleaning='no' compat='no' dataRefreshTime='' directory='Data' filename='amazon_clean.csv' interpretationMode='0' password='' server='' validate='no' />
          </named-connection>
        </named-connections>
        <relation connection='textscan.amazon_clean_conn' name='amazon_clean.csv' table='[amazon_clean#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>
            <column datatype='string' name='product_id' ordinal='0' />
            <column datatype='string' name='product_name' ordinal='1' />
            <column datatype='string' name='main_category' ordinal='2' />
            <column datatype='real' name='actual_price_usd' ordinal='3' />
            <column datatype='real' name='discounted_price_usd' ordinal='4' />
            <column datatype='real' name='discount_pct' ordinal='5' />
            <column datatype='string' name='discount_tier' ordinal='6' />
            <column datatype='real' name='rating_clean' ordinal='7' />
            <column datatype='string' name='rating_tier' ordinal='8' />
            <column datatype='integer' name='review_count' ordinal='9' />
            <column datatype='string' name='social_proof_tier' ordinal='10' />
            <column datatype='string' name='badge_type' ordinal='11' />
            <column datatype='integer' name='est_monthly_units_sold' ordinal='12' />
            <column datatype='real' name='est_monthly_revenue_usd' ordinal='13' />
          </columns>
        </relation>
        <metadata-records>
          <metadata-record class='capability'>
            <remote-name />
            <remote-type>0</remote-type>
            <parent-name>[amazon_clean.csv]</parent-name>
            <remote-alias />
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
        </metadata-records>
      </connection>
      <aliases enabled='yes' />
      <column datatype='string' name='[product_id]' role='dimension' type='nominal' />
      <column datatype='string' name='[product_name]' role='dimension' type='nominal' />
      <column datatype='string' name='[main_category]' role='dimension' type='nominal' />
      <column datatype='real' name='[actual_price_usd]' role='measure' type='quantitative' />
      <column datatype='real' name='[discounted_price_usd]' role='measure' type='quantitative' />
      <column datatype='real' name='[discount_pct]' role='measure' type='quantitative' />
      <column datatype='string' name='[discount_tier]' role='dimension' type='nominal' />
      <column datatype='real' name='[rating_clean]' role='measure' type='quantitative' />
      <column datatype='string' name='[rating_tier]' role='dimension' type='nominal' />
      <column datatype='integer' name='[review_count]' role='measure' type='quantitative' />
      <column datatype='string' name='[social_proof_tier]' role='dimension' type='nominal' />
      <column datatype='string' name='[badge_type]' role='dimension' type='nominal' />
      <column datatype='integer' name='[est_monthly_units_sold]' role='measure' type='quantitative' />
      <column datatype='real' name='[est_monthly_revenue_usd]' role='measure' type='quantitative' />
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='Sheet 1 - The 4.0 Star Rating Cliff'>
      <table>
        <view>
          <datasources>
            <datasource caption='amazon_clean' name='federated.amazon_data_source' />
          </datasources>
        </view>
      </table>
    </worksheet>
    <worksheet name='Sheet 2 - Badge Endorsement Lift'>
      <table>
        <view>
          <datasources>
            <datasource caption='amazon_clean' name='federated.amazon_data_source' />
          </datasources>
        </view>
      </table>
    </worksheet>
    <worksheet name='Sheet 3 - Price Anchoring Analysis'>
      <table>
        <view>
          <datasources>
            <datasource caption='amazon_clean' name='federated.amazon_data_source' />
          </datasources>
        </view>
      </table>
    </worksheet>
    <worksheet name='Sheet 4 - Category Discount Depth'>
      <table>
        <view>
          <datasources>
            <datasource caption='amazon_clean' name='federated.amazon_data_source' />
          </datasources>
        </view>
      </table>
    </worksheet>
  </worksheets>
  <dashboards>
    <dashboard name='Executive Pricing &amp; Behavioral Insights'>
      <style />
      <size maxheight='850' maxwidth='1300' minheight='850' minwidth='1300' sizing-mode='fixed' />
      <zones>
        <zone h='100000' id='4' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='12000' id='5' name='Title' type-v2='title' w='100000' x='0' y='0' />
        </zone>
      </zones>
    </dashboard>
  </dashboards>
  <windows>
    <window class='dashboard' maximized='true' name='Executive Pricing &amp; Behavioral Insights'>
      <viewpoints />
      <active id='-1' />
    </window>
  </windows>
</workbook>
"""

with open(TWB_FILE, "w", encoding="utf-8") as f:
    f.write(twb_xml)

print(f"Created TWB XML at: {TWB_FILE}")

# Now package into .twbx zip archive
with zipfile.ZipFile(TWBX_FILE, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(TWB_FILE, arcname="Amazon_Consumer_Behavior_Executive_Dashboard.twb")
    z.write(CSV_SRC, arcname="Data/amazon_clean.csv")

print(f"Created Packaged Tableau Workbook (.twbx) at: {TWBX_FILE}")
