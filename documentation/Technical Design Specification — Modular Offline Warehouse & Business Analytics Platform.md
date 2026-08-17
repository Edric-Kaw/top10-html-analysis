# Technical Design Specification  
## Modular Offline Warehouse & Business Analytics Platform

**Version:** 3.0  
**Current Primary Module:** Warehouse Inventory  
**Deployment Mode:** Fully Offline  
**Future Modules:** Sales, Purchasing, Receiving, Transfers, Replenishment, Product Performance, Vendor Analysis and Management Reporting

---

# 1. Design Direction

The application must be designed as a **modular business analytics platform**, not as a warehouse-only page.

The first release will focus on:

> **Warehouse Inventory Monitoring & Stock Alerts**

However, the structure must allow future modules to be added without rebuilding the application from scratch.

Potential future modules include:

```text
Warehouse
Sales
Purchasing
Goods Receiving
Stock Transfers
Replenishment
Vendor Analysis
Product Performance
Inventory Movement
Management Overview
```

The core design principle is:

```text
ONE PLATFORM
     ↓
MULTIPLE DATA SOURCES
     ↓
MULTIPLE BUSINESS MODULES
     ↓
SHARED FILTERS & ANALYTICS ENGINE
```

---

# 2. Future-Proof User Interface

The interface should use a professional application shell rather than a single long dashboard.

Recommended structure:

```text
┌──────────────────────────────────────────────────────────────┐
│ BUSINESS ANALYTICS CONTROL                                  │
│ Offline Operations & Analytics Platform                     │
├──────────────┬───────────────────────────────────────────────┤
│              │                                               │
│ OVERVIEW     │             MAIN WORKSPACE                    │
│              │                                               │
│ WAREHOUSE    │                                               │
│              │                                               │
│ SALES        │                                               │
│              │                                               │
│ PURCHASING   │                                               │
│              │                                               │
│ TRANSFERS    │                                               │
│              │                                               │
│ VENDORS      │                                               │
│              │                                               │
│ DATA CENTER  │                                               │
│              │                                               │
│ SETTINGS     │                                               │
│              │                                               │
└──────────────┴───────────────────────────────────────────────┘
```

Modules that are not yet implemented should remain hidden rather than showing broken or empty pages.

---

# 3. Recommended Main Navigation

The first version should contain:

```text
Overview
Warehouse
Data Center
Settings
```

Future versions can progressively enable:

```text
Overview
Warehouse
Sales
Purchasing
Transfers
Receiving
Products
Vendors
Analytics
Data Center
Settings
```

This prevents the system from looking like a warehouse-specific tool that later has unrelated features attached to it.

---

# 4. Application Architecture

Use a modular architecture.

Recommended development structure:

```text
business-analytics-platform/
│
├── index.html
│
├── assets/
│   ├── css/
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── responsive.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── router.js
│   │   │
│   │   ├── core/
│   │   │   ├── file-loader.js
│   │   │   ├── data-store.js
│   │   │   ├── data-validator.js
│   │   │   ├── data-normalizer.js
│   │   │   ├── filter-engine.js
│   │   │   ├── aggregation-engine.js
│   │   │   ├── export-engine.js
│   │   │   └── settings-manager.js
│   │   │
│   │   ├── modules/
│   │   │   ├── overview/
│   │   │   ├── warehouse/
│   │   │   ├── sales/
│   │   │   ├── purchasing/
│   │   │   ├── transfers/
│   │   │   └── vendors/
│   │   │
│   │   └── vendor/
│   │       ├── xlsx.full.min.js
│   │       └── chart.umd.min.js
│   │
│   └── icons/
│
└── README.md
```

For final distribution, these files may later be bundled into one offline HTML file.

---

# 5. Separate Core Engine From Business Modules

A critical requirement is that generic functions must not be written directly inside the warehouse dashboard.

For example:

### Core Engine

Should handle:

```text
File Import
Excel Parsing
CSV Parsing
Column Detection
Data Validation
Data Cleaning
Filtering
Grouping
Aggregation
Searching
Pagination
Export
Settings
Formatting
```

