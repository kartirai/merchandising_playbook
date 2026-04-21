import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="India Smartphone Market Intelligence",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.metric-card {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 16px 20px;
    border: 1px solid #e9ecef;
}
.metric-val { font-size: 28px; font-weight: 600; color: #1a1a2e; }
.metric-label { font-size: 12px; color: #6c757d; margin-bottom: 4px; }
.metric-sub { font-size: 11px; color: #adb5bd; margin-top: 2px; }
.gap-badge { background: #fff0f0; color: #c0392b; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }
.ok-badge { background: #f0fff4; color: #27ae60; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }
.section-header { font-size: 13px; font-weight: 600; color: #6c757d; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    xl = pd.ExcelFile(file)
    sheets = {}

    # Scraped Data
    df = pd.read_excel(file, sheet_name="Scraped Data", header=1)
    df = df.dropna(how="all")
    df.columns = df.columns.str.strip()
    df["Brand"] = df["Brand"].str.strip()
    df["CC Status"] = df["CC Status"].str.strip()
    df["Positioning"] = df["Positioning"].str.strip()
    df["Status"] = df["Status"].str.strip()
    df["Platform"] = df["Platform"].str.strip()
    brand_map = {"REDMI": "Xiaomi", "Redmi": "Xiaomi", "XIAOMI": "Xiaomi",
                 "IQOO": "iQOO", "Motorola": "MOTOROLA", "Poco": "POCO"}
    df["Brand"] = df["Brand"].replace(brand_map)
    df["Price_clean"] = pd.to_numeric(df["Price (scraping tool)"], errors="coerce")
    df["Discount_pct"] = df["Discount"].str.extract(r"(\d+)").astype(float)
    df["Volume"] = pd.to_numeric(df["Volume ( Review *5)"], errors="coerce").fillna(0)
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Review Count"] = pd.to_numeric(df["Review Count"], errors="coerce")
    sheets["scraped"] = df

    # Top Brands
    tb = pd.read_excel(file, sheet_name="Top Brands", header=None)
    tb = tb.dropna(how="all")
    sheets["top_brands"] = tb

    # Upcoming Models
    up = pd.read_excel(file, sheet_name="Upcoming Models", header=0)
    up = up.dropna(how="all")
    up.columns = ["_", "Brand", "Model", "Release Date"]
    up = up.dropna(subset=["Brand"])
    up["Brand"] = up["Brand"].str.strip()
    up["Release Date"] = up["Release Date"].fillna("TBC").astype(str)
    up.loc[up["Release Date"].str.contains("2026-04"), "Release Date"] = "Apr 2026"
    up.loc[up["Release Date"].str.contains("2026-05"), "Release Date"] = "May 2026"
    up.loc[up["Release Date"].str.contains("2026-06"), "Release Date"] = "Jun 2026"
    up.loc[up["Release Date"].str.contains("2026-07"), "Release Date"] = "Jul 2026"
    up.loc[up["Release Date"].str.contains("2026-10"), "Release Date"] = "Oct 2026"
    up.loc[up["Release Date"].str.contains("NaT"), "Release Date"] = "TBC"
    sheets["upcoming"] = up

    return sheets


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📱 Market Intelligence")
    st.markdown("---")
    uploaded = st.file_uploader("Upload your Excel playbook", type=["xlsx"])
    if uploaded:
        st.success("File loaded!")
    else:
        st.info("Upload your `Smartphone_marketResearch` Excel file to begin.")

    st.markdown("---")
    st.markdown("**Data definitions**")
    st.markdown("""
- **Volume** = Rating × 5 (Flipkart proxy)
- **Current series** = Released 2025+
- **Latest launch** = Released 2026
- **CC Status** = Listed on company ecommerce channel
- Source: IDC, Counterpoint, Flipkart, Amazon
    """)

if not uploaded:
    st.markdown("## 📱 India Smartphone Market Intelligence Dashboard")
    st.markdown("Upload your Excel playbook from the sidebar to get started.")
    st.stop()

data = load_data(uploaded)
df = data["scraped"]
upcoming = data["upcoming"]

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📊 Market Overview", "🏷️ Brand Landscape", "🔍 Product Explorer", "📋 Report Card", "🚀 Upcoming Launches"])


# ════════════════════════════════════════════════════════════════
# TAB 1 — MARKET OVERVIEW
# ════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("### Market overview — India 2026")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-label">Market size (est. 2026)</div><div class="metric-val">153 Mn</div><div class="metric-sub">units shipped</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-label">Online share</div><div class="metric-val">43%</div><div class="metric-sub">vs 57% offline</div></div>', unsafe_allow_html=True)
    with c3:
        top_brand = df.groupby("Brand")["Volume"].sum().idxmax()
        st.markdown(f'<div class="metric-card"><div class="metric-label">Top brand by volume (platform)</div><div class="metric-val">{top_brand}</div><div class="metric-sub">highest review-proxy volume</div></div>', unsafe_allow_html=True)
    with c4:
        total_skus = len(df)
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total SKUs tracked</div><div class="metric-val">{total_skus:,}</div><div class="metric-sub">across Flipkart & Amazon</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Market share — IDC vs Counterpoint 2025</div>', unsafe_allow_html=True)
        brands_share = pd.DataFrame({
            "Brand": ["vivo", "Samsung", "OPPO", "Realme", "Apple", "Xiaomi", "Motorola"],
            "IDC": [19.3, 14.1, 13.3, 9.5, 9.8, 8.5, 7.5],
            "Counterpoint": [20.0, 15.0, 14.0, None, None, 12.0, None]
        })
        fig = go.Figure()
        fig.add_bar(name="IDC", x=brands_share["Brand"], y=brands_share["IDC"],
                    marker_color="#3266ad", text=brands_share["IDC"].apply(lambda x: f"{x}%" if pd.notna(x) else ""), textposition="outside")
        fig.add_bar(name="Counterpoint", x=brands_share["Brand"], y=brands_share["Counterpoint"],
                    marker_color="#27ae60", text=brands_share["Counterpoint"].apply(lambda x: f"{x}%" if pd.notna(x) else "N/A"), textposition="outside")
        fig.update_layout(barmode="group", height=320, margin=dict(t=20, b=20),
                          legend=dict(orientation="h", y=1.1), yaxis_title="Volume share (%)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Channel split — online vs offline</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=["Online", "Offline"], values=[43, 57],
            marker_colors=["#3266ad", "#a8d8ea"],
            hole=0.5, textinfo="label+percent"
        ))
        fig2.update_layout(height=320, margin=dict(t=20, b=20), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Platform volume by brand (review proxy)</div>', unsafe_allow_html=True)
    vol_df = df.groupby("Brand")["Volume"].sum().reset_index().sort_values("Volume", ascending=False).head(12)
    vol_df["Volume_M"] = (vol_df["Volume"] / 1e6).round(2)
    fig3 = px.bar(vol_df, x="Brand", y="Volume_M", text="Volume_M",
                  color="Volume_M", color_continuous_scale=["#cfe2ff", "#3266ad"],
                  labels={"Volume_M": "Volume (Mn units proxy)"})
    fig3.update_traces(texttemplate="%{text:.1f}M", textposition="outside")
    fig3.update_layout(height=320, margin=dict(t=20, b=20), coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# TAB 2 — BRAND LANDSCAPE
# ════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("### Brand landscape")

    brand_summary = df.groupby("Brand").agg(
        SKUs=("Product Name", "count"),
        Avg_Price=("Price_clean", "mean"),
        Avg_Rating=("Rating", "mean"),
        Total_Volume=("Volume", "sum"),
        Avg_Discount=("Discount_pct", "mean")
    ).reset_index()
    brand_summary = brand_summary[brand_summary["SKUs"] >= 5].sort_values("Total_Volume", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Positioning mix by brand (SKU count)</div>', unsafe_allow_html=True)
        pos_df = df[df["Brand"].isin(brand_summary["Brand"])].groupby(["Brand", "Positioning"])["Product Name"].count().reset_index()
        pos_df.columns = ["Brand", "Positioning", "Count"]
        color_map = {"Entry Level": "#639922", "Mid Premium": "#EF9F27", "Premium": "#7F77DD"}
        fig4 = px.bar(pos_df, x="Brand", y="Count", color="Positioning",
                      color_discrete_map=color_map, barmode="stack",
                      category_orders={"Positioning": ["Entry Level", "Mid Premium", "Premium"]})
        fig4.update_layout(height=320, margin=dict(t=20, b=20),
                           legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Avg price vs avg rating — bubble = volume</div>', unsafe_allow_html=True)
        bub = brand_summary[brand_summary["Avg_Price"].notna()].copy()
        bub["Vol_scaled"] = (bub["Total_Volume"] / bub["Total_Volume"].max() * 60).clip(lower=5)
        fig5 = px.scatter(bub, x="Avg_Price", y="Avg_Rating", size="Vol_scaled",
                          text="Brand", color="Brand",
                          labels={"Avg_Price": "Avg price (₹)", "Avg_Rating": "Avg rating"},
                          size_max=60)
        fig5.update_traces(textposition="top center", textfont_size=10)
        fig5.update_layout(height=320, margin=dict(t=20, b=20), showlegend=False,
                           xaxis_tickformat="₹,.0f")
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Brand summary table</div>', unsafe_allow_html=True)

    display = brand_summary.copy()
    display["Avg_Price"] = display["Avg_Price"].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "—")
    display["Avg_Rating"] = display["Avg_Rating"].round(2)
    display["Total_Volume"] = display["Total_Volume"].apply(lambda x: f"{x/1e6:.1f}M")
    display["Avg_Discount"] = display["Avg_Discount"].apply(lambda x: f"{x:.0f}%" if pd.notna(x) else "—")
    display.columns = ["Brand", "SKUs", "Avg price", "Avg rating", "Platform volume", "Avg discount"]
    st.dataframe(display, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════
# TAB 3 — PRODUCT EXPLORER
# ════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("### Product explorer")

    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    with col1:
        search = st.text_input("Search product name", placeholder="e.g. vivo T4x, Samsung Galaxy...")
    with col2:
        brands_list = ["All"] + sorted(df["Brand"].dropna().unique().tolist())
        sel_brand = st.selectbox("Brand", brands_list)
    with col3:
        pos_list = ["All"] + sorted(df["Positioning"].dropna().unique().tolist())
        sel_pos = st.selectbox("Segment", pos_list)
    with col4:
        plat_list = ["All"] + sorted(df["Platform"].dropna().unique().tolist())
        sel_plat = st.selectbox("Platform", plat_list)
    with col5:
        status_list = ["All"] + sorted(df["Status"].dropna().unique().tolist())
        sel_status = st.selectbox("Series status", status_list)

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["Product Name"].str.contains(search, case=False, na=False)]
    if sel_brand != "All":
        filtered = filtered[filtered["Brand"] == sel_brand]
    if sel_pos != "All":
        filtered = filtered[filtered["Positioning"] == sel_pos]
    if sel_plat != "All":
        filtered = filtered[filtered["Platform"] == sel_plat]
    if sel_status != "All":
        filtered = filtered[filtered["Status"] == sel_status]

    st.caption(f"Showing {len(filtered):,} of {len(df):,} products")

    show_cols = ["Product Name", "Brand", "Price_clean", "Discount", "Rating",
                 "Positioning", "Platform", "Status", "Top sellers", "CC Status"]
    display_df = filtered[show_cols].copy()
    display_df.columns = ["Product", "Brand", "Price (₹)", "Discount", "Rating",
                          "Segment", "Platform", "Status", "Top seller", "CC Status"]
    display_df["Price (₹)"] = display_df["Price (₹)"].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "—")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=500
    )


# ════════════════════════════════════════════════════════════════
# TAB 4 — REPORT CARD (Merch team)
# ════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("### Report card — CC gap analysis")
    st.caption("Shows which models are available in the market but not listed on the company ecommerce channel (CC)")

    brand_filter = st.selectbox(
        "Select brand to analyse",
        options=sorted(df["Brand"].dropna().unique().tolist()),
        index=sorted(df["Brand"].dropna().unique().tolist()).index("Vivo") if "Vivo" in df["Brand"].values else 0
    )

    brand_df = df[df["Brand"] == brand_filter].copy()
    active_df = brand_df[brand_df["Status"].isin(["Current series", "Latest launch"])]

    c1, c2, c3, c4 = st.columns(4)
    total_v = len(active_df)
    gap_v = len(active_df[active_df["CC Status"] == "No"])
    ok_v = len(active_df[active_df["CC Status"] == "Yes"])
    top_v = len(brand_df[brand_df["Top sellers"].astype(str).str.strip() == "Yes"])

    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Active variants</div><div class="metric-val">{total_v}</div><div class="metric-sub">current & latest series</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Not on CC</div><div class="metric-val" style="color:#c0392b">{gap_v}</div><div class="metric-sub">ecommerce gap (active series)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Listed on CC</div><div class="metric-val" style="color:#27ae60">{ok_v}</div><div class="metric-sub">active on channel</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Top sellers</div><div class="metric-val">{top_v}</div><div class="metric-sub">flagged as top sellers</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">CC status by series</div>', unsafe_allow_html=True)
        if "Series" in brand_df.columns:
            series_cc = brand_df.groupby(["Series", "CC Status"])["Product Name"].count().reset_index()
            series_cc.columns = ["Series", "CC Status", "Count"]
            series_cc = series_cc[series_cc["Series"].notna() & (series_cc["Series"] != "nan")]
            if not series_cc.empty:
                fig6 = px.bar(series_cc, x="Series", y="Count", color="CC Status",
                              color_discrete_map={"Yes": "#27ae60", "No": "#e74c3c"},
                              barmode="group", text="Count")
                fig6.update_traces(textposition="outside")
                fig6.update_layout(height=300, margin=dict(t=20, b=20),
                                   legend=dict(orientation="h", y=1.1))
                st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Positioning breakdown (CC gap vs listed)</div>', unsafe_allow_html=True)
        pos_cc = brand_df.groupby(["Positioning", "CC Status"])["Product Name"].count().reset_index()
        pos_cc.columns = ["Positioning", "CC Status", "Count"]
        fig7 = px.bar(pos_cc, x="Positioning", y="Count", color="CC Status",
                      color_discrete_map={"Yes": "#27ae60", "No": "#e74c3c"},
                      barmode="group", text="Count")
        fig7.update_traces(textposition="outside")
        fig7.update_layout(height=300, margin=dict(t=20, b=20),
                           legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Full CC gap detail — all variants</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        gap_only = st.checkbox("Show only CC gaps (not listed)", value=False)
    with col_f2:
        active_only = st.checkbox("Current & latest series only (exclude old phones)", value=True)

    show_df = brand_df.copy()
    if active_only:
        show_df = show_df[show_df["Status"].isin(["Current series", "Latest launch"])]
    if gap_only:
        show_df = show_df[show_df["CC Status"] == "No"]

    rc_cols = ["Series", "Model", "Product Name", "Price_clean", "Discount", "Rating",
               "Volume", "Status", "Top sellers", "CC Status"]
    rc_cols = [c for c in rc_cols if c in show_df.columns]
    rc_display = show_df[rc_cols].copy()
    rc_display["Price_clean"] = rc_display["Price_clean"].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "—")
    rc_display["Volume"] = rc_display["Volume"].apply(lambda x: f"{x/1e3:.0f}K" if x > 0 else "—")
    rc_display.columns = [c.replace("Price_clean", "Price (₹)").replace("Volume", "Vol proxy") for c in rc_display.columns]

    def highlight_cc(row):
        if row.get("CC Status") == "No":
            return ["background-color: #fff5f5"] * len(row)
        elif row.get("CC Status") == "Yes":
            return ["background-color: #f0fff4"] * len(row)
        return [""] * len(row)

    st.dataframe(
        rc_display.style.apply(highlight_cc, axis=1),
        use_container_width=True,
        hide_index=True,
        height=450
    )

    st.markdown("---")
    st.markdown('<div class="section-header">Top 10 products by volume — with CC status</div>', unsafe_allow_html=True)

    # Deduplicate by model name (same model appears in multiple colour/storage variants)
    top_df = (
        brand_df[["Product Name", "Price_clean", "Rating", "Volume", "Positioning", "CC Status", "Top sellers"]]
        .drop_duplicates(subset=["Product Name"])
        .sort_values("Volume", ascending=False)
        .head(10)
    )

    if not top_df.empty:
        top_df = top_df.copy()
        top_df["Top sellers"] = top_df["Top sellers"].apply(lambda x: "★" if x == "Yes" else "")
        top_df["Price_clean"] = top_df["Price_clean"].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "—")
        top_df["Volume"] = top_df["Volume"].apply(lambda x: f"{x/1e3:.0f}K" if x > 0 else "—")
        top_df.columns = ["Product", "Price", "Rating", "Volume", "Segment", "CC Status", "Top seller flag"]
        st.dataframe(top_df.style.apply(highlight_cc, axis=1), use_container_width=True, hide_index=True)
    else:
        st.info(f"No products found for {brand_filter}.")


# ════════════════════════════════════════════════════════════════
# TAB 5 — UPCOMING LAUNCHES
# ════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("### Upcoming launches — 2026 pipeline")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total tracked</div><div class="metric-val">{len(upcoming)}</div><div class="metric-sub">upcoming models</div></div>', unsafe_allow_html=True)
    with c2:
        apr = len(upcoming[upcoming["Release Date"] == "Apr 2026"])
        st.markdown(f'<div class="metric-card"><div class="metric-label">April 2026</div><div class="metric-val">{apr}</div><div class="metric-sub">expected launches</div></div>', unsafe_allow_html=True)
    with c3:
        tbc = len(upcoming[upcoming["Release Date"] == "TBC"])
        st.markdown(f'<div class="metric-card"><div class="metric-label">Date TBC</div><div class="metric-val">{tbc}</div><div class="metric-sub">unconfirmed timeline</div></div>', unsafe_allow_html=True)
    with c4:
        most_brand = upcoming["Brand"].value_counts().idxmax()
        most_count = upcoming["Brand"].value_counts().max()
        st.markdown(f'<div class="metric-card"><div class="metric-label">Largest pipeline</div><div class="metric-val">{most_brand}</div><div class="metric-sub">{most_count} models upcoming</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Pipeline count by brand</div>', unsafe_allow_html=True)
        up_count = upcoming["Brand"].value_counts().reset_index()
        up_count.columns = ["Brand", "Count"]
        fig8 = px.bar(up_count, x="Count", y="Brand", orientation="h", text="Count",
                      color="Count", color_continuous_scale=["#d4e6f1", "#2e86de"])
        fig8.update_traces(textposition="outside")
        fig8.update_layout(height=380, margin=dict(t=20, b=20),
                           coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig8, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Release timeline distribution</div>', unsafe_allow_html=True)
        timeline_order = ["Apr 2026", "May 2026", "Jun 2026", "Jul 2026",
                          "Oct 2026", "Late 2026", "Jan/Feb 2027", "2027", "TBC"]
        tl = upcoming["Release Date"].value_counts().reset_index()
        tl.columns = ["Month", "Count"]
        tl["Month"] = pd.Categorical(tl["Month"], categories=timeline_order, ordered=True)
        tl = tl.sort_values("Month")
        fig9 = px.bar(tl, x="Month", y="Count", text="Count",
                      color="Count", color_continuous_scale=["#d5f5e3", "#1e8449"])
        fig9.update_traces(textposition="outside")
        fig9.update_layout(height=380, margin=dict(t=20, b=20), coloraxis_showscale=False)
        st.plotly_chart(fig9, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">All upcoming models</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        up_brand_filter = st.selectbox("Filter by brand", ["All"] + sorted(upcoming["Brand"].unique().tolist()))
    with col2:
        up_date_filter = st.selectbox("Filter by release", ["All"] + [d for d in ["Apr 2026","May 2026","Jun 2026","Jul 2026","Oct 2026","Late 2026","Jan/Feb 2027","2027","TBC"] if d in upcoming["Release Date"].values])

    up_filtered = upcoming.copy()
    if up_brand_filter != "All":
        up_filtered = up_filtered[up_filtered["Brand"] == up_brand_filter]
    if up_date_filter != "All":
        up_filtered = up_filtered[up_filtered["Release Date"] == up_date_filter]

    st.dataframe(
        up_filtered[["Brand", "Model", "Release Date"]].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        height=400
    )
