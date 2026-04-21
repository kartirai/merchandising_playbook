# 📱 India Smartphone Market Intelligence Dashboard

A dynamic Streamlit dashboard that reads your Excel playbook and auto-generates
interactive charts, brand analysis, product explorer, and CC gap report.

## Setup (one time)

### 1. Install Python
Download from https://python.org (version 3.9 or higher)

### 2. Install dependencies
Open Terminal (Mac) or Command Prompt (Windows), navigate to this folder, and run:
```
pip install -r requirements.txt
```

### 3. Run the dashboard
```
streamlit run app.py
```
Your browser will open automatically at http://localhost:8501

## How to use

1. Run `streamlit run app.py`
2. In the sidebar, click **Browse files** and upload your Excel playbook
3. The dashboard loads instantly — all 5 tabs are populated from your data
4. Next time your data changes, just re-upload the new Excel file

## What the dashboard reads from your Excel

| Sheet | What it powers |
|---|---|
| `Scraped Data` | Everything — brand landscape, product explorer, report card |
| `Top Brands` | IDC / Counterpoint share chart in Market Overview |
| `Upcoming Models` | Upcoming Launches tab |

## Adding new data

Just update your `Scraped Data` sheet and re-upload. The dashboard handles:
- New brands automatically added to all filters
- New CC Status values in Report Card
- New positioning segments
- New platforms (Flipkart/Amazon/etc.)

**Important:** Keep these column names exactly as-is in your Excel:
- `Brand`, `Product Name`, `CC Status`, `Positioning`, `Platform`
- `Status`, `Rating`, `Price (scraping tool)`, `Discount`, `Volume ( Review *5)`
- `Top sellers`, `Series`, `Model`

## Deploy online (share with team)

1. Create a free account at https://streamlit.io/cloud
2. Push this folder to a GitHub repository
3. Connect the repo on Streamlit Cloud → your team gets a shareable URL

No server costs. Free for public repos.