### Warehouse Module

Should handle:

```text
Stock Quantity
Low Stock
Out of Stock
Negative Stock
Inventory Aging
Inventory Location
Warehouse Alerts
```

### Future Sales Module

Should handle:

```text
Sales Revenue
Units Sold
Transactions
Gross Sales
Discounts
Product Sales
Store Performance
Sales Trends
```

This separation is essential.

---

# 6. Central Data Store

The application should maintain a centralized in-memory data store.

Conceptually:

```javascript
AppData = {
    inventory: [],
    sales: [],
    purchasing: [],
    receiving: [],
    transfers: [],
    vendors: [],
    products: []
};
```

The initial release may only populate:

```javascript
AppData.inventory
```

Future files can populate additional datasets without changing the warehouse logic.

---

# 7. Dataset Registry

Every uploaded dataset should be identified by type.

Example:

```javascript
DatasetRegistry = {
    inventory: {
        loaded: true,
        rows: 18420,
        sourceFile: "Inventory_August.xlsx"
    },

    sales: {
        loaded: false
    },

    purchasing: {
        loaded: false
    }
};
```

This enables modules to determine whether the required data exists.

---

# 8. Data Center

Instead of using only a warehouse upload box, create a reusable:

# Data Center

The Data Center manages all imported files.

Initial screen:

```text
DATA CENTER

Inventory Balance
✓ Inventory_August.xlsx
18,420 rows
17 Aug 2026

[ Replace File ]

---------------------------------

Sales Data
Not Loaded

[ Import Sales File ]

---------------------------------

Purchase Data
Not Loaded

[ Import Purchase File ]
```

For Version 1, only the inventory import needs to be enabled.

Future datasets can be added here.

---

# 9. Dataset Auto-Detection

When a file is dropped into the application, the program should attempt to determine its type based on column names.

Example:

Inventory dataset:

```text
BalanceDate
ItemSku
BalanceQty
LocationCode
```

→ classify as:

```text
Inventory
```

Future sales dataset:

```text
SalesDate
ReceiptNumber
ItemSku
SalesQty
NetSales
```

→ classify as:

```text
Sales
```

If the system cannot determine the dataset:

```text
Dataset type could not be detected.

Please select:

[ Inventory ]
[ Sales ]
[ Purchasing ]
[ Other ]
```

---

# 10. Universal Product Key

Future analytics will rely heavily on connecting datasets.

The primary recommended joining field is:

```text
ItemSku
```

Additional joining fields:

```text
ItemCode
ItemBarcode
LocationCode
VendorCode
BalanceDate
```

For example:

```text
Inventory
ItemSku
   ↓
Sales
ItemSku
   ↓
Purchasing
ItemSku
```

This enables cross-module analysis later.

---

# 11. Shared Master Dimensions

The system should internally treat several fields as reusable business dimensions.

### Product

```text
ItemCode
ItemSku
ItemBarcode
ItemDescription
```

### Product Classification

```text
Brand
Group
Category
Subcategory
Department
Season
Color
Size
```

### Location

```text
LocationCode
HQLocationCode
LocationDescription
```

### Vendor

```text
VendorCode
VendorName
```

These dimensions should be reusable across warehouse, sales and purchasing modules.

---

# 12. Common Filtering Engine

Do not develop different filter systems for every module.

Use one reusable filter engine.

Common filters:

```text
Date
Location
Brand
Department
Category
Subcategory
Vendor
Item
SKU
Color
Size
Season
```

Each module can additionally provide its own filters.

Warehouse:

```text
Stock Status
Age Bucket
```

Future Sales:

```text
Sales Channel
Promotion
Transaction Type
```

---

# 13. Persistent Global Context

The user should be able to select:

```text
Location: Sunway Pyramid
Brand: TOPTEN10
```

and move between:

```text
Warehouse
Sales
Products
```

while retaining the same filters where applicable.

This creates a connected analytical experience.

---

# 14. Overview Module

The platform should eventually contain a management-level Overview page.

Initial Version 1 overview may display:

```text
Inventory Quantity
Inventory Cost
Locations
Low Stock
Out of Stock
Aging Inventory
```

