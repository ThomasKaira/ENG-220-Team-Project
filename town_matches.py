import zipfile
import pandas as pd
import os

# 1. Define file paths for your zip archives and output CSV
mobile_summary_zip = r"C:\Users\zack\Documents\ECE220\Project\FCC data\bdc_35_mobile_broadband_summary_by_geography_place_D25_29sep2026.zip" 
provider_summary_zip = r"C:\Users\zack\Documents\ECE220\Project\FCC data\bdc_us_provider_summary_by_geography_D25_29sep2026.zip" 
provider_list_zip = r"C:\Users\zack\Documents\ECE220\Project\FCC data\bdc_us_provider_list_D25_29sep2026.zip" 

output_csv_path = r"C:\Users\zack\Documents\ECE220\Project\FCC data\filtered_towns_merged_broadband_data.csv"

# 2. Helper function to read the first CSV inside a zip file
def read_csv_from_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_files = [f for f in z.namelist() if f.endswith('.csv')]
        if not csv_files:
            raise ValueError(f"No CSV file found inside {zip_path}")
        with z.open(csv_files[0]) as f:
            return pd.read_csv(f)

print("Loading datasets from ZIP archives...")
df_mobile_summary = read_csv_from_zip(mobile_summary_zip)
df_provider_summary = read_csv_from_zip(provider_summary_zip)
df_provider_list = read_csv_from_zip(provider_list_zip)

# 3. Keep requested columns from the mobile broadband summary (including 'geography_desc' if present for filtering)
mobile_cols_to_keep = [
    'geography_id',
    'geography_desc',
    'mobilebb_4g_area_st_pct',
    'mobilebb_4g_area_iv_pct',
    'mobilebb_5g_spd1_area_st_pct',
    'mobilebb_5g_spd1_area_iv_pct',
    'mobilebb_5g_spd2_area_st_pct',
    'mobilebb_5g_spd2_area_iv_pct'
]
existing_mobile_cols = [c for c in mobile_cols_to_keep if c in df_mobile_summary.columns]
df_mobile_trimmed = df_mobile_summary[existing_mobile_cols]

# 4. Keep ONLY geography_id and provider_id from the Provider Summary file
provider_summary_cols = ['geography_id', 'provider_id']
existing_summary_cols = [c for c in provider_summary_cols if c in df_provider_summary.columns]
df_provider_summary_trimmed = df_provider_summary[existing_summary_cols]

# 5. Merge Mobile Summary with Provider Summary on 'geography_id'
print("Merging Mobile Summary with Provider Summary on 'geography_id'...")
merged_df = pd.merge(
    df_mobile_trimmed, 
    df_provider_summary_trimmed, 
    on='geography_id', 
    how='left'
)

# 6. Filter rows for specific towns: Cuba, Chama, Bloomfield, Taos
target_towns = ['cuba', 'chama', 'bloomfield', 'taos']
pattern = '|'.join(target_towns)

if 'geography_desc' in merged_df.columns:
    print("Filtering rows for Cuba, Chama, Bloomfield, and Taos...")
    merged_df = merged_df[merged_df['geography_desc'].astype(str).str.contains(pattern, case=False, na=False)]
else:
    raise ValueError("The 'geography_desc' column is missing from the mobile summary dataset, which is required for filtering towns.")

# 7. Merge with US Provider List using 'provider_id' to pull in the provider/holding company name
name_col = 'holding_company' if 'holding_company' in df_provider_list.columns else 'provider'

if 'provider_id' in df_provider_list.columns and name_col in df_provider_list.columns:
    print(f"Merging with US Provider List using '{name_col}'...")
    df_provider_list_trimmed = df_provider_list[['provider_id', name_col]]
    
    merged_df = pd.merge(
        merged_df, 
        df_provider_list_trimmed, 
        on='provider_id', 
        how='left'
    )
else:
    raise ValueError(f"Could not find 'provider_id' or '{name_col}' in the provider list file.")

# 8. Reorder key columns upfront
front_cols = [col for col in ['geography_id', 'geography_desc', 'provider_id', name_col] if col in merged_df.columns]
remaining_cols = [col for col in merged_df.columns if col not in front_cols]
final_df = merged_df[front_cols + remaining_cols]

# 9. Save directly as a plain CSV file
final_df.to_csv(output_csv_path, index=False)

print(f"\nSuccessfully processed, filtered, and merged all datasets!")
print(f"Saved output CSV file to: {output_csv_path}")

# ==========================================
# 10. POST-PROCESSING CONTENT INSPECTION
# ==========================================
print("\n" + "="*40)
print("POST-PROCESSING CONTENT INSPECTION")
print("="*40)
print(f"Total Rows: {len(final_df)}")
print(f"Total Columns: {len(final_df.columns)}")
print("\nFinal Column Names:")
print(final_df.columns.tolist())
print("\nFirst 5 Rows Preview:")
print(final_df.head())
