# top10-html-analysis

Static, browser-based inventory analysis dashboard.

## Live dashboard

[Open the inventory analysis dashboard](https://edric-kaw.github.io/top10-html-analysis/)

## Public GitHub Pages build

Generate a public-safe `index.html` with no embedded inventory records:

```powershell
python scripts/build_public_dashboard.py
```

Visitors can load an `.xlsx` or `.csv` file from **Data Center**. The selected
file is processed locally in their browser and is not uploaded or persisted.

`operations-insight.html` is the private generated dashboard with embedded
inventory data and remains excluded from Git by `.gitignore`.