When Sales is added later:

```text
Today's / Period Sales
Units Sold
Inventory
Stock Alerts
Sales vs Stock
Top Products
Top Locations
```

The Overview module therefore should use cards that can be dynamically registered rather than hard-coded permanently.

---

# 15. Modular KPI System

KPIs should be defined as reusable configuration objects.

Concept:

```javascript
{
    id: "totalStock",
    module: "warehouse",
    title: "Total Stock",
    type: "number",
    calculation: "sum",
    field: "BalanceQty"
}
```

Future:

```javascript
{
    id: "netSales",
    module: "sales",
    title: "Net Sales",
    type: "currency",
    calculation: "sum",
    field: "NetSales"
}
```

This makes it easier to add or remove KPI cards.

---

# 16. Modular Chart System

Charts should also use reusable components.

Examples:

```text
Bar Chart
Horizontal Bar
Line Chart
Donut Chart
Stacked Bar
Trend Chart
```

Business modules provide:

```text
Data
Title
Grouping
Metric
```

The shared chart component handles rendering.

---

# 17. Warehouse Module

The current Warehouse module remains the primary Version 1 functionality.

Sections:

```text
Warehouse Status
Critical Alerts
Low Stock
Out of Stock
Negative Stock
Inventory by Location
Inventory Aging
Stock by Brand
Stock by Category
Size Availability
Color Availability
Vendor Exposure
SKU Inventory
Potential Transfer Opportunities
```

This functionality should remain isolated under:

```text
modules/warehouse/
```

---

# 18. Future Sales Module

The architecture must be capable of adding a Sales module later.

Potential Sales KPIs:

```text
Net Sales
Gross Sales
Units Sold
Transaction Count
Average Transaction Value
Discount Amount
Average Selling Price
```

Possible analysis:

```text
Sales by Date
Sales by Store
Sales by Product
Sales by Brand
Sales by Category
Sales by Size
Sales by Color
Sales by Season
Top Selling Items
Lowest Selling Items
```

---

# 19. Inventory + Sales Integration

Once sales data exists, the system can provide much stronger inventory analysis.

Example:

```text
Current Inventory
+
Units Sold
=
Stock Productivity
```

Possible future metrics:

```text
Sell-Through Rate
Days of Supply
Weeks of Supply
Stock Turnover
Stock Cover
Sales Velocity
Fast-Moving Items
Slow-Moving Items
Dead Stock Candidates
Stockout Risk
Replenishment Priority
```

These must only become available once sufficient sales history exists.

---

# 20. Example Future Product View

The system should eventually support a unified Product view.

Example:

```text
PRODUCT
MBF2JJ1002
Short Sleeve Woven T-Shirts

Current Stock
82 Units

Warehouse Stock
46

Store Stock
36

30-Day Sales
57 Units

Average Daily Sales
1.9

Estimated Stock Cover
43 Days

Stock Status
Healthy

Locations
Warehouse    46
Sunway        6
Mid Valley   12
Pavilion     18
```

This is why the initial data model must not be warehouse-specific.

---

# 21. Future Purchasing Module

Possible dataset:

```text
PurchaseOrderNumber
OrderDate
VendorCode
ItemSku
OrderedQty
ReceivedQty
UnitCost
ExpectedDeliveryDate
Status
```

Future dashboard:

```text
Open Purchase Orders
Incoming Quantity
Late Deliveries
Outstanding Quantity
Vendor Performance
Purchase Cost
Expected Receipts
```

---

# 22. Future Goods Receiving Module

Possible analysis:

```text
Goods Received Today
Receiving Volume
Delayed Receipts
Items Received
Vendor Receipts
Warehouse Receiving Activity
```

This can eventually replace simplistic analysis based only on `LastGoodsReceiveDate`.

---

# 23. Future Stock Movement Module

Once movement records are available:

```text
TransactionDate
Location
SKU
MovementType
Quantity
```

Movement types:

```text
Receipt
Sale
Transfer In
Transfer Out
Adjustment
Return
```

The platform can calculate:

