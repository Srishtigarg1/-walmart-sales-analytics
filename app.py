import streamlit as st
import pandas as pd

import base64

st.set_page_config(
    page_title="Walmart Sales Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        min-width: 280px !important;
        width: 280px !important;
        transform: none !important;
        display: block !important;
        visibility: visible !important;
    }
    section[data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 280px !important;
        width: 280px !important;
        transform: none !important;
        margin-left: 0px !important;
    }
    button[data-testid="collapsedControl"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Official Walmart brand colors (2025 refresh)
WMT_TRUE_BLUE = "#0071CE"
WMT_SPARK_YELLOW = "#FFC220"
WMT_DARK_BLUE = "#041F41"
WMT_SKY_BLUE = "#A9DDF7"
WMT_LIGHT_BLUE = "#4DBDF5"
WMT_WHITE = "#FFFFFF"

SPARK_PNG = "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"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * {{ font-family: 'Inter', sans-serif !important; }}

    /* Base */
    .stApp {{ background-color: {WMT_DARK_BLUE}; color: #e8f0fa; }}
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #031529 0%, {WMT_DARK_BLUE} 60%, #031529 100%);
        border-right: 1px solid rgba(0,113,206,0.25);
    }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding: 1.5rem 2rem; }}

    /* Topbar accent */
    .stApp::before {{
        content: '';
        display: block;
        height: 3px;
        background: linear-gradient(90deg, {WMT_TRUE_BLUE} 0%, {WMT_LIGHT_BLUE} 50%, {WMT_SPARK_YELLOW} 100%);
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 9999;
    }}

    /* Typography */
    h1 {{ font-size: 1.6rem !important; font-weight: 800 !important; color: {WMT_WHITE} !important; letter-spacing: -0.5px !important; }}
    h3 {{ font-size: 0.68rem !important; font-weight: 700 !important; color: {WMT_LIGHT_BLUE} !important;
          text-transform: uppercase !important; letter-spacing: 2px !important; margin-bottom: 0.8rem !important; }}

    /* Metric cards — official Walmart blue */
    [data-testid="metric-container"] {{
        background: linear-gradient(135deg, rgba(0,113,206,0.15) 0%, rgba(4,31,65,0.8) 100%);
        border: 1px solid rgba(0,113,206,0.3);
        border-top: 2px solid {WMT_TRUE_BLUE};
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
    }}
    [data-testid="stMetricLabel"] {{ color: {WMT_LIGHT_BLUE} !important; font-size: 0.7rem !important;
        text-transform: uppercase !important; letter-spacing: 1.2px !important; font-weight: 600 !important; }}
    [data-testid="stMetricValue"] {{ color: {WMT_WHITE} !important; font-size: 1.65rem !important; font-weight: 800 !important; }}

    /* Divider */
    hr {{ border: none; border-top: 1px solid rgba(0,113,206,0.2); margin: 1.2rem 0; }}

    /* Insight boxes */
    .insight-box {{
        background: rgba(0,113,206,0.08);
        border: 1px solid rgba(0,113,206,0.25);
        border-left: 3px solid {WMT_TRUE_BLUE};
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin: 0.6rem 0;
        font-size: 0.82rem;
        color: {WMT_SKY_BLUE};
        line-height: 1.6;
    }}
    .yellow-box {{
        background: rgba(255,194,32,0.06);
        border: 1px solid rgba(255,194,32,0.2);
        border-left: 3px solid {WMT_SPARK_YELLOW};
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin: 0.6rem 0;
        font-size: 0.82rem;
        color: {WMT_SKY_BLUE};
        line-height: 1.6;
    }}

    /* Sidebar logo area */
    .wmt-brand {{
        display: flex; align-items: center; gap: 12px;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid rgba(0,113,206,0.25);
        margin-bottom: 1.2rem;
    }}
    .wmt-name {{ color: {WMT_WHITE}; font-size: 1.1rem; font-weight: 800; letter-spacing: -0.3px; line-height:1.1; }}
    .wmt-sub {{ color: {WMT_SPARK_YELLOW}; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }}

    /* Stat pills */
    .pill-row {{ display: flex; gap: 6px; flex-wrap: wrap; margin: 0.4rem 0; }}
    .pill {{
        background: rgba(0,113,206,0.12);
        border: 1px solid rgba(0,113,206,0.2);
        border-radius: 20px;
        padding: 0.22rem 0.7rem;
        font-size: 0.72rem;
        color: {WMT_SKY_BLUE};
    }}
    .pill b {{ color: {WMT_SPARK_YELLOW}; }}

    /* Section divider */
    .sec-div {{
        display: flex; align-items: center; gap: 10px;
        margin: 1.2rem 0 0.8rem 0;
    }}
    .sec-dot {{ width: 5px; height: 5px; border-radius: 50%; background: {WMT_SPARK_YELLOW}; flex-shrink:0; }}
    .sec-lbl {{ font-size: 0.68rem; font-weight: 700; color: {WMT_LIGHT_BLUE}; text-transform: uppercase; letter-spacing: 2px; }}
    .sec-line {{ flex: 1; height: 1px; background: rgba(0,113,206,0.2); }}

    /* Selectbox */
    .stSelectbox > div > div {{
        background: rgba(0,113,206,0.1) !important;
        border: 1px solid rgba(0,113,206,0.3) !important;
        color: {WMT_WHITE} !important;
        border-radius: 8px !important;
    }}

    /* Radio */
    .stRadio div[role="radiogroup"] label {{
        color: {WMT_SKY_BLUE} !important;
        font-size: 0.82rem !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }}
    .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(0,113,206,0.15) !important;
        color: {WMT_WHITE} !important;
    }}

    /* Dataframe */
    .stDataFrame {{ border: 1px solid rgba(0,113,206,0.25) !important; border-radius: 8px !important; }}

    /* Nav buttons */
    div[data-testid="stSidebar"] div[data-testid="stButton"] > button {{
        background: transparent !important;
        border: none !important;
        border-left: 3px solid transparent !important;
        border-radius: 6px !important;
        color: #4dbdf5 !important;
        text-align: left !important;
        width: 100% !important;
        padding: 0.5rem 0.9rem !important;
        font-size: 0.83rem !important;
        font-weight: 400 !important;
        margin-bottom: 3px !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
    }}
    div[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {{
        background: rgba(0,113,206,0.15) !important;
        border-left: 3px solid #0071CE !important;
        color: #ffffff !important;
    }}
    div[data-testid="stSidebar"] div[data-testid="stButton"] > button:focus:not(:active) {{
        background: rgba(0,113,206,0.2) !important;
        border-left: 3px solid #0071CE !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# Chart theme
CT = {
    "paper_bgcolor": "rgba(4,31,65,0.6)",
    "plot_bgcolor": "rgba(4,31,65,0.6)",
    "font": {"color": WMT_SKY_BLUE, "size": 11, "family": "Inter"},
    "xaxis": {"gridcolor": "rgba(0,113,206,0.12)", "linecolor": "rgba(0,113,206,0.2)",
               "tickfont": {"color": WMT_LIGHT_BLUE}},
    "yaxis": {"gridcolor": "rgba(0,113,206,0.12)", "linecolor": "rgba(0,113,206,0.2)",
               "tickfont": {"color": WMT_LIGHT_BLUE}},
    "margin": {"t": 35, "b": 30, "l": 40, "r": 20}
}

@st.cache_data
def load_data():
    df = pd.read_csv('walmart.csv')
    df['unit_price'] = df['unit_price'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['revenue'] = df['unit_price'] * df['quantity']
    df['profit'] = df['revenue'] * df['profit_margin']
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.hour
    def rb(r):
        if r < 5: return 'Poor'
        elif r < 7: return 'Average'
        elif r < 9: return 'Good'
        else: return 'Excellent'
    df['rating_band'] = df['rating'].apply(rb)
    df['shift'] = pd.cut(df['hour'], bins=[-1,11,16,23], labels=['Morning','Afternoon','Evening'])
    return df

df = load_data()

def section(label):
    st.markdown(f'<div class="sec-div"><div class="sec-dot"></div><div class="sec-lbl">{label}</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────
with st.sidebar:
    st.markdown(f'''
    <div class="wmt-brand">
        <img src="data:image/png;base64,{SPARK_PNG}" width="40" style="filter:drop-shadow(0 0 8px rgba(255,194,32,0.5));">
        <div>
            <div class="wmt-name">Walmart</div>
            <div class="wmt-sub">Sales Intelligence</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Overview"

    nav_items = [("📊", "Overview"), ("💰", "Revenue"), ("🏪", "Branches"), ("⏰", "Operations"), ("📈", "Profitability")]

    for icon, name in nav_items:
        active = st.session_state.nav_page == name
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.nav_page = name
            st.rerun()

    page = st.session_state.nav_page

    st.markdown("<hr>", unsafe_allow_html=True)
    total_rev = df['revenue'].sum()
    total_profit = df['profit'].sum()
    margin = total_profit / total_rev * 100
    st.markdown(f'''
    <p style="color:{WMT_LIGHT_BLUE};font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin-bottom:0.6rem;">Live Summary</p>
    <div class="pill-row">
        <div class="pill">Txns <b>{len(df):,}</b></div>
        <div class="pill">Branches <b>{df["Branch"].nunique()}</b></div>
    </div>
    <div class="pill-row">
        <div class="pill">Revenue <b>${total_rev:,.0f}</b></div>
        <div class="pill">Margin <b>{margin:.1f}%</b></div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<p style="color:{WMT_LIGHT_BLUE};font-size:0.68rem;text-transform:uppercase;letter-spacing:1.2px;font-weight:700;margin-bottom:0.4rem;">Period</p><p style="color:{WMT_SKY_BLUE};font-size:0.78rem;">{df["date"].min().strftime("%b %d, %Y")} – {df["date"].max().strftime("%b %d, %Y")}</p>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<p style="color:{WMT_LIGHT_BLUE};font-size:0.72rem;">Built by <span style="color:{WMT_SPARK_YELLOW};font-weight:600;">Srishti Garg</span> · TIET Patiala</p>', unsafe_allow_html=True)


# ── PAGE 1: OVERVIEW ─────────────────────────
if page == "Overview":
    st.title("Sales Overview")
    st.markdown(f'<p style="color:{WMT_LIGHT_BLUE};font-size:0.83rem;margin-top:-0.4rem;margin-bottom:1rem;">End-to-end performance snapshot across all Walmart branches and categories</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
    c2.metric("Total Transactions", f"{len(df):,}")
    c3.metric("Avg Customer Rating", f"{df['rating'].mean():.2f} / 10")
    c4.metric("Active Branches", df['Branch'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)
    section("Category Performance")
    col1, col2 = st.columns(2)

    with col1:
        cat = df.groupby('category')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
        fig = px.bar(cat, x='revenue', y='category', orientation='h',
                     color='revenue',
                     color_continuous_scale=[[0, WMT_DARK_BLUE],[0.5, WMT_TRUE_BLUE],[1, WMT_LIGHT_BLUE]])
        fig.update_layout(**CT, title="Revenue by Category", title_font_color=WMT_WHITE,
                          showlegend=False, coloraxis_showscale=False,
                          xaxis_title="Revenue ($)", yaxis_title="")
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        cat_txn = df.groupby('category').size().reset_index()
        cat_txn.columns = ['category', 'count']
        cat_txn = cat_txn.sort_values('count', ascending=True)
        fig2 = px.bar(cat_txn, x='count', y='category', orientation='h',
                      color='count',
                      color_continuous_scale=[[0, WMT_DARK_BLUE],[0.5, WMT_TRUE_BLUE],[1, WMT_SPARK_YELLOW]])
        fig2.update_layout(**CT, title="Transactions by Category", title_font_color=WMT_WHITE,
                           showlegend=False, coloraxis_showscale=False,
                           xaxis_title="Transactions", yaxis_title="")
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

    section("Daily Revenue Trend")
    daily = df.groupby('date')['revenue'].sum().reset_index()
    daily['7d_avg'] = daily['revenue'].rolling(7).mean()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=daily['date'], y=daily['revenue'],
                               name='Daily Revenue',
                               line=dict(color=WMT_TRUE_BLUE, width=1.5),
                               fill='tozeroy', fillcolor='rgba(0,113,206,0.1)'))
    fig3.add_trace(go.Scatter(x=daily['date'], y=daily['7d_avg'],
                               name='7-Day Avg',
                               line=dict(color=WMT_SPARK_YELLOW, width=2.5, dash='dot')))
    fig3.update_layout(**CT, title="Daily Revenue with 7-Day Moving Average",
                        title_font_color=WMT_WHITE,
                        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=WMT_SKY_BLUE)),
                        xaxis_title="", yaxis_title="Revenue ($)")
    st.plotly_chart(fig3, use_container_width=True)


# ── PAGE 2: REVENUE ───────────────────────────
elif page == "Revenue":
    st.title("Revenue Analysis")
    st.markdown(f'<p style="color:{WMT_LIGHT_BLUE};font-size:0.83rem;margin-top:-0.4rem;margin-bottom:1rem;">Payment breakdown, spending patterns, and category revenue mix</p>', unsafe_allow_html=True)

    pay = df.groupby('payment_method').agg(
        transactions=('payment_method', 'count'),
        spend=('revenue', 'sum')
    ).reset_index()

    section("Payment Method Breakdown")
    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure(go.Pie(
            labels=pay['payment_method'], values=pay['transactions'], hole=0.6,
            marker=dict(colors=[WMT_TRUE_BLUE, WMT_LIGHT_BLUE, WMT_SPARK_YELLOW],
                        line=dict(color=WMT_DARK_BLUE, width=3)),
            textfont=dict(color=WMT_SKY_BLUE, size=11)
        ))
        fig.update_layout(
            paper_bgcolor='rgba(4,31,65,0.6)', plot_bgcolor='rgba(4,31,65,0.6)',
            font=dict(color=WMT_SKY_BLUE, family='Inter'),
            title="Transactions by Payment Method", title_font_color=WMT_WHITE,
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=WMT_SKY_BLUE)),
            margin=dict(t=40, b=20, l=20, r=20),
            annotations=[dict(text=f'<b>{len(df):,}</b><br>Total', x=0.5, y=0.5,
                               font=dict(size=14, color=WMT_WHITE, family='Inter'), showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(pay, x='payment_method', y='spend', color='payment_method',
                      color_discrete_sequence=[WMT_TRUE_BLUE, WMT_LIGHT_BLUE, WMT_SPARK_YELLOW],
                      text='spend')
        fig2.update_traces(texttemplate='$%{{text:,.0f}}', textposition='outside',
                           textfont=dict(color=WMT_SKY_BLUE, size=10), marker_line_width=0)
        fig2.update_layout(**CT, title="Total Spend by Payment Method", title_font_color=WMT_WHITE,
                           showlegend=False, xaxis_title="", yaxis_title="Spend ($)")
        st.plotly_chart(fig2, use_container_width=True)

    section("Category × Payment Mix")
    avg_txn = df.groupby(['category', 'payment_method'])['revenue'].mean().reset_index()
    avg_txn.columns = ['category', 'payment_method', 'avg_revenue']
    fig3 = px.bar(avg_txn, x='category', y='avg_revenue', color='payment_method',
                  barmode='group',
                  color_discrete_sequence=[WMT_TRUE_BLUE, WMT_LIGHT_BLUE, WMT_SPARK_YELLOW])
    fig3.update_layout(**CT, title="Avg Transaction Value by Category & Payment Method",
                        title_font_color=WMT_WHITE, xaxis_title="", yaxis_title="Avg Revenue ($)",
                        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=WMT_SKY_BLUE)))
    fig3.update_traces(marker_line_width=0)
    st.plotly_chart(fig3, use_container_width=True)

    top_cat = df.groupby('category')['revenue'].sum().idxmax()
    top_pay = df.groupby('payment_method').size().idxmax()
    st.markdown(f'<div class="insight-box"><strong style="color:{WMT_SPARK_YELLOW};">{top_cat}</strong> drives the highest total revenue. <strong style="color:{WMT_SPARK_YELLOW};">{top_pay}</strong> is the dominant payment method — signalling strong digital payment adoption.</div>', unsafe_allow_html=True)


# ── PAGE 3: BRANCHES ─────────────────────────
elif page == "Branches":
    st.title("Branch Intelligence")
    st.markdown(f'<p style="color:{WMT_LIGHT_BLUE};font-size:0.83rem;margin-top:-0.4rem;margin-bottom:1rem;">City-level drill-down into branch performance and ratings</p>', unsafe_allow_html=True)

    col_sel, _ = st.columns([1, 3])
    with col_sel:
        selected_city = st.selectbox("Select City", sorted(df['City'].unique().tolist()))

    city_df = df[df['City'] == selected_city]
    city_rev = city_df['revenue'].sum()
    share = city_rev / df['revenue'].sum() * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("City Revenue", f"${city_rev:,.0f}")
    c2.metric("Revenue Share", f"{share:.1f}%")
    c3.metric("Transactions", f"{len(city_df):,}")
    c4.metric("Avg Rating", f"{city_df['rating'].mean():.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Category Performance")
    col1, col2 = st.columns(2)

    with col1:
        city_cat = city_df.groupby('category')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
        fig = px.bar(city_cat, x='revenue', y='category', orientation='h',
                     color='revenue',
                     color_continuous_scale=[[0, WMT_DARK_BLUE],[0.5, WMT_TRUE_BLUE],[1, WMT_SKY_BLUE]])
        fig.update_layout(**CT, title=f"Revenue by Category — {selected_city}",
                           title_font_color=WMT_WHITE,
                           showlegend=False, coloraxis_showscale=False,
                           xaxis_title="Revenue ($)", yaxis_title="")
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        cr = city_df.groupby(['category','rating_band']).size().reset_index()
        cr.columns = ['category','rating_band','count']
        fig2 = px.bar(cr, x='category', y='count', color='rating_band', barmode='stack',
                      color_discrete_map={'Poor':'#e05555','Average':WMT_SPARK_YELLOW,
                                          'Good':WMT_TRUE_BLUE,'Excellent':WMT_LIGHT_BLUE})
        fig2.update_layout(**CT, title="Rating Distribution",
                           title_font_color=WMT_WHITE,
                           legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=WMT_SKY_BLUE)),
                           xaxis_title="", yaxis_title="Count")
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

    section("Branch Performance Table")
    bd = city_df.groupby(['Branch','category']).agg(
        Revenue=('revenue','sum'), Avg_Rating=('rating','mean'),
        Transactions=('Branch','count'), Profit=('profit','sum')
    ).reset_index()
    bd['Revenue'] = bd['Revenue'].round(2)
    bd['Avg_Rating'] = bd['Avg_Rating'].round(2)
    bd['Profit'] = bd['Profit'].round(2)
    st.dataframe(bd.sort_values('Revenue', ascending=False), use_container_width=True, hide_index=True)


# ── PAGE 4: OPERATIONS ───────────────────────
elif page == "Operations":
    st.title("Operational Analytics")
    st.markdown(f'<p style="color:{WMT_LIGHT_BLUE};font-size:0.83rem;margin-top:-0.4rem;margin-bottom:1rem;">Peak hours, shift patterns, and demand heatmap</p>', unsafe_allow_html=True)

    shift_data = df.groupby('shift', observed=True).agg(
        transactions=('revenue','count'), revenue=('revenue','sum')
    ).reset_index()

    peak_hour = df.groupby('hour').size().idxmax()
    peak_shift = shift_data.loc[shift_data['revenue'].idxmax(),'shift']

    c1, c2, c3 = st.columns(3)
    c1.metric("Peak Hour", f"{peak_hour}:00")
    c2.metric("Top Revenue Shift", str(peak_shift))
    c3.metric("Busiest Category", df.groupby('category').size().idxmax())

    st.markdown("<br>", unsafe_allow_html=True)
    section("Hourly Pattern")
    col1, col2 = st.columns(2)

    with col1:
        hd = df.groupby('hour').size().reset_index()
        hd.columns = ['hour','transactions']
        colors = [WMT_SPARK_YELLOW if h == peak_hour else WMT_TRUE_BLUE for h in hd['hour']]
        fig = go.Figure(go.Bar(x=hd['hour'], y=hd['transactions'],
                                marker=dict(color=colors, line=dict(width=0)),
                                text=hd['transactions'], textposition='outside',
                                textfont=dict(color=WMT_SKY_BLUE, size=9)))
        fig.update_layout(**CT, title="Transactions by Hour (Yellow = Peak)",
                           title_font_color=WMT_WHITE,
                           xaxis_title="Hour of Day", yaxis_title="Transactions", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        sc = [WMT_TRUE_BLUE, WMT_LIGHT_BLUE, WMT_SPARK_YELLOW]
        fig2 = go.Figure()
        for i, row in shift_data.iterrows():
            fig2.add_trace(go.Bar(name=str(row['shift']), x=[str(row['shift'])],
                                   y=[row['revenue']], marker=dict(color=sc[i], line=dict(width=0)),
                                   text=[f"${row['revenue']:,.0f}"], textposition='outside',
                                   textfont=dict(color=WMT_SKY_BLUE, size=10)))
        fig2.update_layout(**CT, title="Revenue by Shift", title_font_color=WMT_WHITE,
                            showlegend=False, xaxis_title="", yaxis_title="Revenue ($)")
        st.plotly_chart(fig2, use_container_width=True)

    section("Category × Hour Demand Heatmap")
    pivot = df.groupby(['category','hour'])['revenue'].sum().reset_index().pivot(
        index='category', columns='hour', values='revenue').fillna(0)
    fig3 = px.imshow(pivot,
                      color_continuous_scale=[[0, WMT_DARK_BLUE],[0.4, WMT_TRUE_BLUE],[0.7, WMT_LIGHT_BLUE],[1, WMT_SPARK_YELLOW]],
                      aspect='auto', labels=dict(color="Revenue ($)"))
    fig3.update_layout(paper_bgcolor='rgba(4,31,65,0.6)', plot_bgcolor='rgba(4,31,65,0.6)',
                        font=dict(color=WMT_SKY_BLUE, family='Inter'),
                        title="Revenue Intensity — Category vs Hour",
                        title_font_color=WMT_WHITE,
                        xaxis_title="Hour of Day", yaxis_title="",
                        margin=dict(t=40, b=40, l=120, r=20),
                        coloraxis_colorbar=dict(tickfont=dict(color=WMT_SKY_BLUE),
                                                title=dict(text="Revenue", font=dict(color=WMT_LIGHT_BLUE))))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f'<div class="yellow-box">Peak demand occurs at <strong style="color:{WMT_SPARK_YELLOW};">{peak_hour}:00</strong>. The <strong style="color:{WMT_SPARK_YELLOW};">{peak_shift}</strong> shift drives the highest revenue — inventory restocking and staffing should be front-loaded around this window.</div>', unsafe_allow_html=True)


# ── PAGE 5: PROFITABILITY ─────────────────────
elif page == "Profitability":
    st.title("Profitability Intelligence")
    st.markdown(f'<p style="color:{WMT_LIGHT_BLUE};font-size:0.83rem;margin-top:-0.4rem;margin-bottom:1rem;">Margin analysis, profit drivers, and revenue-rating correlation</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Profit", f"${df['profit'].sum():,.0f}")
    c2.metric("Overall Margin", f"{df['profit_margin'].mean()*100:.1f}%")
    c3.metric("Top Margin Category", df.groupby('category')['profit_margin'].mean().idxmax())
    c4.metric("Avg Profit / Txn", f"${df['profit'].mean():.1f}")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Profit by Category")
    col1, col2 = st.columns(2)

    with col1:
        pc = df.groupby('category')['profit'].sum().reset_index().sort_values('profit', ascending=True)
        fig = px.bar(pc, x='profit', y='category', orientation='h', color='profit',
                     color_continuous_scale=[[0, WMT_DARK_BLUE],[0.5, WMT_TRUE_BLUE],[1,'#7dd8ff']])
        fig.update_layout(**CT, title="Total Profit by Category", title_font_color=WMT_WHITE,
                           showlegend=False, coloraxis_showscale=False,
                           xaxis_title="Total Profit ($)", yaxis_title="")
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        mc = df.groupby('category')['profit_margin'].mean().reset_index()
        mc['pct'] = (mc['profit_margin']*100).round(1)
        mc = mc.sort_values('pct', ascending=True)
        fig2 = px.bar(mc, x='pct', y='category', orientation='h', color='pct',
                      color_continuous_scale=[[0, WMT_DARK_BLUE],[0.5, WMT_TRUE_BLUE],[1, WMT_SPARK_YELLOW]],
                      text='pct')
        fig2.update_traces(texttemplate='%{{text:.1f}}%', textposition='outside',
                            textfont=dict(color=WMT_SKY_BLUE, size=10), marker_line_width=0)
        fig2.update_layout(**CT, title="Avg Profit Margin % by Category", title_font_color=WMT_WHITE,
                            showlegend=False, coloraxis_showscale=False,
                            xaxis_title="Avg Margin (%)", yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    section("Revenue vs Rating")
    scatter = df.groupby('rating').agg(avg_revenue=('revenue','mean'), count=('revenue','count')).reset_index()
    fig3 = px.scatter(scatter, x='rating', y='avg_revenue', size='count', color='avg_revenue',
                       color_continuous_scale=[[0, WMT_TRUE_BLUE],[1, WMT_SPARK_YELLOW]],
                       trendline='ols', trendline_color_override=WMT_SPARK_YELLOW)
    fig3.update_layout(**CT, title="Does Higher Rating Drive More Revenue?", title_font_color=WMT_WHITE,
                        xaxis_title="Customer Rating", yaxis_title="Avg Revenue ($)",
                        coloraxis_showscale=False, showlegend=False)
    fig3.update_traces(marker=dict(line=dict(width=0)))
    st.plotly_chart(fig3, use_container_width=True)

    section("Revenue vs Margin vs Profit — Bubble View")
    bubble = df.groupby('category').agg(
        total_revenue=('revenue','sum'), avg_margin=('profit_margin','mean'), total_profit=('profit','sum')
    ).reset_index()
    bubble['avg_margin_pct'] = (bubble['avg_margin']*100).round(1)
    fig4 = px.scatter(bubble, x='total_revenue', y='avg_margin_pct',
                       size='total_profit', text='category', color='total_profit',
                       color_continuous_scale=[[0, WMT_TRUE_BLUE],[1, WMT_SPARK_YELLOW]])
    fig4.update_traces(textposition='top center',
                        textfont=dict(color=WMT_WHITE, size=10),
                        marker=dict(line=dict(width=1, color=WMT_DARK_BLUE)))
    fig4.update_layout(**CT, title="Revenue vs Margin vs Profit (Bubble = Total Profit)",
                        title_font_color=WMT_WHITE, coloraxis_showscale=False, showlegend=False,
                        xaxis_title="Total Revenue ($)", yaxis_title="Avg Profit Margin (%)")
    st.plotly_chart(fig4, use_container_width=True)

    top_margin = df.groupby('category')['profit_margin'].mean().idxmax()
    top_profit = df.groupby('category')['profit'].sum().idxmax()
    st.markdown(f'<div class="insight-box"><strong style="color:{WMT_SPARK_YELLOW};">{top_margin}</strong> has the highest avg profit margin. <strong style="color:{WMT_SPARK_YELLOW};">{top_profit}</strong> generates the most absolute profit — prioritising these in restocking and promotions can significantly improve net margins.</div>', unsafe_allow_html=True)
