import zipfile
import pandas as pd

# Update this path to point to your downloaded Census Place summary zip file
# (e.g., the mobile or fixed Census Place zip you downloaded for New Mexico)
census_place_zip = r"C:\Users\zack\Documents\ECE220\Project\FCC data\bdc_35_mobile_broadband_summary_by_geography_place_D25_29sep2026.zip"
provider_list_zip = r"C:\Users\zack\Documents\ECE220\Project\FCC data\bdc_us_provider_list_D25_29sep2026.zip"
output_csv_path = r"C:\Users\zack\Documents\ECE220\Project\four_towns_census_places.csv"

print("1. Loading Census Place summary data...")
with zipfile.ZipFile(census_place_zip, "r") as z:
  with z.open(z.namelist()[0]) as f:
    df_census = pd.read_csv(f, encoding="latin-1")

# Filter strictly for your 4 towns
target_towns = ["Taos", "Bloomfield", "Chama", "Cuba"]
pattern = "|".join(target_towns)

df_towns = df_census[
    df_census["geography_desc"].astype(str).str.contains(pattern, case=False, na=False)
].copy()

print(f"-> Found {len(df_towns)} geographic entries for your 4 towns.")

print("2. Loading Master Provider List...")
with zipfile.ZipFile(provider_list_zip, "r") as z:
  with z.open(z.namelist()[0]) as f:
    df_providers = pd.read_csv(f, encoding="latin-1")

print("3. Merging with Master Provider List...")
# Check if provider_id is in the census file, otherwise join via available keys
if "provider_id" in df_towns.columns:
  df_final = pd.merge(df_towns, df_providers, on="provider_id", how="inner")
else:
  # If the census place file doesn't have provider_id, print columns to inspect
  print(
      "Notice: 'provider_id' not directly in census file. Columns are:"
      f" {df_towns.columns.tolist()}"
  )
  df_final = df_towns

# Save and export
df_final.to_csv(output_csv_path, index=False)
print(f"\nSaved successfully to:\n{output_csv_path}")

print("\nPreview of towns found:")
print(df_final[["geography_desc"]].drop_duplicates())
