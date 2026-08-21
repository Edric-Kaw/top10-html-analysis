from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "src" / "dashboard.template.html"
OUTPUT = ROOT / "index.html"

COLUMNS = [
    "LocationCode", "LocationDescription", "ItemCode", "ItemDescription",
    "X-AxisDescription", "Y-AxisDescription", "ItemSku", "BalanceQty",
    "WeightedAverageCost", "TotalWeightedAverageCost", "CurrentUnitPrice",
    "BrandDescription", "CategoryDescription", "SubCategoryDescription",
    "DepartmentDescription", "SeasonDescription", "VendorCode", "VendorName",
    "FirstGoodsReceiveDate", "LastGoodsReceiveDate"
]

payload = json.dumps({
    "meta": {
        "file": "No dataset loaded",
        "sheet": "Browser import",
        "rows": 0,
        "balanceDate": "",
        "generated": "",
        "schema": "Inventory Schema v1"
    },
    "columns": COLUMNS,
    "rows": []
}, separators=(",", ":"))

html = TEMPLATE.read_text(encoding="utf-8")
html = html.replace(
    "/*__INVENTORY_DATA__*/",
    f"window.INVENTORY_DATA={payload};"
)
html = html.replace(
    '<span class="status healthy" id="connectionBadge">Ready</span>',
    '<span class="status" id="connectionBadge">Waiting for data</span>'
)
html = html.replace(
    "The bundled workbook is active. Import another file to replace it for this session.",
    "No inventory is loaded. Choose a file to begin; it will stay in this browser session."
)
html = html.replace(
    "document.getElementById('subtitle').textContent=`${D.meta.balanceDate} snapshot · ${fmt.format(rows.length)} SKU-location records · ${fmt.format(m.skus)} unique SKUs`",
    "document.getElementById('subtitle').textContent=raw.length?`${D.meta.balanceDate} snapshot · ${fmt.format(rows.length)} SKU-location records · ${fmt.format(m.skus)} unique SKUs`:'No inventory loaded · Open Data Center to import an Excel or CSV file'"
)
html = html.replace(
    "render();navigate('overview');toast(`${fmt.format(rows.length)} rows imported locally`)",
    "render();document.getElementById('connectionBadge').textContent='Ready';document.getElementById('connectionBadge').className='status healthy';navigate('overview');toast(`${fmt.format(rows.length)} rows imported locally`)"
)

OUTPUT.write_text(html, encoding="utf-8")
print(f"Created public-safe {OUTPUT} with no embedded inventory records")
