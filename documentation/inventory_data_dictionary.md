# Data Dictionary

This data dictionary describes the inventory, product, pricing, classification, vendor, and stock-related columns contained in the dataset.

## Column Definitions

| Column Name | Description | Example / Meaning |
|---|---|---|
| **BalanceDate** | Date on which the inventory balance or stock quantity was recorded. | `2026-08-17` |
| **LocationCode** | Unique code identifying the warehouse, store, or inventory location where the stock is held. | `WHS01`, `T10SP` |
| **HQLocationCode** | Code representing the headquarters, parent location, or main reporting location associated with the inventory location. | `WHS01`, `MGA001` |
| **LocationDescription** | Name or description of the warehouse/store represented by `LocationCode`. | `LX PANTOS WAREHOUSE`, `TOPTEN10 SUNWAY PYRAMID` |
| **ItemCode** | Base product/item identifier. Products with different colors or sizes may share the same ItemCode. | `MBF2JJ1002` |
| **ItemDescription** | General product description or product name. | `SHORT SLEEVE WOVEN T-SHIRTS` |
| **X-AxisCode** | Code representing the first product variation dimension, which appears to be color in this dataset. | `CR` |
| **X-AxisDescription** | Description of the first variation dimension, such as product color. | `CREAM` |
| **Y-AxisCode** | Code representing the second product variation dimension, which appears to be size in this dataset. | `M100`, `M105` |
| **Y-AxisDescription** | Description of the second variation dimension, such as garment size. | `L`, `XL` |
| **ItemSku** | Unique Stock Keeping Unit identifying a specific product variation, such as Item + Color + Size. | `MBF2JJ1002CR100` |
| **ItemBarcode** | Barcode assigned to the specific product/SKU for scanning and identification. | `MBF2JJ1002CR100` |
| **BalanceQty** | Quantity of stock available at the specified location and balance date. | `46`, `6`, `28`, `10` |
| **RecentCost** | Most recently recorded cost per unit for the item. | `32.06817797` |
| **LatestWeightedAverageCost** | Latest calculated weighted-average unit cost based on inventory purchase or receipt history. | `32.06817797` |
| **WeightedAverageCost** | Weighted-average cost per unit used for inventory valuation. | `32.06817797` |
| **TotalWeightedAverageCost** | Total inventory value based on `BalanceQty × WeightedAverageCost`. | `1475.136186` |
| **BaseUnitPrice** | Standard/base selling price per unit before applicable discounts or price adjustments. | `99.90` |
| **DiscountGroupCode** | Discount group originally assigned to the item for pricing or promotional rules. | `N` |
| **CurrentDiscountGroupCode** | Discount group currently applicable to the item. | `N` |
| **CurrentUnitPrice** | Current selling price per unit after applicable pricing rules or adjustments. | `99.90` |
| **BrandCode** | Unique code identifying the product brand. | `T10` |
| **BrandDescription** | Name of the product brand. | `TOPTEN10` |
| **GroupCode** | High-level product group classification code. | `APP` |
| **GroupDescription** | Description of the high-level product group. | `APPAREL` |
| **SubGroupCode** | Code representing a secondary classification below the main product group. | Blank in sample |
| **SubGroupDescription** | Description of the secondary product group. | Blank in sample |
| **CategoryCode** | Product category classification code. | `TOP` |
| **CategoryDescription** | Description/name of the product category. | `TOP` |
| **SubCategoryCode** | Product subcategory classification code. | `WOVN` |
| **SubCategoryDescription** | Description/name of the product subcategory. | `WOVEN` |
| **UnitMeasureCode** | Unit of measurement used to record inventory quantity. | `PCS` = Pieces |
| **DepartmentCode** | Code identifying the department or merchandise division responsible for the item. | `ADLT` |
| **DepartmentDescription** | Description/name of the department or merchandise division. | `ADULT` |
| **SeasonCode** | Code identifying the merchandise season associated with the item. | `SUM` |
| **SeasonDescription** | Description/name of the merchandise season. | `Summer` |
| **MaterialCode** | Merchandise/material classification code. In the sample data, it appears to represent a target gender or merchandise segment rather than literal fabric composition. | `MEN` |
| **MaterialDescription** | Description corresponding to the MaterialCode. | `MEN` |
| **VendorCode** | Unique identifier assigned to the supplier/vendor of the product. | `4000-S101` |
| **VendorName** | Name of the supplier/vendor providing the item. | `SHINSUNG TONGSANG CO., LTD` |
| **FirstGoodsReceiveDate** | Date on which the item was first received into inventory. | `2025-12-17` |
| **LastGoodsReceiveDate** | Most recent date on which the item was received into inventory. | `2025-12-17` |
| **ItemUDField1** | User-defined/custom item attribute field configured by the source system. Exact business meaning requires confirmation from the system owner. | `F` |
| **ItemUDField2** | Additional user-defined/custom item attribute field. Exact meaning is not identifiable from the provided sample. | Blank |
| **ItemUDField3** | Additional user-defined/custom item attribute field for organization-specific item information. | Blank |

