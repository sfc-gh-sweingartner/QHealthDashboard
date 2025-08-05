import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
from datetime import datetime, timedelta

# Import custom modules
from utils.snowflake_conn import ensure_connection, execute_query
from utils.viz_components import (
    create_metric_card, create_kpi_dashboard, create_geographic_map,
    create_hierarchy_sunburst, create_provider_performance_chart,
    create_trend_analysis, display_data_table, create_performance_monitor
)
from utils.queries import get_query

# Page configuration
st.set_page_config(
    page_title="Q.CheckUp Lite - Medical Device Analytics",
    page_icon="🩺",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #333;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .filter-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def load_checkup_lite_data(conn):
    """Load all Q.CheckUp Lite data with performance monitoring"""
    start_time = time.time()
    
    try:
        with st.spinner("🔄 Loading Q.CheckUp Lite analytics..."):
            
            # Load overview KPIs
            overview_df = execute_query(conn, get_query('checkup_lite', 'overview_kpis'))
            
            # Load province performance
            province_df = execute_query(conn, get_query('checkup_lite', 'province_performance'))
            
            # Load provider analysis
            provider_df = execute_query(conn, get_query('checkup_lite', 'provider_analysis'))
            
            # Load product hierarchy
            hierarchy_df = execute_query(conn, get_query('checkup_lite', 'product_hierarchy'))
            
            # Load monthly trends
            trends_df = execute_query(conn, get_query('checkup_lite', 'monthly_trends'))
            
            # Load high-value claims
            high_value_df = execute_query(conn, get_query('checkup_lite', 'high_value_claims'))
            
            load_time = time.time() - start_time
            create_performance_monitor(load_time, target_time=3.0)
            
            return {
                'overview': overview_df,
                'provinces': province_df,
                'providers': provider_df,
                'hierarchy': hierarchy_df,
                'trends': trends_df,
                'high_value': high_value_df,
                'load_time': load_time
            }
    
    except Exception as e:
        st.error(f"Error loading Q.CheckUp Lite data: {str(e)}")
        return None

def create_overview_section(data):
    """Create overview KPI section"""
    st.markdown('<h2 class="section-header">📊 Overview Dashboard</h2>', unsafe_allow_html=True)
    
    if data['overview'].empty:
        st.warning("No overview data available")
        return
    
    overview = data['overview'].iloc[0]
    
    # Create KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            "Total Claims", 
            f"{overview['TOTAL_CLAIMS']:,.0f}",
            "Medical device claims processed"
        )
    
    with col2:
        create_metric_card(
            "Unique Patients", 
            f"{overview['UNIQUE_PATIENTS']:,.0f}",
            "Patients served across SA"
        )
    
    with col3:
        create_metric_card(
            "Total Claimed", 
            f"R{overview['TOTAL_CLAIM_AMOUNT']:,.0f}",
            f"Avg: R{overview['AVG_CLAIM_AMOUNT']:,.0f} per claim"
        )
    
    with col4:
        approval_rate = (overview['TOTAL_PAID_AMOUNT'] / overview['TOTAL_CLAIM_AMOUNT']) * 100
        create_metric_card(
            "Approval Rate", 
            f"{approval_rate:.1f}%",
            f"R{overview['TOTAL_PAID_AMOUNT']:,.0f} paid"
        )