```text
Stock In
Stock Out
Movement Frequency
No-Movement Items
Fast-Moving Items
Slow-Moving Items
```

---

# 24. Future Transfer Module

Warehouse analysis can evolve into:

```text
Source Location
Destination Location
SKU
Transfer Qty
Transfer Date
Transfer Status
```

Then the system can display:

```text
Pending Transfers
Transfer In
Transfer Out
Transfer Aging
Location Imbalance
Transfer Completion
```

---

# 25. Future Replenishment Intelligence

With inventory + sales + purchasing data, low-stock alerts can later become more intelligent.

Version 1:

```text
Qty <= User Threshold
=
Low Stock
```

Future:

```text
Average Daily Sales
×
Supplier Lead Time
+
Safety Stock
=
Reorder Point
```

Possible future:

```text
Current Qty:          20
Average Daily Sales:   4
Lead Time:             7 days
Safety Stock:         10

Reorder Point:
38 units

Status:
Replenishment Required
```

The Version 1 interface should therefore call its setting:

```text
Stock Alert Threshold
```

rather than hard-coding the concept of `Reorder Point`.

---

# 26. Configurable Business Rules

The application should use centralized settings.

Example:

```javascript
Settings = {
    inventory: {
        criticalStockThreshold: 3,
        lowStockThreshold: 10,
        agingDays: 365,
        surplusThreshold: 30
    },

    sales: {
        defaultPeriodDays: 30
    }
};
```

Settings should not be scattered throughout JavaScript files.

---

# 27. Local Settings Storage

Because the application is offline, user preferences may optionally be stored using:

```text
localStorage
```

Examples:

```text
Low Stock Threshold
Critical Threshold
Preferred Page Size
Default Location
Selected Theme
```

Inventory datasets themselves should not be permanently saved unless explicitly designed to do so.

---

# 28. Shared Alert Framework

Do not build warehouse alerts as a one-off implementation.

Create a generic alert engine.

Example categories:

```text
CRITICAL
WARNING
INFORMATION
```

Version 1:

```text
Negative Inventory
Out of Stock
Low Stock
Aging Inventory
```

Future:

```text
Sales Drop
Purchase Delay
High Returns
Late Delivery
Unusual Discount
Stockout Risk
Transfer Delay
```

---

# 29. Generic Alert Object

Concept:

```javascript
{
    module: "warehouse",
    level: "critical",
    type: "out_of_stock",
    title: "Out of Stock",
    message: "23 SKU-location combinations are out of stock.",
    count: 23
}
```

Future:

```javascript
{
    module: "sales",
    level: "warning",
    type: "sales_decline",
    title: "Sales Decline",
    message: "Sales decreased 18% versus the previous period."
}
```

The same UI can render both.

---

# 30. Notification Center

The header should eventually include:

```text
🔔 12
```

Clicking opens:

```text
NOTIFICATIONS

Warehouse
● 23 Out-of-Stock SKUs

Warehouse
⚠ 68 Low-Stock SKUs

Sales
⚠ Sales declined 12%

Purchasing
● 4 Purchase Orders overdue
```

For Version 1 this only contains warehouse alerts.

---

# 31. Data Dictionary Architecture

Do not hard-code all definitions only in table logic.

Create centralized metadata.

Concept:

```javascript
FieldDefinitions = {
    ItemSku: {
        type: "string",
        label: "SKU",
        dimension: "product",
        requiredFor: ["warehouse", "sales", "purchasing"]
    },

    BalanceQty: {
        type: "number",
        label: "Balance Quantity",
        module: "warehouse"
    }
};
```

This enables future schemas to be added cleanly.

---

# 32. Schema Versioning

Future input formats may change.

Therefore include schema definitions such as:

```text
Inventory Schema v1
Sales Schema v1
Purchase Schema v1
```

Avoid assuming every future Excel file will follow exactly the same format.

---

# 33. Column Mapping

The Data Center should eventually support manual column mapping.

Example:

```text
Detected Column       Platform Field

SKU_CODE             → ItemSku
ProductName          → ItemDescription
QTY                   → BalanceQty
Store                 → LocationCode
```