## Product Hierarchy

Based on the sample data, the product hierarchy can be interpreted approximately as:

```text
Brand
└── Group
    └── Category
        └── Subcategory
            └── Item
                └── Color
                    └── Size
                        └── SKU
```

Example:

```text
TOPTEN10
└── APPAREL
    └── TOP
        └── WOVEN
            └── SHORT SLEEVE WOVEN T-SHIRTS
                └── CREAM
                    └── L
                        └── MBF2JJ1002CR100
```

## Important Field Relationships

### ItemCode vs ItemSku

- `ItemCode` identifies the general product.
- `ItemSku` identifies the specific sellable variation of the product.
- Different colors and sizes may share the same `ItemCode` but have different `ItemSku` values.

Example:

```text
ItemCode: MBF2JJ1002
ItemSku:  MBF2JJ1002CR100
Color:    CREAM
Size:     L
```

## Inventory Valuation

`TotalWeightedAverageCost` can be interpreted as:

```text
TotalWeightedAverageCost = BalanceQty × WeightedAverageCost
```

Example:

```text
BalanceQty = 46
WeightedAverageCost = 32.06817797

46 × 32.06817797 ≈ 1475.136186
```

This represents the inventory cost value for the SKU at the specified location.

## Recommended Columns for Further Analysis

The following fields are especially useful for inventory and retail analysis:

- `BalanceDate`
- `LocationCode`
- `LocationDescription`
- `ItemCode`
- `ItemSku`
- `ItemDescription`
- `X-AxisDescription`
- `Y-AxisDescription`
- `BalanceQty`
- `WeightedAverageCost`
- `TotalWeightedAverageCost`
- `BaseUnitPrice`
- `CurrentUnitPrice`
- `BrandDescription`
- `GroupDescription`
- `CategoryDescription`
- `SubCategoryDescription`
- `DepartmentDescription`
- `SeasonDescription`
- `VendorCode`
- `VendorName`
- `FirstGoodsReceiveDate`
- `LastGoodsReceiveDate`

## Potential Analysis Use Cases

This dataset can support analysis such as:

1. Inventory stock level by store, warehouse, SKU, brand, or category.
2. Inventory valuation using weighted average cost.
3. Stock distribution between warehouse and retail stores.
4. Color and size availability analysis.
5. Brand, category, and subcategory stock comparison.
6. Vendor contribution and supplier analysis.
7. Inventory aging based on goods receipt dates.
8. Potential retail value using `BalanceQty × CurrentUnitPrice`.
9. Gross margin estimation using selling price and weighted average cost.
10. Slow-moving or excess-stock identification when historical balance data is available.

## Notes

- Meanings for `ItemUDField1`, `ItemUDField2`, and `ItemUDField3` should be confirmed with the source system or business owner.
- `MaterialCode` and `MaterialDescription` should also be validated because the provided sample uses `MEN`, which appears more like a gender or merchandise segment than a material type.
- X-axis and Y-axis meanings are inferred from the sample data and should be verified if other product categories use these fields differently.
