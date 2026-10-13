import geopandas as gpd

# 1. Load the shapefile (point to your .shp file)
shapefile_path = "C:\\Users\\zack\\Documents\\ECE220\\Project\\FCC data\\extracted_mobile_shapefile\\bdc_35_5GNR_mobile_broadband_h3_D25_29sep2026.shp"
gdf = gpd.read_file(shapefile_path)

# 2. Check the columns in the shapefile
print("--- Shapefile Columns ---")
print(gdf.columns.tolist())

# 3. Search for '5g' or '500' in the columns/contents
print("\n--- Searching for 5G / 500 ---")
found = False
for col in gdf.columns:
    matches = gdf[gdf[col].astype(str).str.contains('5g|500', case=False, na=False)]
    if not matches.empty:
        found = True
        print(f"Found matches in column: {col}")

if not found:
    print("No matches for '5g' or '500' found.")

# 4. Convert and save the shapefile as a CSV
# (Note: If the shapefile contains geometry polygons/points, you might want to drop geometry or convert it to WKT text first)
gdf_no_geom = gdf.drop(columns='geometry') # Drops the spatial map shapes for a clean table
output_csv = "converted_file.csv"
gdf_no_geom.to_csv(output_csv, index=False)

print(f"\nSuccessfully converted shapefile to CSV: {output_csv}")
