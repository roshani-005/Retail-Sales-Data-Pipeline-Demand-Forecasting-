# Materials Management & Supply Planning Analytics

## Materials aligned project

This project is designed around the Materials Management / Supply Chain / Manufacturing Operations responsibilities in the supplied Eaton Intern–Materials job description. SQL is the core analytics layer.

### Project story

> Built a materials planning analytics pipeline that integrates material demand, inventory, purchase orders and supplier performance into a SQL warehouse. It identifies replenishment needs using safety-stock/reorder-point logic, measures demand–supply gaps, supplier OTIF and quality, quantifies inventory cash tied up, and produces a planning KPI scorecard. A time-aware ML model adds a 30-day demand forecast.

## JD → project mapping

| JD area | Project evidence |
|---|---|
| Material Management | Material master, inventory, PO and demand flow |
| Demand & Supply | SQL demand–supply matching and shortage detection |
| Inventory Management | Inventory health, days of cover, stockout exposure |
| Inventory Optimization | Excess-inventory/cash opportunity analysis |
| Safety Stock | Demand-variability and lead-time based calculation |
| Reorder Point | Lead-time demand + safety stock and reorder flag |
| Schedule / recovery | PO due-vs-receipt analysis and delayed supplier metrics |
| KPI reporting | Reusable SQL KPI queries and scorecard |
| Cost / Cash | Inventory valuation and excess-stock cash |
| Quality | Supplier rejection-rate analysis |
| Service | Availability / stockout exposure |
| Continuity | Supply coverage and shortage flags |
| Lean improvement | Excess inventory and cash-tied-up opportunities |
| Python | ETL, data-quality automation and demand forecasting |
| ERP / SAP | **No hands-on SAP claim**; warehouse is ERP-inspired |

## Architecture

```text
Synthetic manufacturing source data
          ↓
     Python ETL + DQ
          ↓
      SQLite warehouse
          ↓
  SQL materials analytics
  ├─ Inventory health
  ├─ Safety stock / ROP
  ├─ Replenishment flags
  ├─ Demand–supply gaps
  ├─ Supplier OTIF / quality
  ├─ Cost & cash
  ├─ Service / continuity
  └─ Lean excess-stock opportunities
          ↓
  30-day demand forecast
          ↓
 KPI / forecast artifacts
```

## SQL concepts demonstrated

- CTEs
- `JOIN`s
- `GROUP BY` and aggregations
- `CASE WHEN` business rules
- date arithmetic
- analytical calculations
- KPI and exception reporting

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python pipeline/run_all.py
pytest tests/ -v
python sql/run_queries.py
```

## Interview positioning

Do **not** claim SAP/ERP hands-on experience based on this project. Say the database is **ERP-inspired** and demonstrates the material-management data flow. The strongest skills demonstrated are SQL materials analytics and Python automation.

## Resume bullets

- Built a SQL-driven materials planning analytics pipeline integrating demand, inventory, purchase orders and supplier data; automated replenishment, demand–supply gap and material-health reporting.
- Implemented safety-stock, reorder-point, days-of-cover and service/continuity KPIs using SQL, identifying shortage and excess-inventory opportunities tied to cash.
- Developed supplier OTIF and rejection-rate analytics and a time-aware 30-day demand forecast using Python/XGBoost, with automated data-quality checks and CI tests.
