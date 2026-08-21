# top10-html-analysis

Static, browser-based inventory analysis dashboard.

## Live dashboard

[Open the inventory analysis dashboard](https://edric-kaw.github.io/top10-html-analysis/)

## User guide

### Before you begin

- Use a current version of Chrome or Microsoft Edge.
- Prepare an Excel `.xlsx` file or a UTF-8 `.csv` file.
- Do not use the older `.xls` format.
- For `.xlsx` files, place the inventory table in the workbook's first worksheet.
- The first row must contain column names with the exact spelling shown below.

The three required columns are:

| Column | Purpose |
| --- | --- |
| `ItemSku` | Identifies the product variation. |
| `LocationCode` | Identifies the store or warehouse. |
| `BalanceQty` | Provides the inventory quantity used for stock status. |

The dashboard can also use these optional columns for richer descriptions,
filters, valuation, charts, and aging analysis:

`LocationDescription`, `ItemCode`, `ItemDescription`, `X-AxisDescription`,
`Y-AxisDescription`, `WeightedAverageCost`, `TotalWeightedAverageCost`,
`CurrentUnitPrice`, `BrandDescription`, `CategoryDescription`,
`SubCategoryDescription`, `DepartmentDescription`, `SeasonDescription`,
`VendorCode`, `VendorName`, `FirstGoodsReceiveDate`, `LastGoodsReceiveDate`, and
`BalanceDate`.

### Load an inventory file

1. Open the [live dashboard](https://edric-kaw.github.io/top10-html-analysis/).
2. Select **Data Center** from the left navigation.
3. Drag an `.xlsx` or `.csv` file onto the import area, or select
   **Choose inventory file**.
4. Wait for the success message confirming how many rows were imported.
5. The dashboard returns to **Overview** automatically after a successful import.

Importing another file replaces the current dataset for that browser session.

### Use the dashboard

- **Overview** shows inventory quantity, cost, potential retail value, active
  locations, stock exceptions, aging, and distribution charts.
- Use the search box to find a SKU, item, vendor, or location.
- Use the location, brand, category, and stock-status filters to narrow the view.
- Select **Location**, **Brand**, or **Category** above the distribution chart to
  change its grouping.
- Select **Investigate alerts** or **Warehouse** to inspect individual records.
- In Warehouse, sort by risk, quantity, value, or receipt age and choose the
  number of rows displayed per page.
- Select **Clear** to reset all active filters.

### Export or print results

- **Export filtered CSV** and **Export view** download only the records matching
  the current filters.
- The downloaded CSV is created locally by the browser.
- Use the printer button in the top-right corner to print the dashboard or save
  it as a PDF through the browser's print window.

### Configure stock rules

Open **Settings** to adjust the critical, low-stock, surplus, and inventory-aging
thresholds. Critical must be lower than low stock, and low stock must be lower
than surplus. The defaults are 3, 10, 30, and 365 days respectively. These
numeric settings are saved in the browser; inventory rows are not.

### Privacy and session behavior

- The published page starts with zero inventory records.
- A selected file is read and analysed on the user's device.
- Inventory rows are held only in the current page's memory and are not uploaded
  to GitHub or stored in browser storage.
- Refreshing or closing the page clears the imported inventory. Import the file
  again to continue working.
- The page includes a browser security policy that blocks network connections
  and form submissions.
- Anyone can access the public dashboard interface, but they cannot see another
  user's locally imported file or results.

### Troubleshooting

| Message or symptom | What to do |
| --- | --- |
| `Missing required columns` | Rename the headers to exactly `ItemSku`, `LocationCode`, and `BalanceQty`. |
| `The selected file contains no data rows` | Confirm that the file has a header row followed by at least one data row. |
| `No worksheet found` | Save the workbook again as a standard `.xlsx` file containing at least one worksheet. |
| Import fails for an Excel file | Try opening and resaving it in Excel, or export the data as a UTF-8 CSV. |
| Values or charts appear incomplete | Add the relevant optional description, cost, price, category, and date columns. |
| Data disappeared after refresh | This is expected for privacy; import the source file again. |

For the complete field reference, see the
[inventory data dictionary](documentation/inventory_data_dictionary.md).

## Public GitHub Pages build

Generate a public-safe `index.html` with no embedded inventory records:

```powershell
python scripts/build_public_dashboard.py
```

Visitors can load an `.xlsx` or `.csv` file from **Data Center**. The selected
file is processed locally in their browser and is not uploaded or persisted.

`operations-insight.html` is the private generated dashboard with embedded
inventory data and remains excluded from Git by `.gitignore`.
