# Walmart Sales Intelligence Dashboard

End-to-end sales analysis on 10,000+ Walmart transactions using SQL, Python, Pandas and Streamlit.

## Live Dashboard
[Coming soon — deploying on Streamlit Cloud]

## Tools Used
- Python, Pandas
- MySQL (16 SQL queries — CTEs, Window Functions, CASE, YoY)
- Streamlit (interactive 5-page dashboard)
- Plotly (interactive charts)

## Dashboard Pages
1. **Overview** — Revenue trends, category performance, 7-day moving average
2. **Revenue** — Payment method breakdown, category × payment mix
3. **Branches** — City-level drill-down with dynamic filter
4. **Operations** — Peak hour analysis, shift revenue, category × hour heatmap
5. **Profitability** — Profit margins, bubble chart, rating vs revenue correlation

## Key Insights
- Identified peak transaction hours across 100 branches
- Found top-performing product categories by profit margin
- Analysed YoY revenue decline by branch
- Built heatmap showing category demand by hour of day

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author
Srishti Garg | B.Tech ECE | TIET Patiala
