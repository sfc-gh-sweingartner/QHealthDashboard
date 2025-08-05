import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time
from datetime import datetime

# Import custom modules
from utils.snowflake_conn import ensure_connection, execute_query
from utils.viz_components import (
    create_metric_card, create_kpi_dashboard, create_hierarchy_sunburst,
    create_trend_analysis, create_financial_breakdown, create_anomaly_detection_chart,
    display_data_table, create_performance_monitor
)
from utils.queries import get_query

# Page configuration
st.set_page_config(
    page_title="Q.Dose - Pharmaceutical Analytics",
    page_icon="💊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #ff6b35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #333;
        border-bottom: 2px solid #ff6b35;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .pharma-insight-box {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .ms-focus-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #ff6b35;
    }
    .financial-metric {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff6b35;
        margin: 0.5rem 0;
    }
    .patient-demographic {
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_dose_data(conn):
    """Load all Q.Dose pharmaceutical data with performance monitoring"""
    start_time = time.time()
    
    try:
        with st.spinner("💊 Loading Q.Dose pharmaceutical analytics..."):
            
            # Load overview KPIs
            overview_df = execute_query(conn, get_query('dose', 'overview_kpis'))
            
            # Load ATC hierarchy analysis
            atc_df = execute_query(conn, get_query('dose', 'atc_hierarchy'))
            
            # Load Multiple Sclerosis specific analysis
            ms_df = execute_query(conn, get_query('dose', 'ms_analysis'))
            
            # Load patient demographics
            demographics_df = execute_query(conn, get_query('dose', 'patient_demographics'))
            
            # Load provider prescribing patterns
            providers_df = execute_query(conn, get_query('dose', 'provider_patterns'))
            
            # Load financial breakdown
            financial_df = execute_query(conn, get_query('dose', 'financial_breakdown'))
            
            # Load yearly trends
            trends_df = execute_query(conn, get_query('dose', 'yearly_trends'))
            
            # Load high-cost patients
            high_cost_df = execute_query(conn, get_query('dose', 'high_cost_patients'))
            
            load_time = time.time() - start_time
            create_performance_monitor(load_time, target_time=3.0)
            
            return {
                'overview': overview_df,
                'atc': atc_df,
                'ms_analysis': ms_df,
                'demographics': demographics_df,
                'providers': providers_df,
                'financial': financial_df,
                'trends': trends_df,
                'high_cost': high_cost_df,
                'load_time': load_time
            }
    
    except Exception as e:
        st.error(f"Error loading Q.Dose data: {str(e)}")
        return None

def create_overview_section(data):
    """Create pharmaceutical overview KPI section"""
    st.markdown('<h2 class="section-header">💊 Pharmaceutical Overview (2017-2019)</h2>', unsafe_allow_html=True)
    
    if data['overview'].empty:
        st.warning("No overview data available")
        return
    
    overview = data['overview'].iloc[0]
    
    # Create KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            "Total Prescriptions", 
            f"{overview['TOTAL_PRESCRIPTIONS']:,.0f}",
            "2017-2019 prescription records"
        )
    
    with col2:
        create_metric_card(
            "Unique Patients", 
            f"{overview['UNIQUE_PATIENTS']:,.0f}",
            "Patients receiving treatment"
        )
    
    with col3:
        create_metric_card(
            "Benefits Paid", 
            f"R{overview['TOTAL_BENEFIT_PAID']:,.0f}",
            f"Avg: R{overview['AVG_BENEFIT_PAID']:,.0f} per prescription"
        )
    
    with col4:
        copay_ratio = (overview['TOTAL_COPAY'] / overview['TOTAL_BENEFIT_PAID']) * 100
        create_metric_card(
            "Patient Copay", 
            f"{copay_ratio:.1f}%",
            f"R{overview['TOTAL_COPAY']:,.0f} patient contribution"
        )
    
    # Financial breakdown summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="financial-metric">
            <h4>💰 Cost Structure</h4>
            <p><strong>Gross Drug Cost:</strong> R{:,.0f}</p>
            <p><strong>Benefit Coverage:</strong> {:.1f}%</p>
            <p><strong>Patient Responsibility:</strong> {:.1f}%</p>
        </div>
        """.format(
            overview['TOTAL_GROSS_COST'],
            (overview['TOTAL_BENEFIT_PAID'] / overview['TOTAL_GROSS_COST']) * 100,
            (overview['TOTAL_COPAY'] / overview['TOTAL_GROSS_COST']) * 100
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="financial-metric">
            <h4>🏥 Provider Network</h4>
            <p><strong>Active Providers:</strong> {:,.0f}</p>
            <p><strong>Avg Prescriptions per Provider:</strong> {:,.0f}</p>
            <p><strong>Avg Patients per Provider:</strong> {:,.0f}</p>
        </div>
        """.format(
            overview['UNIQUE_PROVIDERS'],
            overview['TOTAL_PRESCRIPTIONS'] / overview['UNIQUE_PROVIDERS'],
            overview['UNIQUE_PATIENTS'] / overview['UNIQUE_PROVIDERS']
        ), unsafe_allow_html=True)