def create_geographic_analysis(data):
    """Create geographic analysis section"""
    st.markdown('<h2 class="section-header">🗺️ Geographic Distribution</h2>', unsafe_allow_html=True)
    
    if data['provinces'].empty:
        st.warning("No province data available")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Province performance chart
        fig = px.bar(
            data['provinces'],
            x='PROVINCE',
            y='TOTAL_CLAIMS',
            color='TOTAL_PAID',
            title="Claims by Province",
            labels={'TOTAL_CLAIMS': 'Total Claims', 'TOTAL_PAID': 'Total Paid (R)'},
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top provinces by volume
        top_provinces = data['provinces'].head(5)
        st.subheader("🏆 Top 5 Provinces")
        for _, row in top_provinces.iterrows():
            st.metric(
                row['PROVINCE'],
                f"{row['TOTAL_CLAIMS']:,.0f}",
                f"R{row['TOTAL_PAID']:,.0f}"
            )
    
    # Geographic insights
    st.markdown("""
    <div class="insight-box">
        <h4>🔍 Geographic Insights</h4>
        <ul>
            <li><strong>Urban Concentration:</strong> Gauteng and Western Cape lead in claim volumes</li>
            <li><strong>Access Gaps:</strong> Rural provinces show lower per-capita utilization</li>
            <li><strong>Cost Optimization:</strong> Northern provinces show higher average claim values</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def create_provider_analysis(data):
    """Create provider performance analysis"""
    st.markdown('<h2 class="section-header">🏥 Provider Performance</h2>', unsafe_allow_html=True)
    
    if data['providers'].empty:
        st.warning("No provider data available")
        return
    
    # Provider type analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Claims by provider category
        category_summary = data['providers'].groupby('PROVIDER_CATEGORY').agg({
            'TOTAL_CLAIMS': 'sum',
            'TOTAL_PAID': 'sum',
            'UNIQUE_PATIENTS': 'sum'
        }).reset_index()
        
        fig = px.pie(
            category_summary,
            values='TOTAL_CLAIMS',
            names='PROVIDER_CATEGORY',
            title="Claims Distribution by Provider Type"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Approval rate by provider type
        category_summary['approval_rate'] = (category_summary['TOTAL_PAID'] / 
                                           category_summary['TOTAL_CLAIMS']) * 100
        
        fig = px.bar(
            category_summary,
            x='PROVIDER_CATEGORY',
            y='approval_rate',
            title="Approval Rate by Provider Category",
            color='approval_rate',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top performers table
    st.subheader("🌟 Top Performing Providers")
    top_providers = data['providers'].head(20)[
        ['PROVIDER_NAME', 'PROVIDER_CATEGORY', 'PROVINCE', 'TOTAL_CLAIMS', 
         'TOTAL_PAID', 'AVG_CLAIM_AMOUNT', 'APPROVAL_RATE']
    ]
    st.dataframe(top_providers, use_container_width=True)

def create_product_analysis(data):
    """Create product hierarchy analysis"""
    st.markdown('<h2 class="section-header">🧬 Product Analysis</h2>', unsafe_allow_html=True)
    
    if data['hierarchy'].empty:
        st.warning("No product hierarchy data available")
        return
    
    # Product category performance
    level_1_summary = data['hierarchy'].groupby('LEVEL_1').agg({
        'TOTAL_CLAIMS': 'sum',
        'TOTAL_CLAIMED': 'sum',
        'TOTAL_PAID': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Claims by product category with improved Snowflake compatibility
        fig = px.treemap(
            level_1_summary,
            path=['LEVEL_1'],
            values='TOTAL_CLAIMS',
            title="Claims by Product Category",
            color='TOTAL_PAID',
            color_continuous_scale='Viridis',  # Better color scale for Snowflake
            labels={'TOTAL_PAID': 'Total Paid (R)', 'TOTAL_CLAIMS': 'Total Claims'}
        )
        fig.update_traces(
            textinfo="label+value+percent entry",
            textfont_size=12,
            marker=dict(
                colorbar=dict(title="Total Paid (R)"),
                line=dict(width=2, color='white')  # Add borders for better definition
            )
        )
        fig.update_layout(
            height=500,
            font=dict(size=10),
            margin=dict(t=50, l=25, r=25, b=25)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top product categories
        level_1_summary = level_1_summary.sort_values('TOTAL_CLAIMS', ascending=False)
        st.subheader("📈 Product Categories by Volume")
        
        for _, row in level_1_summary.head(10).iterrows():
            st.metric(
                row['LEVEL_1'],
                f"{row['TOTAL_CLAIMS']:,.0f}",
                f"R{row['TOTAL_PAID']:,.0f}"
            )
    
    # Product insights
    st.markdown("""
    <div class="insight-box">
        <h4>💡 Product Insights</h4>
        <ul>
            <li><strong>Wound Management:</strong> Highest volume category - focus for cost optimization</li>
            <li><strong>Orthopedics:</strong> High-value procedures - monitor for fraud patterns</li>
            <li><strong>Sutures:</strong> Consistent demand - potential for generic alternatives</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def create_trends_analysis(data):
    """Create trends and patterns analysis"""
    st.markdown('<h2 class="section-header">📈 Trends & Patterns</h2>', unsafe_allow_html=True)
    
    if data['trends'].empty:
        st.warning("No trends data available")
        return
    
    # Monthly trends chart
    fig = create_trend_analysis(
        data['trends'], 
        'MONTH', 
        'TOTAL_CLAIMS',
        title="Monthly Claims Volume Trend"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Claims vs Payments correlation
        fig = px.scatter(
            data['trends'],
            x='TOTAL_CLAIMS',
            y='TOTAL_PAID',
            title="Claims Volume vs Payments Correlation",
            trendline="ols"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average claim value trend
        fig = px.line(
            data['trends'],
            x='MONTH',
            y='AVG_CLAIM_AMOUNT',
            title="Average Claim Value Trend",
            markers=True
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def create_risk_analysis(data):
    """Create risk and fraud analysis"""
    st.markdown('<h2 class="section-header">⚠️ Risk Analysis</h2>', unsafe_allow_html=True)
    
    if data['high_value'].empty:
        st.warning("No high-value claims data available")
        return
    
    # Risk categories distribution
    risk_summary = data['high_value']['RISK_CATEGORY'].value_counts().reset_index()
    risk_summary.columns = ['Risk Category', 'Count']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            risk_summary,
            values='Count',
            names='Risk Category',
            title="High-Value Claims by Risk Category",
            color_discrete_map={
                'Very High': '#dc3545',
                'High': '#fd7e14', 
                'Medium': '#ffc107',
                'Normal': '#28a745'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # High-value claims by province
        province_risk = data['high_value'].groupby('PROVINCE_DESCR').agg({
            'TOTAL_CLAIM_AMOUNT': ['count', 'sum', 'mean']
        }).round(2)
        province_risk.columns = ['High Value Claims', 'Total Amount', 'Avg Amount']
        province_risk = province_risk.reset_index()
        
        fig = px.bar(
            province_risk,
            x='PROVINCE_DESCR',
            y='High Value Claims',
            title="High-Value Claims by Province",
            color='Avg Amount',
            color_continuous_scale='Reds'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk alerts table
    st.subheader("🚨 Risk Alerts - High-Value Claims")
    risk_table = data['high_value'][
        ['PROVIDER_NAME', 'PROVINCE_DESCR', 'HIGH_LEVEL_1', 'TOTAL_CLAIM_AMOUNT', 
         'TOTAL_PAID_AMOUNT', 'RISK_CATEGORY', 'DATE_KEY']
    ].head(20)
    st.dataframe(risk_table, use_container_width=True)

def main():
    # Ensure Snowflake connection
    conn = ensure_connection()
    
    # Header
    st.markdown('<h1 class="main-header">🩺 Q.CheckUp Lite - Medical Device Analytics</h1>', unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Home"):
            st.switch_page("app.py")
    with col3:
        if st.button("Q.Dose Dashboard →"):
            st.switch_page("pages/dose.py")
    
    # Filters
    with st.container():
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.subheader("🔧 Filters & Controls")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            date_range = st.selectbox("Date Range", ["Last 12 months", "Last 6 months", "Last 3 months"])
        with col2:
            province_filter = st.selectbox("Province", ["All", "Gauteng", "Western Cape", "KwaZulu-Natal"])
        with col3:
            provider_type = st.selectbox("Provider Type", ["All", "Hospitals", "Pharmacies", "Specialists"])
        with col4:
            refresh_data = st.button("🔄 Refresh Data")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Load data
    if 'checkup_lite_data' not in st.session_state or refresh_data:
        st.session_state.checkup_lite_data = load_checkup_lite_data(conn)
    
    data = st.session_state.checkup_lite_data
    
    if data is None:
        st.error("Failed to load Q.CheckUp Lite data")
        return
    
    # Create dashboard sections
    create_overview_section(data)
    
    st.markdown("---")
    create_geographic_analysis(data)
    
    st.markdown("---")
    create_provider_analysis(data)
    
    st.markdown("---")
    create_product_analysis(data)
    
    st.markdown("---")
    create_trends_analysis(data)
    
    st.markdown("---")
    create_risk_analysis(data)
    
    # Footer with performance stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Dashboard Load Time", f"{data['load_time']:.1f}s", "Target: <3s")
    with col2:
        st.metric("Total Records Analyzed", f"{data['overview'].iloc[0]['TOTAL_CLAIMS']:,.0f}" if not data['overview'].empty else "0")
    with col3:
        st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M"))

if __name__ == "__main__":
    main()