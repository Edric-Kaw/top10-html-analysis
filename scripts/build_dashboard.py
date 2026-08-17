from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "IMDR002_InventoryBalanceByDate.xlsx"
TEMPLATE = ROOT / "src" / "dashboard.template.html"
OUTPUT = ROOT / "operations-insight.html"

df = pd.read_excel(SOURCE, sheet_name="data")

date_cols = ["BalanceDate", "FirstGoodsReceiveDate", "LastGoodsReceiveDate"]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

text_cols = [
    "LocationCode", "LocationDescription", "ItemCode", "ItemDescription",
    "X-AxisDescription", "Y-AxisDescription", "ItemSku", "BrandDescription",
    "CategoryDescription", "SubCategoryDescription", "DepartmentDescription",
    "SeasonDescription", "VendorCode", "VendorName"
]
for col in text_cols:
    df[col] = df[col].fillna("").astype(str)

num_cols = ["BalanceQty", "WeightedAverageCost", "TotalWeightedAverageCost", "CurrentUnitPrice"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Compact arrays keep the single offline HTML practical while retaining all rows.
columns = [
    "LocationCode", "LocationDescription", "ItemCode", "ItemDescription",
    "X-AxisDescription", "Y-AxisDescription", "ItemSku", "BalanceQty",
    "WeightedAverageCost", "TotalWeightedAverageCost", "CurrentUnitPrice",
    "BrandDescription", "CategoryDescription", "SubCategoryDescription",
    "DepartmentDescription", "SeasonDescription", "VendorCode", "VendorName",
    "FirstGoodsReceiveDate", "LastGoodsReceiveDate"
]
compact = []
for _, row in df[columns].iterrows():
    compact.append([
        row["LocationCode"], row["LocationDescription"], row["ItemCode"], row["ItemDescription"],
        row["X-AxisDescription"], row["Y-AxisDescription"], row["ItemSku"], round(float(row["BalanceQty"]), 3),
        round(float(row["WeightedAverageCost"]), 4), round(float(row["TotalWeightedAverageCost"]), 2),
        round(float(row["CurrentUnitPrice"]), 2), row["BrandDescription"], row["CategoryDescription"],
        row["SubCategoryDescription"], row["DepartmentDescription"], row["SeasonDescription"],
        row["VendorCode"], row["VendorName"],
        row["FirstGoodsReceiveDate"].strftime("%Y-%m-%d") if pd.notna(row["FirstGoodsReceiveDate"]) else "",
        row["LastGoodsReceiveDate"].strftime("%Y-%m-%d") if pd.notna(row["LastGoodsReceiveDate"]) else ""
    ])

meta = {
    "file": SOURCE.name,
    "sheet": "data",
    "rows": len(df),
    "balanceDate": df["BalanceDate"].max().strftime("%Y-%m-%d"),
    "generated": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
    "schema": "Inventory Schema v1"
}

payload = json.dumps({"meta": meta, "columns": columns, "rows": compact}, ensure_ascii=False, separators=(",", ":"))
html = TEMPLATE.read_text(encoding="utf-8").replace("/*__INVENTORY_DATA__*/", f"window.INVENTORY_DATA={payload};")
OUTPUT.write_text(html, encoding="utf-8")
print(f"Created {OUTPUT} ({OUTPUT.stat().st_size / 1024 / 1024:.1f} MB, {len(df):,} rows)")