def create_ms_analysis_section(data):
    """Create Multiple Sclerosis focused analysis"""
    st.markdown('<h2 class="section-header">🧠 Multiple Sclerosis Drug Analysis</h2>', unsafe_allow_html=True)
    
    if data['ms_analysis'].empty:
        st.warning("No MS analysis data available")
        return
    
    # MS Focus Box
    st.markdown("""
    <div class="ms-focus-box">
        <h4>🎯 Multiple Sclerosis Treatment Focus</h4>
        <p>Specialized analysis of high-cost MS drugs including Copaxone, Interferon, and other 
        disease-modifying therapies. These treatments are critical for patient quality of life 
        and represent significant healthcare investments.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # MS drugs by prescription volume
        fig = px.bar(
            data['ms_analysis'].head(10),
            x='PRESCRIPTION_COUNT',
            y='PRODUCT_NAME',
            orientation='h',
            title="MS Drugs by Prescription Volume",
            color='TOTAL_BENEFIT_PAID',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # MS drugs by total cost
        fig = px.treemap(
            data['ms_analysis'].head(15),
            path=['NAPPI_MANUFACTURER', 'PRODUCT_NAME'],
            values='TOTAL_BENEFIT_PAID',
            title="MS Drug Costs by Manufacturer",
            color='AVG_BENEFIT_PAID',
            color_continuous_scale='OrRd'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # MS geographic distribution
    st.subheader("🗺️ MS Treatment Geographic Distribution")
    ms_geographic = data['ms_analysis'].groupby('PROVIDER_PROVINCE').agg({
        'PRESCRIPTION_COUNT': 'sum',
        'TOTAL_BENEFIT_PAID': 'sum',
        'UNIQUE_PATIENTS': 'sum'
    }).reset_index()
    
    fig = px.scatter(
        ms_geographic,
        x='UNIQUE_PATIENTS',
        y='TOTAL_BENEFIT_PAID',
        size='PRESCRIPTION_COUNT',
        color='PROVIDER_PROVINCE',
        title="MS Treatment: Patients vs Cost by Province",
        labels={
            'UNIQUE_PATIENTS': 'Unique MS Patients',
            'TOTAL_BENEFIT_PAID': 'Total Benefits Paid (R)',
            'PRESCRIPTION_COUNT': 'Prescription Count'
        }
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # MS insights
    st.markdown("""
    <div class="pharma-insight-box">
        <h4>💡 MS Treatment Insights</h4>
        <ul>
            <li><strong>High-Cost Therapy:</strong> MS drugs average R15,000+ per prescription</li>
            <li><strong>Geographic Access:</strong> Urban centers show higher treatment utilization</li>
            <li><strong>Brand Dominance:</strong> Specialty manufacturers lead this therapeutic area</li>
            <li><strong>Patient Journey:</strong> Long-term therapy requiring consistent monitoring</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def create_atc_hierarchy_analysis(data):
    """Create ATC pharmaceutical hierarchy analysis"""
    st.markdown('<h2 class="section-header">🧬 ATC Drug Classification Analysis</h2>', unsafe_allow_html=True)
    
    if data['atc'].empty:
        st.warning("No ATC hierarchy data available")
        return
    
    # ATC Level 1 summary
    level_1_summary = data['atc'].groupby(['ATC_LEVEL_1_CODE', 'ATC_LEVEL_DESC_1']).agg({
        'TOTAL_PRESCRIPTIONS': 'sum',
        'TOTAL_BENEFIT_PAID': 'sum',
        'UNIQUE_PATIENTS': 'sum'
    }).reset_index().sort_values('TOTAL_PRESCRIPTIONS', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ATC Level 1 distribution
        fig = px.pie(
            level_1_summary.head(8),
            values='TOTAL_PRESCRIPTIONS',
            names='ATC_LEVEL_DESC_1',
            title="Prescriptions by ATC Level 1 Category"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cost vs Volume analysis
        fig = px.scatter(
            level_1_summary,
            x='TOTAL_PRESCRIPTIONS',
            y='TOTAL_BENEFIT_PAID',
            size='UNIQUE_PATIENTS',
            color='ATC_LEVEL_1_CODE',
            title="ATC Categories: Volume vs Cost",
            labels={
                'TOTAL_PRESCRIPTIONS': 'Total Prescriptions',
                'TOTAL_BENEFIT_PAID': 'Total Benefits Paid (R)'
            }
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed ATC breakdown
    st.subheader("📊 Detailed ATC Breakdown")
    atc_table = level_1_summary[['ATC_LEVEL_1_CODE', 'ATC_LEVEL_DESC_1', 
                                'TOTAL_PRESCRIPTIONS', 'TOTAL_BENEFIT_PAID', 'UNIQUE_PATIENTS']]
    atc_table.columns = ['ATC Code', 'Description', 'Prescriptions', 'Benefits Paid (R)', 'Patients']
    st.dataframe(atc_table, use_container_width=True)

def create_patient_demographics_analysis(data):
    """Create patient demographics analysis"""
    st.markdown('<h2 class="section-header">👥 Patient Demographics</h2>', unsafe_allow_html=True)
    
    if data['demographics'].empty:
        st.warning("No demographics data available")
        return
    
    # Age and gender analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        age_summary = data['demographics'].groupby('AGE_BUCKET').agg({
            'UNIQUE_PATIENTS': 'sum',
            'TOTAL_PRESCRIPTIONS': 'sum',
            'TOTAL_BENEFIT_PAID': 'sum'
        }).reset_index()
        
        fig = px.bar(
            age_summary,
            x='AGE_BUCKET',
            y='UNIQUE_PATIENTS',
            title="Patient Distribution by Age",
            color='TOTAL_BENEFIT_PAID',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gender analysis
        gender_summary = data['demographics'].groupby('GENDER').agg({
            'UNIQUE_PATIENTS': 'sum',
            'TOTAL_PRESCRIPTIONS': 'sum',
            'TOTAL_BENEFIT_PAID': 'sum'
        }).reset_index()
        
        fig = px.pie(
            gender_summary,
            values='UNIQUE_PATIENTS',
            names='GENDER',
            title="Patient Distribution by Gender"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Provincial demographics
    st.subheader("🗺️ Demographics by Province")
    province_demo = data['demographics'].groupby('PROVINCE').agg({
        'UNIQUE_PATIENTS': 'sum',
        'TOTAL_PRESCRIPTIONS': 'sum',
        'TOTAL_BENEFIT_PAID': 'sum',
        'AVG_BENEFIT_PER_PATIENT': 'mean'
    }).reset_index().sort_values('UNIQUE_PATIENTS', ascending=False)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Patients by Province", "Avg Benefit per Patient"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Bar(x=province_demo['PROVINCE'], y=province_demo['UNIQUE_PATIENTS'], name="Patients"),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=province_demo['PROVINCE'], y=province_demo['AVG_BENEFIT_PER_PATIENT'], 
               name="Avg Benefit", marker_color='orange'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

def create_provider_patterns_analysis(data):
    """Create provider prescribing patterns analysis"""
    st.markdown('<h2 class="section-header">🏥 Provider Prescribing Patterns</h2>', unsafe_allow_html=True)
    
    if data['providers'].empty:
        st.warning("No provider patterns data available")
        return
    
    # Provider type analysis
    provider_type_summary = data['providers'].groupby('PROVIDER_TYPE').agg({
        'TOTAL_PRESCRIPTIONS': 'sum',
        'UNIQUE_PATIENTS': 'sum',
        'TOTAL_BENEFIT_PAID': 'sum',
        'AVG_PRESCRIPTION_VALUE': 'mean'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Prescriptions by provider type
        fig = px.bar(
            provider_type_summary,
            x='PROVIDER_TYPE',
            y='TOTAL_PRESCRIPTIONS',
            title="Prescriptions by Provider Type",
            color='AVG_PRESCRIPTION_VALUE',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Provider efficiency (patients per prescription)
        provider_type_summary['efficiency'] = (provider_type_summary['UNIQUE_PATIENTS'] / 
                                             provider_type_summary['TOTAL_PRESCRIPTIONS'])
        
        fig = px.scatter(
            provider_type_summary,
            x='TOTAL_PRESCRIPTIONS',
            y='AVG_PRESCRIPTION_VALUE',
            size='UNIQUE_PATIENTS',
            color='PROVIDER_TYPE',
            title="Provider Efficiency: Volume vs Value"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Fraud detection analysis
    st.subheader("🚨 Potential Fraud Indicators")
    
    # High-value prescribers
    high_value_providers = data['providers'][
        data['providers']['MAX_PRESCRIPTION_VALUE'] > data['providers']['MAX_PRESCRIPTION_VALUE'].quantile(0.95)
    ].head(20)
    
    if not high_value_providers.empty:
        fig = create_anomaly_detection_chart(
            data['providers'], 
            'AVG_PRESCRIPTION_VALUE',
            threshold=2.0
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("⚠️ High-Risk Providers")
        risk_table = high_value_providers[
            ['PROVIDER_NAME', 'PROVIDER_TYPE', 'PROVIDER_PROVINCE', 'TOTAL_PRESCRIPTIONS',
             'AVG_PRESCRIPTION_VALUE', 'MAX_PRESCRIPTION_VALUE']
        ]
        st.dataframe(risk_table, use_container_width=True)

def create_financial_analysis(data):
    """Create comprehensive financial analysis"""
    st.markdown('<h2 class="section-header">💰 Financial Analysis (2017-2019)</h2>', unsafe_allow_html=True)
    
    if data['financial'].empty:
        st.warning("No financial data available")
        return
    
    # Yearly financial trends
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Benefits Paid by Year", "Cost Components by Year", 
                       "Patient Copay Trends", "Prescription Volume"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Benefits paid trend
    fig.add_trace(
        go.Bar(x=data['financial']['YEAR'], y=data['financial']['BENEFIT_PAID'], 
               name="Benefits Paid", marker_color='blue'),
        row=1, col=1
    )
    
    # Cost components
    fig.add_trace(
        go.Scatter(x=data['financial']['YEAR'], y=data['financial']['GROSS_DRUG_COST'], 
                  mode='lines+markers', name="Gross Drug Cost", line=dict(color='red')),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=data['financial']['YEAR'], y=data['financial']['INGREDIENT_COST'], 
                  mode='lines+markers', name="Ingredient Cost", line=dict(color='orange')),
        row=1, col=2
    )
    
    # Patient copay
    fig.add_trace(
        go.Bar(x=data['financial']['YEAR'], y=data['financial']['PATIENT_COPAY'], 
               name="Patient Copay", marker_color='green'),
        row=2, col=1
    )
    
    # Prescription volume
    fig.add_trace(
        go.Bar(x=data['financial']['YEAR'], y=data['financial']['TOTAL_PRESCRIPTIONS'], 
               name="Prescriptions", marker_color='purple'),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=True, title_text="Financial Analysis Dashboard")
    st.plotly_chart(fig, use_container_width=True)
    
    # Financial insights
    st.markdown("""
    <div class="pharma-insight-box">
        <h4>💡 Financial Insights</h4>
        <ul>
            <li><strong>Cost Growth:</strong> Year-over-year pharmaceutical cost increases</li>
            <li><strong>Patient Burden:</strong> Copay trends indicate patient financial impact</li>
            <li><strong>Ingredient vs Total:</strong> Drug ingredient costs vs total prescription costs</li>
            <li><strong>Volume Trends:</strong> Prescription volume changes over time</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def create_high_cost_patients_analysis(data):
    """Create high-cost patients analysis"""
    st.markdown('<h2 class="section-header">💎 High-Cost Patient Analysis</h2>', unsafe_allow_html=True)
    
    if data['high_cost'].empty:
        st.warning("No high-cost patient data available")
        return
    
    # Cost category distribution
    cost_category_summary = data['high_cost']['COST_CATEGORY'].value_counts().reset_index()
    cost_category_summary.columns = ['Cost Category', 'Patient Count']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            cost_category_summary,
            values='Patient Count',
            names='Cost Category',
            title="High-Cost Patients by Category",
            color_discrete_map={
                'Very High Cost': '#dc3545',
                'High Cost': '#fd7e14',
                'Medium Cost': '#ffc107'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Demographics of high-cost patients
        age_cost = data['high_cost'].groupby('AGE_BUCKET').agg({
            'TOTAL_BENEFIT_PAID': ['count', 'sum', 'mean']
        }).round(2)
        age_cost.columns = ['Patient Count', 'Total Cost', 'Avg Cost per Patient']
        age_cost = age_cost.reset_index()
        
        fig = px.bar(
            age_cost,
            x='AGE_BUCKET',
            y='Patient Count',
            title="High-Cost Patients by Age Group",
            color='Avg Cost per Patient',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top high-cost patients table
    st.subheader("🔍 Top High-Cost Patients")
    high_cost_table = data['high_cost'][
        ['AGE_BUCKET', 'GENDER', 'PROVINCE', 'PRESCRIPTION_COUNT', 
         'TOTAL_BENEFIT_PAID', 'AVG_PRESCRIPTION_VALUE', 'COST_CATEGORY']
    ].head(20)
    high_cost_table.columns = ['Age', 'Gender', 'Province', 'Prescriptions', 
                              'Total Benefit (R)', 'Avg per Prescription (R)', 'Category']
    st.dataframe(high_cost_table, use_container_width=True)

def main():
    # Ensure Snowflake connection
    conn = ensure_connection()
    
    # Header
    st.markdown('<h1 class="main-header">💊 Q.Dose - Pharmaceutical Analytics</h1>', unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Q.CheckUp Lite"):
            st.switch_page("pages/checkup_lite.py")
    with col2:
        if st.button("🏠 Home"):
            st.switch_page("app.py")
    with col3:
        if st.button("AI Insights →"):
            st.switch_page("pages/ai_insights.py")
    
    # Load data
    if 'dose_data' not in st.session_state:
        st.session_state.dose_data = load_dose_data(conn)
    
    data = st.session_state.dose_data
    
    if data is None:
        st.error("Failed to load Q.Dose data")
        return
    
    # Create dashboard sections
    create_overview_section(data)
    
    st.markdown("---")
    create_ms_analysis_section(data)
    
    st.markdown("---")
    create_atc_hierarchy_analysis(data)
    
    st.markdown("---")
    create_patient_demographics_analysis(data)
    
    st.markdown("---")
    create_provider_patterns_analysis(data)
    
    st.markdown("---")
    create_financial_analysis(data)
    
    st.markdown("---")
    create_high_cost_patients_analysis(data)
    
    # Footer with performance stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Dashboard Load Time", f"{data['load_time']:.1f}s", "Target: <3s")
    with col2:
        st.metric("Total Prescriptions", f"{data['overview'].iloc[0]['TOTAL_PRESCRIPTIONS']:,.0f}" if not data['overview'].empty else "0")
    with col3:
        st.metric("Analysis Period", "2017-2019", "3 years historical data")

if __name__ == "__main__":
    main()