import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Import custom modules
from utils.snowflake_conn import get_snowflake_connection, test_connection, execute_query, execute_cache_clear_query, clear_snowflake_cache_sis
from utils.viz_components import create_metric_card, create_performance_monitor

# Page configuration
st.set_page_config(
    page_title="Quantium Healthcare Analytics Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern healthcare theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-container {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .nav-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .performance-badge {
        background: #28a745;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'page_load_time' not in st.session_state:
        st.session_state.page_load_time = time.time()
    if 'snowflake_connection' not in st.session_state:
        st.session_state.snowflake_connection = None
    if 'connection_status' not in st.session_state:
        st.session_state.connection_status = 'Not Connected'

def main():
    # Initialize session state
    initialize_session_state()
    
    # Auto-connect to Snowflake on page load (similar to nation_app.py)
    if st.session_state.snowflake_connection is None:
        with st.spinner("Connecting to Snowflake..."):
            try:
                conn = get_snowflake_connection()
                if conn and test_connection(conn):
                    st.session_state.connection_status = 'Connected ✅'
                    st.session_state.snowflake_connection = conn
                else:
                    st.session_state.connection_status = 'Failed ❌'
                    st.error("Failed to connect to Snowflake. Please check your connection parameters.")
            except Exception as e:
                st.session_state.connection_status = f'Error: {str(e)}'
                st.error(f"Snowflake connection error: {str(e)}")
    
    # Header
    st.markdown('<h1 class="main-header">🏥 Quantium Healthcare Analytics Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Modern healthcare dashboards powered by Snowflake & AI</p>', unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## 🚀 Navigation")
        
        # Connection Status (now display-only)
        with st.container():
            st.markdown("### 🔗 Connection Status")
            st.info(f"Status: {st.session_state.connection_status}")
            
            # Optional manual reconnect button
            if st.session_state.connection_status != 'Connected ✅':
                if st.button("🔄 Retry Connection", key="retry_conn"):
                    st.rerun()
        
        st.markdown("---")
        
        # Product Navigation
        st.markdown("### 📊 Healthcare Products")
        
        # Q.CheckUp Lite
        if st.button("🩺 Q.CheckUp Lite", key="checkup_lite", help="Medical Device & Claims Analytics"):
            st.switch_page("pages/checkup_lite.py")
        
        # Q.Dose
        if st.button("💊 Q.Dose", key="dose", help="Pharmaceutical Analytics"):
            st.switch_page("pages/dose.py")
        
        # Visualisations Gallery
        if st.button("🎨 Visualisations Gallery", key="visualisations", help="Showcase of Advanced Visualizations"):
            st.switch_page("pages/visualisations.py")

        st.markdown("---")
        
        # Performance Monitor
        st.markdown("### ⚡ Performance")
        current_time = time.time()
        load_time = current_time - st.session_state.page_load_time
        
        if load_time < 3:
            st.markdown(f'<span class="performance-badge">🚀 {load_time:.1f}s</span>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ Load time: {load_time:.1f}s")
        
        st.markdown("---")
        
        # Cache Management
        st.markdown("### 🧹 Cache Management")
        st.markdown("*For performance testing*")
        
        # Clear Snowflake Cache Button
        if st.button("🗑️ Clear Snowflake Cache", key="clear_sf_cache", help="Clear query cache (method varies by environment)"):
            if st.session_state.connection_status == 'Connected ✅':
                try:
                    conn = st.session_state.snowflake_connection
                    
                    with st.spinner("Clearing Snowflake cache..."):
                        # Check if we're in Streamlit in Snowflake (Snowpark session)
                        if hasattr(conn, 'sql'):  # Snowpark session
                            st.info("🏔️ Detected Streamlit in Snowflake environment")
                            
                            # Use specialized cache clearing for Streamlit in Snowflake
                            if clear_snowflake_cache_sis(conn):
                                st.success("✅ Cache bypass activated! Subsequent queries will use fresh data.")
                                st.info("💡 In Streamlit in Snowflake, cache clearing is limited but session has been refreshed.")
                            else:
                                st.warning("⚠️ Cache clearing had limited effect in this environment.")
                                st.info("💡 Try the 'Clear Streamlit Cache' button or refresh the page for best results.")
                        
                        else:  # Regular connection - can use warehouse commands
                            st.info("💻 Detected local Snowflake connection")
                            
                            # Try warehouse suspension (may fail if no permissions)
                            try:
                                execute_cache_clear_query(conn, "ALTER WAREHOUSE MYWH SUSPEND")
                                time.sleep(1)
                                execute_cache_clear_query(conn, "ALTER WAREHOUSE MYWH RESUME")
                                st.success("✅ Warehouse MYWH restarted - query cache cleared!")
                            except Exception as warehouse_err:
                                st.warning(f"⚠️ Warehouse restart failed: {str(warehouse_err)}")
                            
                            # Try session settings (may fail in some environments)
                            try:
                                execute_cache_clear_query(conn, "ALTER SESSION SET USE_CACHED_RESULT = FALSE")
                                st.success("✅ Result caching disabled for this session!")
                            except Exception as session_err:
                                st.warning(f"⚠️ Session setting failed: {str(session_err)}")
                        
                except Exception as e:
                    st.error(f"❌ Failed to clear Snowflake cache: {str(e)}")
                    st.info("💡 Try the 'Clear Streamlit Cache' button instead, or refresh the page.")
            else:
                st.warning("⚠️ No Snowflake connection available")
        
        # Clear Streamlit Cache Button  
        if st.button("🗑️ Clear Streamlit Cache", key="clear_st_cache", help="Clear all Streamlit cached data and resources"):
            try:
                with st.spinner("Clearing Streamlit cache..."):
                    # Clear all Streamlit caches
                    st.cache_data.clear()
                    st.cache_resource.clear()
                    
                    # Clear specific connection cache by clearing session state
                    if 'snowflake_connection' in st.session_state:
                        st.session_state.snowflake_connection = None
                        st.session_state.connection_status = 'Not Connected'
                    
                st.success("✅ Streamlit cache cleared! Page will reconnect automatically.")
                time.sleep(0.5)  # Brief pause before rerun
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to clear Streamlit cache: {str(e)}")
    
    # Main Content Area
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="nav-section">
            <h3>🩺 Q.CheckUp Lite</h3>
            <p><strong>Medical Device Analytics</strong></p>
            <ul>
                <li>1.1M+ healthcare claims (2024)</li>
                <li>Provider performance analysis</li>
                <li>Geographic distribution across SA</li>
                <li>4-level product hierarchy</li>
                <li>Cost optimization insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Q.CheckUp Lite →", key="launch_checkup"):
            st.switch_page("pages/checkup_lite.py")
    
    with col2:
        st.markdown("""
        <div class="nav-section">
            <h3>💊 Q.Dose</h3>
            <p><strong>Pharmaceutical Analytics</strong></p>
            <ul>
                <li>1.2M+ prescription records (2017-2019)</li>
                <li>Multiple Sclerosis focus</li>
                <li>Patient demographic patterns</li>
                <li>5-level ATC hierarchy</li>
                <li>13-source financial breakdown</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Q.Dose →", key="launch_dose"):
            st.switch_page("pages/dose.py")
    
    # Visualisations Gallery Section
    st.markdown("---")
    st.markdown("## 🎨 Visualizations Gallery")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="nav-section">
            <h3>🎨 Advanced Visualization Gallery</h3>
            <p><strong>Showcase of Streamlit's Visual Power</strong></p>
            <ul>
                <li>Professional Healthcare Analytics</li>
                <li>Interactive dashboards & KPI metrics</li>
                <li>Statistical analysis & correlations</li>
                <li>Provincial demographic breakdowns</li>
                <li>Zero-dependency reliability</li>
                <li>Publication-quality aesthetics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Explore Gallery →", key="launch_gallery"):
            st.switch_page("pages/visualisations.py")
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white;">
            <h2 style="margin: 0; color: white;">5</h2>
            <p style="margin: 0.5rem 0; color: #f8f9fa;">Analysis Modules</p>
            <p style="margin: 0; font-size: 0.9rem; color: #dee2e6;">Interactive • Reliable • Fast</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Platform Overview Metrics
    st.markdown("## 📈 Platform Overview")
    
    # Create sample metrics (these would be real-time in production)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Total Records", "2.3M+", "Combined Q.CheckUp Lite + Q.Dose")
    
    with col2:
        create_metric_card("Load Performance", "<3 sec", "90% improvement vs Tableau")
    
    with col3:
        create_metric_card("Active Provinces", "9/9", "Complete SA coverage")
    
    with col4:
        create_metric_card("Intelligence", "Active", "Snowflake Intelligence enabled")
    
    # Quick Stats Dashboard
    if st.session_state.connection_status == 'Connected ✅':
        st.markdown("## 🔍 Quick Data Overview")
        
        try:
            # Get real data from Snowflake
            conn = st.session_state.snowflake_connection
            
            # Query for healthcare claims count
            healthcare_query = "SELECT COUNT(*) as count FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS"
            healthcare_df = execute_query(conn, healthcare_query)
            healthcare_count = healthcare_df['COUNT'].iloc[0] if not healthcare_df.empty else 0
            
            # Query for pharmaceutical claims count  
            pharma_query = "SELECT COUNT(*) as count FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS"
            pharma_df = execute_query(conn, pharma_query)
            pharma_count = pharma_df['COUNT'].iloc[0] if not pharma_df.empty else 0
            
            # Create visualization with real data
            fig = px.bar(
                x=['Q.CheckUp Lite', 'Q.Dose'],
                y=[healthcare_count, pharma_count],
                title="Records by Product",
                color=['Q.CheckUp Lite', 'Q.Dose'],
                color_discrete_map={'Q.CheckUp Lite': '#1f77b4', 'Q.Dose': '#ff7f0e'}
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Failed to load data: {str(e)}")
            # Fallback to basic message
            st.info("Data overview will be available once Snowflake connection is established")
    
    else:
        st.info("🔗 Connect to Snowflake to see live data overview")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>⚡ Powered by Snowflake Data Cloud & Streamlit | 🎯 Target: <5 second load times</p>
        <p>🚀 Migration from 40-50s Tableau to modern web analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()