This significantly increases long-term versatility.

The first version can primarily rely on exact names from the existing data dictionary.

---

# 34. Dashboard Component Library

Create reusable UI elements:

```text
KPI Card
Alert Card
Chart Card
Data Table
Filter Dropdown
Search Input
Status Badge
Tab Control
Modal
Date Selector
File Upload
Empty State
Loading State
Error State
```

Do not create separate visual styles for each future module.

---

# 35. Professional Visual System

The design should remain consistent regardless of module.

Recommended layout:

```text
SIDEBAR
    +
TOP HEADER
    +
FILTER BAR
    +
MODULE WORKSPACE
```

Example:

```text
┌──────────────────────────────────────────────────────────────┐
│ Business Analytics Control                  🔔 4   Settings │
├───────────────┬──────────────────────────────────────────────┤
│ Overview      │                                              │
│               │ Warehouse Inventory                          │
│ Warehouse     │                                              │
│               │ [Location] [Brand] [Category]               │
│ Sales         │                                              │
│               │ KPI CARDS                                    │
│ Purchasing    │                                              │
│               │ ALERTS                                       │
│ Transfers     │                                              │
│               │ CHARTS                                       │
│ Vendors       │                                              │
│               │ TABLE                                        │
│ Data Center   │                                              │
│ Settings      │                                              │
└───────────────┴──────────────────────────────────────────────┘
```

---

# 36. Module Colors

Do not create dramatically different themes for every module.

Use one professional base system.

Accent indicators can vary slightly:

```text
Warehouse       Blue
Sales           Green
Purchasing      Purple
Transfers       Cyan
Critical Alert  Red
Warning         Amber
```

The platform should still look like one application.

---

# 37. Data Import Versatility

Future Data Center should support multiple files simultaneously.

Example:

```text
Inventory
Inventory_17Aug.xlsx

Sales
Sales_August.xlsx

Purchasing
PurchaseOrders.xlsx

Transfers
Transfers_August.xlsx
```

Each dataset should display:

```text
Filename
Rows
Date Range
Loaded Time
Status
```

---

# 38. Data Relationship Status

The system should report whether datasets can be linked successfully.

Example:

```text
DATA CONNECTION

Inventory ↔ Sales
✓ Connected using ItemSku

Inventory ↔ Location
✓ Connected using LocationCode

Inventory ↔ Purchasing
⚠ 24 SKUs could not be matched
```

This is important once multiple datasets are introduced.

---

# 39. Cross-Module Analysis

Future modules should be able to combine data.

Examples:

### Inventory + Sales

```text
Sales Velocity
Stock Cover
Sell Through
Slow-Moving Inventory
```

### Inventory + Purchasing

```text
Current Stock
Incoming Stock
Expected Stock Position
```

### Sales + Purchasing

```text
Demand vs Purchase Quantity
```

### Inventory + Sales + Purchasing

```text
Projected Availability
Replenishment Priority
```

---

# 40. Module Availability Detection

If a dataset is not loaded, the corresponding module should display an informative state.

Example:

```text
SALES ANALYSIS

Sales data has not been loaded.

Import a sales file from Data Center to enable this module.

[ Go to Data Center ]
```

No error should occur.

---

# 41. Warehouse Version 1 Must Remain Lightweight

Even with the expandable architecture, Version 1 should not become unnecessarily complicated.

Initial visible navigation:

```text
Overview
Warehouse
Data Center
Settings
```

Future modules can remain disabled internally.

The user should experience a simple warehouse system now while the code remains ready for expansion.

---

# 42. Recommended Version Roadmap

## Version 1 — Warehouse Control

```text
Inventory File Import
Inventory Overview
Low Stock
Out of Stock
Negative Stock
Aging Stock
Warehouse Analysis
Location Analysis
SKU Search
Stock Alerts
CSV Export
```

---

## Version 2 — Sales Analytics

```text
Sales File Import
Sales Dashboard
Daily / Weekly / Monthly Sales
Product Performance
Store Performance
Category Sales
Brand Sales
```

---

