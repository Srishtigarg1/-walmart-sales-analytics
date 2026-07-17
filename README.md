# Walmart Sales Intelligence Dashboard

End-to-end sales analysis on 10,000+ Walmart transactions built with Python, SQL, Pandas and Streamlit — styled with official Walmart brand colors.

---

## Dashboard Preview

### Overview
![Overview 1](images/Screenshot%202026-07-17%20215938.png)
![Overview 2](images/Screenshot%202026-07-17%20215952.png)

### Revenue Analysis
![Revenue 1](images/Screenshot%202026-07-17%20220009.png)
![Revenue 2](images/Screenshot%202026-07-17%20220023.png)

### Branch Intelligence
![Branches 1](images/Screenshot%202026-07-17%20220045.png)
![Branches 2](images/Screenshot%202026-07-17%20220104.png)

### Operational Analytics
![Operations 1](images/Screenshot%202026-07-17%20220116.png)
![Operations 2](images/Screenshot%202026-07-17%20220125.png)

### Profitability Intelligence
![Profitability 1](images/Screenshot%202026-07-17%20220141.png)
![Profitability 2](images/Screenshot%202026-07-17%20220224.png)
![Profitability 3](images/Screenshot%202026-07-17%20220234.png)

---

## Tools Used

| Tool | Purpose |
|---|---|
| Python | Core language |
| MySQL | 16 SQL queries — CTEs, Window Functions, CASE, YoY comparison |
| Pandas | Data cleaning and transformation |
| Streamlit | 5-page interactive dashboard |
| Plotly | Interactive charts, heatmaps, bubble charts |

---

## Dashboard Pages

| Page | What it shows |
|---|---|
| Overview | Revenue trends by category, daily revenue with 7-day moving average |
| Revenue | Payment method breakdown, category × payment mix analysis |
| Branch Intelligence | City-level drill-down with dynamic filter, branch performance table |
| Operations | Peak hour bar chart, shift revenue, category × hour demand heatmap |
| Profitability | Total profit by category, margin %, rating vs revenue scatter, bubble chart |

---

## Key Insights

- **Peak hours identified** — highest transaction volume concentrated in specific hours across 100 branches
- **Top category by profit margin** — identified using avg margin % analysis across 6 product categories  
- **YoY revenue comparison** — branches with largest revenue decline flagged using SQL CASE + year filtering
- **Demand heatmap** — reveals which product categories are busiest at which hours of the day

---

## Project Structure
