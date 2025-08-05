import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# Basic visualization page using only pre-installed packages
# This version works with just pandas, numpy, and streamlit (no external viz libraries)

# Page configuration
st.set_page_config(
    page_title="Healthcare Visualizations Gallery - Basic",
    page_icon="📊", 
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .chart-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def generate_basic_data():
    """Generate sample healthcare data using only pandas and numpy"""
    np.random.seed(42)
    
    # Patient data
    n_patients = 1000
    patients = pd.DataFrame({
        'patient_id': range(1, n_patients + 1),
        'age': np.random.normal(45, 15, n_patients).clip(18, 90).astype(int),
        'gender': np.random.choice(['Male', 'Female'], n_patients),
        'province': np.random.choice([
            'Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape',
            'Limpopo', 'Mpumalanga', 'North West', 'Free State', 'Northern Cape'
        ], n_patients),
        'satisfaction_score': np.random.normal(7.5, 1.5, n_patients).clip(1, 10),
        'treatment_cost': np.random.lognormal(8, 1, n_patients)
    })
    
    return patients

def create_basic_metrics(data):
    """Create basic metrics using streamlit native components"""
    
    st.markdown('<h1 class="main-header">📊 Healthcare Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Patients", 
            f"{len(data):,}",
            delta=f"+{len(data)//10} this month"
        )
    
    with col2:
        avg_age = data['age'].mean()
        st.metric(
            "Average Age", 
            f"{avg_age:.1f} years",
            delta=f"{avg_age - 44:.1f} vs baseline"
        )
    
    with col3:
        avg_satisfaction = data['satisfaction_score'].mean()
        st.metric(
            "Satisfaction Score", 
            f"{avg_satisfaction:.1f}/10",
            delta=f"{avg_satisfaction - 7:.1f} vs target"
        )
    
    with col4:
        avg_cost = data['treatment_cost'].mean()
        st.metric(
            "Avg Treatment Cost", 
            f"R{avg_cost:,.0f}",
            delta=f"R{avg_cost - 5000:,.0f} vs budget"
        )

def create_data_tables(data):
    """Create informative data tables"""
    
    st.markdown("## 📋 Patient Demographics Summary")
    
    # Gender distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Gender Distribution")
        gender_dist = data['gender'].value_counts()
        st.dataframe(
            pd.DataFrame({
                'Gender': gender_dist.index,
                'Count': gender_dist.values,
                'Percentage': (gender_dist.values / len(data) * 100).round(1)
            }),
            use_container_width=True
        )
    
    with col2:
        st.markdown("### Province Distribution")
        province_dist = data['province'].value_counts().head(5)
        st.dataframe(
            pd.DataFrame({
                'Province': province_dist.index,
                'Count': province_dist.values,
                'Percentage': (province_dist.values / len(data) * 100).round(1)
            }),
            use_container_width=True
        )

def create_statistical_summary(data):
    """Create statistical summaries"""
    
    st.markdown("## 📈 Statistical Analysis")
    
    # Age distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Age Statistics")
        age_stats = data['age'].describe()
        st.dataframe(
            pd.DataFrame({
                'Statistic': ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max'],
                'Value': [
                    f"{age_stats['count']:.0f}",
                    f"{age_stats['mean']:.1f} years", 
                    f"{age_stats['std']:.1f} years",
                    f"{age_stats['min']:.0f} years",
                    f"{age_stats['25%']:.0f} years",
                    f"{age_stats['50%']:.0f} years", 
                    f"{age_stats['75%']:.0f} years",
                    f"{age_stats['max']:.0f} years"
                ]
            }),
            use_container_width=True
        )
    
    with col2:
        st.markdown("### Satisfaction Statistics")
        sat_stats = data['satisfaction_score'].describe()
        st.dataframe(
            pd.DataFrame({
                'Statistic': ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max'],
                'Value': [
                    f"{sat_stats['count']:.0f}",
                    f"{sat_stats['mean']:.2f}/10",
                    f"{sat_stats['std']:.2f}",
                    f"{sat_stats['min']:.1f}/10", 
                    f"{sat_stats['25%']:.1f}/10",
                    f"{sat_stats['50%']:.1f}/10",
                    f"{sat_stats['75%']:.1f}/10",
                    f"{sat_stats['max']:.1f}/10"
                ]
            }),
            use_container_width=True
        )

def create_province_analysis(data):
    """Create province-level analysis"""
    
    st.markdown("## 🗺️ Provincial Analysis")
    
    # Province summary
    province_summary = data.groupby('province').agg({
        'patient_id': 'count',
        'age': 'mean',
        'satisfaction_score': 'mean',
        'treatment_cost': 'mean'
    }).round(2)
    
    province_summary.columns = ['Patient Count', 'Avg Age', 'Avg Satisfaction', 'Avg Cost']
    province_summary = province_summary.sort_values('Patient Count', ascending=False)
    
    # Add rankings
    province_summary['Satisfaction Rank'] = province_summary['Avg Satisfaction'].rank(ascending=False).astype(int)
    province_summary['Cost Efficiency Rank'] = province_summary['Avg Cost'].rank(ascending=True).astype(int)
    
    st.dataframe(province_summary, use_container_width=True)
    
    # Top performing provinces
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top Satisfaction Provinces")
        top_satisfaction = province_summary.nlargest(3, 'Avg Satisfaction')[['Avg Satisfaction']]
        st.dataframe(top_satisfaction, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Most Cost-Efficient Provinces") 
        top_efficiency = province_summary.nsmallest(3, 'Avg Cost')[['Avg Cost']]
        st.dataframe(top_efficiency, use_container_width=True)

def create_correlation_analysis(data):
    """Create correlation analysis"""
    
    st.markdown("## 🔗 Correlation Analysis")
    
    # Numeric correlations
    numeric_cols = ['age', 'satisfaction_score', 'treatment_cost']
    corr_matrix = data[numeric_cols].corr()
    
    st.markdown("### Correlation Matrix")
    st.dataframe(corr_matrix.round(3), use_container_width=True)
    
    # Key insights
    st.markdown("### 🔍 Key Insights")
    
    age_satisfaction_corr = corr_matrix.loc['age', 'satisfaction_score']
    cost_satisfaction_corr = corr_matrix.loc['treatment_cost', 'satisfaction_score']
    age_cost_corr = corr_matrix.loc['age', 'treatment_cost']
    
    insights = [
        f"**Age vs Satisfaction**: {age_satisfaction_corr:.3f} correlation",
        f"**Cost vs Satisfaction**: {cost_satisfaction_corr:.3f} correlation", 
        f"**Age vs Cost**: {age_cost_corr:.3f} correlation"
    ]
    
    for insight in insights:
        st.markdown(f"• {insight}")

def create_interactive_filters(data):
    """Create interactive filters and filtered views"""
    
    st.markdown("## 🎛️ Interactive Data Explorer")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_provinces = st.multiselect(
            "Select Provinces",
            options=data['province'].unique(),
            default=data['province'].unique()[:3]
        )
    
    with col2:
        age_range = st.slider(
            "Age Range",
            min_value=int(data['age'].min()),
            max_value=int(data['age'].max()),
            value=(25, 65)
        )
    
    with col3:
        gender_filter = st.selectbox(
            "Gender",
            options=['All'] + list(data['gender'].unique())
        )
    
    # Apply filters
    filtered_data = data[
        (data['province'].isin(selected_provinces)) &
        (data['age'] >= age_range[0]) &
        (data['age'] <= age_range[1])
    ]
    
    if gender_filter != 'All':
        filtered_data = filtered_data[filtered_data['gender'] == gender_filter]
    
    # Show filtered results
    st.markdown(f"### 📊 Filtered Results ({len(filtered_data):,} patients)")
    
    if len(filtered_data) > 0:
        # Summary metrics for filtered data
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Filtered Patients", f"{len(filtered_data):,}")
        with col2:
            st.metric("Avg Age", f"{filtered_data['age'].mean():.1f}")
        with col3:
            st.metric("Avg Satisfaction", f"{filtered_data['satisfaction_score'].mean():.2f}")
        
        # Show sample of filtered data
        st.dataframe(filtered_data.head(20), use_container_width=True)
    else:
        st.warning("No patients match the selected filters.")

def main():
    """Main function"""
    
    # Generate data
    start_time = time.time()
    data = generate_basic_data()
    load_time = time.time() - start_time
    
    # Performance indicator
    if load_time < 1:
        st.success(f"⚡ Data loaded in {load_time:.2f}s")
    else:
        st.warning(f"⏱️ Data loaded in {load_time:.2f}s")
    
    # Create visualizations
    create_basic_metrics(data)
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Demographics", 
        "📈 Statistics", 
        "🗺️ Provincial", 
        "🔗 Correlations",
        "🎛️ Interactive"
    ])
    
    with tab1:
        create_data_tables(data)
    
    with tab2:
        create_statistical_summary(data)
    
    with tab3:
        create_province_analysis(data)
    
    with tab4:
        create_correlation_analysis(data)
    
    with tab5:
        create_interactive_filters(data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem;">
        <h4>🛡️ Snowflake Compatible Version</h4>
        <p><strong>No External Dependencies</strong> • Uses only pandas, numpy, and streamlit</p>
        <p><strong>Fully Interactive</strong> • Filters, metrics, and statistical analysis</p>
        <p><strong>Production Ready</strong> • Optimized for Snowflake deployment</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()