## Version 3 — Inventory + Sales Intelligence

```text
Sell Through
Stock Cover
Sales Velocity
Slow Moving Stock
Fast Moving Stock
Stockout Risk
Better Replenishment Alerts
```

---

## Version 4 — Purchasing

```text
Purchase Orders
Incoming Stock
Vendor Deliveries
Outstanding Orders
Expected Stock
```

---

## Version 5 — Transfers & Replenishment

```text
Stock Transfer Tracking
Location Stock Imbalance
Transfer Opportunities
Replenishment Planning
```

---

## Version 6 — Management Control Center

```text
Executive Overview
Inventory
Sales
Purchasing
Vendor
Location Performance
Operational Alerts
```

---

# 43. Recommended Product Naming

Since the platform may expand beyond warehouses, avoid naming the entire application:

```text
Warehouse Inventory Dashboard
```

Instead use a more versatile platform name.

Recommended:

# Operations Insight

Subtitle for Version 1:

> **Offline Warehouse Inventory Control**

Future:

> **Offline Business Operations Analytics**

Other suitable names:

```text
Operations Control
Business Operations Insight
Stock & Sales Control
Retail Operations Control
Inventory Intelligence
Operations Analytics Hub
```

Recommended structure:

```text
OPERATIONS INSIGHT

Warehouse
Offline Inventory Control
```

Later:

```text
OPERATIONS INSIGHT

Sales
Sales Performance Analytics
```

---

# 44. Critical Architectural Requirement

Do not create code like:

```javascript
function renderEverything() {
    // inventory logic
    // warehouse logic
    // charts
    // tables
    // sales later...
}
```

Instead:

```text
App
│
├── Core
│
├── Data Store
│
├── Filters
│
├── UI Components
│
├── Alerts
│
└── Modules
     ├── Warehouse
     ├── Sales
     ├── Purchasing
     └── Transfers
```

This is the most important technical requirement for future scalability.

---

# 45. Version 1 Acceptance Criteria — Versatility

In addition to the warehouse requirements, the first implementation should meet these architecture requirements:

- [ ] Warehouse logic is separated from core file-processing logic.
- [ ] File import component can be reused by future modules.
- [ ] Data is maintained in a centralized store.
- [ ] Inventory data has its own dataset namespace.
- [ ] Filters are reusable components.
- [ ] KPI cards are reusable components.
- [ ] Chart containers are reusable components.
- [ ] Tables are reusable components.
- [ ] Alert display is reusable.
- [ ] Business thresholds are maintained in centralized settings.
- [ ] Field definitions are maintained centrally.
- [ ] Navigation supports additional future modules.
- [ ] Hidden modules can be activated later without rebuilding navigation.
- [ ] Data Center can eventually manage multiple datasets.
- [ ] `ItemSku` is treated as the primary product-level integration key.
- [ ] `LocationCode` is treated as the primary location integration key.
- [ ] Warehouse analysis does not depend directly on HTML element IDs throughout business logic.
- [ ] UI rendering is separated from calculations.
- [ ] Business calculations are separated from file parsing.
- [ ] No future module should require rewriting the complete warehouse module.
- [ ] Application remains fully offline.

---

# 46. Final Design Principle

The project should be developed as:

```text
MODULAR BUSINESS PLATFORM
          ↓
WAREHOUSE MODULE FIRST
          ↓
SALES MODULE LATER
          ↓
PURCHASING / TRANSFERS
          ↓
CROSS-MODULE INTELLIGENCE
```

The Version 1 user should still experience:

```text
DROP INVENTORY FILE
        ↓
SEE WAREHOUSE STATUS
        ↓
IDENTIFY STOCK PROBLEMS
        ↓
TAKE ACTION
```

But technically, the application should already be prepared for:

```text
INVENTORY
+
SALES
+
PURCHASING
+
TRANSFERS
+
VENDORS
=
OPERATIONS INTELLIGENCE PLATFORM
```

The goal is therefore **not to build a large application immediately**.

The goal is to build a **small, professional warehouse application on top of an architecture that can grow into a complete offline operations analytics platform without requiring a full redesign later**.