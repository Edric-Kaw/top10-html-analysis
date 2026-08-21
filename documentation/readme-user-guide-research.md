# README user-guide research

Date: 2026-08-21

## Recommended user journey

1. Open the [live dashboard](https://edric-kaw.github.io/top10-html-analysis/). It intentionally starts without inventory data in the public build. ([public build script](../scripts/build_public_dashboard.py))
2. Select **Data Center**, then either drag one file onto the import area or choose **Choose inventory file**. A successful import becomes the active dataset and returns the user to **Overview**. ([dashboard source](../src/dashboard.template.html#L39), [import handlers](../src/dashboard.template.html#L80))
3. Use **Overview** for KPIs, alerts, and charts; **Warehouse** for row-level investigation; **Data Center** to replace the active file; and **Settings** to adjust classification rules. Sales and Purchasing are visibly marked as planned and are not usable. ([navigation](../src/dashboard.template.html#L24))

## Supported files and schema

- Accepted formats are `.xlsx` and UTF-8 `.csv`; legacy `.xls` is not accepted. CSV parsing expects comma-separated headers and supports quoted values. ([file control](../src/dashboard.template.html#L39), [CSV parser](../src/dashboard.template.html#L76))
- For `.xlsx`, the importer reads the first worksheet file it finds. Put the inventory table—with headers in the first row—on the first worksheet. Password-protected, malformed, or unusually compressed workbooks may fail. ([XLSX reader](../src/dashboard.template.html#L78))
- Header names are case-sensitive. The three required columns are `ItemSku`, `LocationCode`, and `BalanceQty`. The file must contain at least one data row. ([validation](../src/dashboard.template.html#L80))
- For complete analytics, include these 20 supported columns:

  `LocationCode`, `LocationDescription`, `ItemCode`, `ItemDescription`, `X-AxisDescription`, `Y-AxisDescription`, `ItemSku`, `BalanceQty`, `WeightedAverageCost`, `TotalWeightedAverageCost`, `CurrentUnitPrice`, `BrandDescription`, `CategoryDescription`, `SubCategoryDescription`, `DepartmentDescription`, `SeasonDescription`, `VendorCode`, `VendorName`, `FirstGoodsReceiveDate`, `LastGoodsReceiveDate`.

  The Data Center reports how many of these fields were found. Missing optional text/date fields become blank; missing or invalid numeric analytics fields become zero, so incomplete input can produce misleading costs, retail values, margins, labels, or aging. ([column map and coercion](../src/dashboard.template.html#L74), [validation](../src/dashboard.template.html#L80))
- `BalanceDate` is optional but recommended. When present, the latest valid value is used as the snapshot date and aging reference; when absent, the browser's current date is used. Date columns accept Excel serial dates or parseable date text. ([date handling](../src/dashboard.template.html#L75), [activation logic](../src/dashboard.template.html#L80))

## Privacy and local-only behavior

- Choosing or dropping a file reads it in browser memory with `file.text()` or `file.arrayBuffer()`; the reviewed dashboard contains no upload request. Imported rows are not written to browser storage. ([import implementation](../src/dashboard.template.html#L81), [security audit](github-pages-security-privacy-research.md))
- Imported inventory lasts only for the current page session. Refreshing, closing the tab, or reopening the site clears it; the user must import again. Importing another file replaces the current dataset and resets filters and pagination. ([activation logic](../src/dashboard.template.html#L80))
- The only persistent browser data is the four threshold settings stored under `oi-settings` in `localStorage`. Inventory rows are not included. ([state initialization](../src/dashboard.template.html#L49), [settings save](../src/dashboard.template.html#L83))
- CSV exports and printing are created locally by the browser. Users should still save exports only to approved locations because the downloaded CSV contains the currently filtered inventory data. ([CSV export](../src/dashboard.template.html#L72), [print behavior](../src/dashboard.template.html#L16))

## Using the dashboard

- **Overview:** shows filtered inventory quantity, cost, potential retail, active locations, stock exceptions, aged positions, distribution, priority signals, stock health, aging, and margin opportunity. Switch the distribution chart among Location, Brand, and Category. ([overview](../src/dashboard.template.html#L37), [metrics and charts](../src/dashboard.template.html#L59))
- **Warehouse:** shows the filtered SKU-location table. Sort by risk, quantity, value, or receipt age; show 25, 50, or 100 rows per page; and use previous/next pagination. ([warehouse view](../src/dashboard.template.html#L38), [table logic](../src/dashboard.template.html#L69))
- **Shared filters:** search SKU, item code/description, vendor, or location description; combine this with Location, Brand, Category, and Stock status. Filters apply across Overview and Warehouse. **Clear** resets all filters. ([filter logic](../src/dashboard.template.html#L53))
- The bell shortcut opens Warehouse with the Critical status filter. **Investigate alerts** opens Warehouse without changing the current filters. The printer button prints the active view. ([event handlers](../src/dashboard.template.html#L82))
- **Export filtered CSV** and **Export view** both download all rows matching the current shared filters, not merely the visible table page. The export includes calculated status, retail value, margin, and age. ([CSV export](../src/dashboard.template.html#L72))

## Settings and reset behavior

- Defaults are Critical `3`, Low `10`, Surplus `30`, and Aging `365` days. Negative and zero quantities are always classified as Negative and Out of stock. Positive quantities use the saved thresholds. ([state and status rules](../src/dashboard.template.html#L49))
- Saving requires `critical < low < surplus`; otherwise the dashboard shows an error and does not save. Saving immediately recalculates the analytics and persists the thresholds on that browser/device. ([settings handler](../src/dashboard.template.html#L83))
- **Refresh/reset:** reloading clears inventory and unsaved filters but keeps saved thresholds. To restore default thresholds, enter `3`, `10`, `30`, and `365`, then select **Save local settings**. Clearing this site's browser data also removes the saved thresholds.

## Troubleshooting guidance for README

- **Missing required columns:** use the exact, case-sensitive names `ItemSku`, `LocationCode`, and `BalanceQty`; remove leading/trailing spaces from header cells.
- **No data rows:** ensure the first row contains headers and at least one populated row follows it.
- **Excel import fails:** save as `.xlsx` (not `.xls`), move the inventory table to the first worksheet, remove workbook encryption, and try again in a current browser.
- **CSV imports incorrectly:** export a UTF-8, comma-delimited CSV with one header row; quote fields that contain commas or quotation marks.
- **Zero or blank analytics:** add the relevant optional columns, especially cost, price, descriptions, and receipt dates; invalid numeric values are treated as zero.
- **Unexpected aging date:** include a valid `BalanceDate`; otherwise the current date is used.
- **Data disappeared after refresh:** this is expected session-only behavior; import the source file again.
- **Filters seem to hide data:** select **Clear**. Filters are shared between Overview and Warehouse.
- **Settings seem to return:** they persist locally by design; restore defaults and save, or clear the site's browser data.
- **Export has more rows than the current table page:** exports include every filtered row, independent of page size and pagination.

## README wording cautions

- Do not include real SKUs, vendors, locations, filenames, quantities, prices, or screenshots containing business data.
- Describe the privacy boundary precisely: inventory is read and processed locally for the current session, while threshold settings persist locally. Do not claim that the browser stores nothing.
- State that users are responsible for handling downloaded CSVs and printed output securely; those artifacts contain inventory data even though the website does not upload it.
