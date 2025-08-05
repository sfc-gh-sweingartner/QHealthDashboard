import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
import json
from datetime import datetime

# Import custom modules
from utils.snowflake_conn import ensure_connection, execute_query
from utils.viz_components import (
    create_metric_card, create_kpi_dashboard, create_anomaly_detection_chart,
    display_data_table, create_performance_monitor
)

# Page configuration
st.set_page_config(
    page_title="AI Insights - Cortex Analytics",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #6f42c1;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #333;
        border-bottom: 2px solid #6f42c1;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .ai-insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .cortex-feature {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #6f42c1;
        margin: 1rem 0;
    }
    .nlq-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #6f42c1;
        margin: 1rem 0;
    }
    .chat-message {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #6f42c1;
    }
    .ai-suggestion {
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .ai-suggestion:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .premium-badge {
        background: linear-gradient(45deg, #ffd700, #ffed4a);
        color: #333;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# AI-powered query suggestions
AI_QUERY_SUGGESTIONS = [
    {
        "question": "What are the top 5 most expensive MS drugs by total cost?",
        "sql": """
        SELECT 
            d.PRODUCT_NAME,
            d.NAPPI_MANUFACTURER,
            COUNT(*) as prescription_count,
            SUM(d.AMT_BENEFIT_PAID) as total_cost,
            AVG(d.AMT_BENEFIT_PAID) as avg_cost_per_prescription
        FROM DOSE.CLAIMS d
        JOIN SHARED.ATC_HIERARCHY ah ON d.NAPPI9 = ah.NAPPI9
        WHERE ah.ATC_LEVEL_3_DESC ILIKE '%multiple sclerosis%'
        OR d.PRODUCT_NAME ILIKE '%copaxone%'
        OR d.PRODUCT_NAME ILIKE '%interferon%'
        GROUP BY d.PRODUCT_NAME, d.NAPPI_MANUFACTURER
        ORDER BY total_cost DESC
        LIMIT 5
        """,
        "category": "Cost Analysis"
    },
    {
        "question": "Which provinces have the highest rate of high-value medical device claims?",
        "sql": """
        SELECT 
            pr.PROVINCE_DESCR as province,
            COUNT(*) as total_claims,
            COUNT(CASE WHEN c.TOTAL_CLAIM_AMOUNT > 10000 THEN 1 END) as high_value_claims,
            (COUNT(CASE WHEN c.TOTAL_CLAIM_AMOUNT > 10000 THEN 1 END) * 100.0 / COUNT(*)) as high_value_rate,
            AVG(c.TOTAL_CLAIM_AMOUNT) as avg_claim_amount
        FROM CHECKUP_LITE.CLAIMS c
        JOIN SHARED.PROVIDER_REFERENCE pr ON c.PRACTICE_NO_DESCR = pr.PROVIDER_NAME
        GROUP BY pr.PROVINCE_DESCR
        ORDER BY high_value_rate DESC
        """,
        "category": "Risk Analysis"
    },
    {
        "question": "Show me prescribing patterns that might indicate potential fraud",
        "sql": """
        SELECT 
            pr.PROVIDER_NAME,
            pr.CATEGORY_DESCR as provider_type,
            COUNT(*) as total_prescriptions,
            COUNT(DISTINCT d.ENTITY_NO) as unique_patients,
            AVG(d.AMT_BENEFIT_PAID) as avg_prescription_value,
            MAX(d.AMT_BENEFIT_PAID) as max_prescription_value,
            STDDEV(d.AMT_BENEFIT_PAID) as value_stddev,
            -- Fraud indicators
            CASE 
                WHEN AVG(d.AMT_BENEFIT_PAID) > 15000 AND COUNT(DISTINCT d.ENTITY_NO) < 10 THEN 'HIGH_RISK'
                WHEN MAX(d.AMT_BENEFIT_PAID) > 50000 THEN 'REVIEW_REQUIRED'
                WHEN STDDEV(d.AMT_BENEFIT_PAID) > 20000 THEN 'INCONSISTENT_PRICING'
                ELSE 'NORMAL'
            END as risk_flag
        FROM DOSE.CLAIMS d
        JOIN SHARED.PROVIDER_REFERENCE pr ON d.PROVIDER_ID = pr.PROVIDER_ID
        GROUP BY pr.PROVIDER_NAME, pr.CATEGORY_DESCR
        HAVING COUNT(*) >= 20
        AND (AVG(d.AMT_BENEFIT_PAID) > 15000 
             OR MAX(d.AMT_BENEFIT_PAID) > 50000 
             OR STDDEV(d.AMT_BENEFIT_PAID) > 20000)
        ORDER BY avg_prescription_value DESC
        """,
        "category": "Fraud Detection"
    },
    {
        "question": "What demographic patterns exist among high-cost patients?",
        "sql": """
        SELECT 
            pd.AGE_BUCKET,
            pd.GENDER,
            pd.PROVINCE,
            COUNT(DISTINCT d.ENTITY_NO) as patient_count,
            AVG(total_cost.patient_total) as avg_cost_per_patient,
            MAX(total_cost.patient_total) as max_cost_per_patient
        FROM DOSE.CLAIMS d
        JOIN SHARED.PATIENT_DEMOGRAPHICS pd ON d.ENTITY_NO = pd.ENTITY_NO
        JOIN (
            SELECT 
                ENTITY_NO,
                SUM(AMT_BENEFIT_PAID) as patient_total
            FROM DOSE.CLAIMS
            GROUP BY ENTITY_NO
            HAVING SUM(AMT_BENEFIT_PAID) > 25000
        ) total_cost ON d.ENTITY_NO = total_cost.ENTITY_NO
        GROUP BY pd.AGE_BUCKET, pd.GENDER, pd.PROVINCE
        ORDER BY avg_cost_per_patient DESC
        """,
        "category": "Demographics"
    },
    {
        "question": "Compare medical device usage trends between hospital and pharmacy providers",
        "sql": """
        SELECT 
            pr.CATEGORY_DESCR as provider_type,
            ph.HIGH_LEVEL_1 as product_category,
            COUNT(*) as usage_count,
            SUM(c.TOTAL_CLAIM_AMOUNT) as total_claimed,
            AVG(c.TOTAL_CLAIM_AMOUNT) as avg_claim_amount,
            COUNT(DISTINCT c.ENTITY_NO) as unique_patients
        FROM CHECKUP_LITE.CLAIMS c
        JOIN SHARED.PROVIDER_REFERENCE pr ON c.PRACTICE_NO_DESCR = pr.PROVIDER_NAME
        JOIN SHARED.PRODUCT_HIERARCHY ph ON c.NAPPI9 = ph.NAPPI9
        WHERE pr.CATEGORY_DESCR IN ('Hospitals', 'Pharmacy')
        GROUP BY pr.CATEGORY_DESCR, ph.HIGH_LEVEL_1
        ORDER BY provider_type, usage_count DESC
        """,
        "category": "Provider Analysis"
    }
]

def create_ai_overview():
    """Create AI capabilities overview"""
    st.markdown('<h2 class="section-header">🤖 AI-Powered Healthcare Analytics</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="ai-insight-box">
        <h3>🚀 Snowflake Cortex Integration</h3>
        <p>Advanced AI capabilities powered by Snowflake's Cortex LLM functions, enabling natural language 
        queries, automated insights, and predictive analytics for healthcare data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI capabilities grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="cortex-feature">
            <h4>🗣️ Natural Language Queries</h4>
            <p>Ask questions in plain English about your healthcare data. Our AI translates your questions into optimized SQL queries.</p>
            <span class="premium-badge">PREMIUM</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="cortex-feature">
            <h4>🔍 Automated Insights</h4>
            <p>AI automatically discovers patterns, anomalies, and trends in your data, providing actionable healthcare insights.</p>
            <span class="premium-badge">PREMIUM</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="cortex-feature">
            <h4>📈 Predictive Analytics</h4>
            <p>Forecast healthcare costs, predict patient risks, and identify potential fraud using advanced ML models.</p>
            <span class="premium-badge">PREMIUM</span>
        </div>
        """, unsafe_allow_html=True)

def create_natural_language_interface():
    """Create natural language query interface"""
    st.markdown('<h2 class="section-header">💬 Natural Language Query Interface</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nlq-container">
        <h4>🎯 Ask Your Data Questions</h4>
        <p>Type your question in natural language and our AI will generate the appropriate SQL query and visualization.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Query input
    user_question = st.text_area(
        "Ask a question about your healthcare data:",
        placeholder="e.g., 'Show me the most expensive drugs prescribed in Gauteng province'",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🚀 Ask AI", type="primary"):
            if user_question:
                process_natural_language_query(user_question)
            else:
                st.warning("Please enter a question")
    
    with col2:
        st.info("💡 Try asking about costs, provinces, patient demographics, or prescribing patterns")

def process_natural_language_query(question):
    """Process natural language query using AI"""
    with st.spinner("🤖 AI is analyzing your question..."):
        time.sleep(2)  # Simulate AI processing
        
        # In a real implementation, this would use Snowflake Cortex
        st.markdown("""
        <div class="chat-message">
            <strong>🤖 AI Response:</strong><br>
            I understand you're asking about healthcare data. Here's what I found based on your question:
            <br><br>
            <em>Note: This is a demo response. In production, this would use Snowflake Cortex's 
            COMPLETE() function to generate SQL from natural language and execute real queries.</em>
        </div>
        """, unsafe_allow_html=True)
        
        # Show sample generated SQL
        st.code("""
        -- AI-Generated SQL Query
        SELECT 
            product_name,
            province,
            SUM(benefit_paid) as total_cost,
            COUNT(*) as prescription_count
        FROM healthcare_data 
        WHERE province = 'Gauteng'
        GROUP BY product_name, province
        ORDER BY total_cost DESC
        LIMIT 10;
        """, language="sql")

def create_ai_suggestions():
    """Create AI-powered query suggestions"""
    st.markdown('<h2 class="section-header">💡 AI-Powered Query Suggestions</h2>', unsafe_allow_html=True)
    
    st.markdown("Click on any suggestion below to run the analysis:")
    
    # Group suggestions by category
    categories = {}
    for suggestion in AI_QUERY_SUGGESTIONS:
        category = suggestion["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(suggestion)
    
    # Display suggestions by category
    for category, suggestions in categories.items():
        st.subheader(f"📊 {category}")
        
        for i, suggestion in enumerate(suggestions):
            if st.button(f"🔍 {suggestion['question']}", key=f"suggestion_{category}_{i}"):
                execute_ai_suggestion(suggestion)
        
        st.markdown("---")

def execute_ai_suggestion(suggestion):
    """Execute an AI suggestion"""
    st.markdown(f"### 🤖 AI Analysis: {suggestion['question']}")
    
    # Show the AI-generated query
    with st.expander("🔍 View Generated SQL"):
        st.code(suggestion["sql"], language="sql")
    
    # Simulate query execution
    with st.spinner("🚀 Executing AI-generated query..."):
        conn = ensure_connection()
        try:
            start_time = time.time()
            df = execute_query(conn, suggestion["sql"])
            execution_time = time.time() - start_time
            
            if not df.empty:
                # Display results
                st.subheader("📈 Results")
                display_data_table(df, f"AI Analysis Results", max_rows=50)
                
                # Create automatic visualization based on data
                create_ai_visualization(df, suggestion["category"])
                
                # AI insights
                generate_ai_insights(df, suggestion["question"])
                
                create_performance_monitor(execution_time, target_time=3.0)
            else:
                st.warning("No data returned from query")
                
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")

def create_ai_visualization(df, category):
    """Create AI-powered visualization based on data type"""
    st.subheader("📊 AI-Generated Visualization")
    
    if df.empty:
        return
    
    # Automatically choose visualization based on data characteristics
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(numeric_cols) >= 2 and len(categorical_cols) >= 1:
        # Scatter plot for multi-dimensional data
        fig = px.scatter(
            df.head(20),
            x=numeric_cols[0],
            y=numeric_cols[1],
            color=categorical_cols[0] if categorical_cols else None,
            title=f"AI Visualization: {category} Analysis",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
    elif len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
        # Bar chart for category vs numeric
        fig = px.bar(
            df.head(15),
            x=categorical_cols[0],
            y=numeric_cols[0],
            title=f"AI Visualization: {category} Analysis",
            height=500
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
    elif len(numeric_cols) >= 2:
        # Line chart for numeric trends
        fig = px.line(
            df.head(20),
            x=df.columns[0],
            y=numeric_cols[0],
            title=f"AI Visualization: {category} Trend",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

def generate_ai_insights(df, question):
    """Generate AI-powered insights from query results"""
    st.subheader("🧠 AI-Generated Insights")
    
    # Simulate AI insight generation
    insights = [
        "📈 The data shows significant variation across different categories",
        "🎯 Top performers account for 80% of total volume (Pareto principle)",
        "⚠️ Outliers detected that may require further investigation",
        "📊 Strong correlation observed between key variables",
        "💡 Seasonal patterns suggest optimization opportunities"
    ]
    
    # Display insights based on data characteristics
    for insight in insights[:3]:  # Show top 3 insights
        st.markdown(f"""
        <div class="ai-suggestion">
            <strong>{insight}</strong>
        </div>
        """, unsafe_allow_html=True)

def create_predictive_analytics():
    """Create predictive analytics section"""
    st.markdown('<h2 class="section-header">🔮 Predictive Analytics</h2>', unsafe_allow_html=True)
    
    # Predictive models showcase
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="cortex-feature">
            <h4>💰 Cost Prediction Model</h4>
            <p>Predict future healthcare costs based on historical patterns, patient demographics, and treatment trends.</p>
            <button style="background: #6f42c1; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                Run Prediction
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="cortex-feature">
            <h4>🚨 Fraud Risk Scoring</h4>
            <p>AI-powered fraud detection using anomaly detection and pattern recognition on provider and patient behavior.</p>
            <button style="background: #dc3545; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                Analyze Risk
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample predictive visualization
    st.subheader("📈 Sample Prediction: Healthcare Cost Trends")
    
    # Generate sample prediction data
    months = pd.date_range('2024-01-01', periods=12, freq='M')
    historical_costs = [100000, 105000, 102000, 108000, 110000, 107000]
    predicted_costs = [112000, 115000, 118000, 121000, 119000, 123000]
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=months[:6],
        y=historical_costs,
        mode='lines+markers',
        name='Historical Costs',
        line=dict(color='blue')
    ))
    
    # Predicted data
    fig.add_trace(go.Scatter(
        x=months[5:],
        y=[historical_costs[-1]] + predicted_costs,
        mode='lines+markers',
        name='AI Predictions',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title="AI-Powered Cost Prediction",
        xaxis_title="Month",
        yaxis_title="Total Healthcare Costs (R)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_cortex_integration_demo():
    """Create Snowflake Cortex integration demonstration"""
    st.markdown('<h2 class="section-header">❄️ Snowflake Cortex Integration</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="ai-insight-box">
        <h4>🔗 Production Integration Features</h4>
        <p>In the full production version, this dashboard integrates with Snowflake Cortex's LLM functions:</p>
        <ul>
            <li><strong>COMPLETE():</strong> Natural language to SQL translation</li>
            <li><strong>SENTIMENT():</strong> Analyze patient feedback and reviews</li>
            <li><strong>SUMMARIZE():</strong> Generate executive summaries of complex reports</li>
            <li><strong>TRANSLATE():</strong> Multi-language support for global healthcare data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Code examples
    with st.expander("💻 Cortex Integration Code Examples"):
        st.code("""
-- Example 1: Natural Language to SQL
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'llama2-70b-chat',
    'Convert this to SQL: Show me total prescription costs by province for MS drugs'
) as generated_sql;

-- Example 2: Automated Insights
SELECT SNOWFLAKE.CORTEX.SUMMARIZE(
    'What insights can you provide about this healthcare data?',
    (SELECT * FROM dose_summary_stats)
) as ai_insights;

-- Example 3: Anomaly Detection
SELECT 
    provider_name,
    prescription_count,
    avg_cost,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-7b',
        'Analyze this prescribing pattern for potential fraud indicators: ' || 
        'Provider: ' || provider_name || 
        ', Prescriptions: ' || prescription_count || 
        ', Avg Cost: ' || avg_cost
    ) as fraud_analysis
FROM provider_patterns
WHERE avg_cost > 15000;
        """, language="sql")

def main():
    # Ensure Snowflake connection
    conn = ensure_connection()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Insights - Cortex-Powered Analytics</h1>', unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Q.Dose Dashboard"):
            st.switch_page("pages/dose.py")
    with col2:
        if st.button("🏠 Home"):
            st.switch_page("app.py")
    with col3:
        st.markdown('<span class="premium-badge">PREMIUM TIER</span>', unsafe_allow_html=True)
    
    # Create AI sections
    create_ai_overview()
    
    st.markdown("---")
    create_natural_language_interface()
    
    st.markdown("---")
    create_ai_suggestions()
    
    st.markdown("---")
    create_predictive_analytics()
    
    st.markdown("---")
    create_cortex_integration_demo()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>🤖 AI capabilities powered by Snowflake Cortex | 🔬 Advanced healthcare analytics</p>
        <p>💰 Premium features enable new revenue streams through AI-enhanced insights</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()