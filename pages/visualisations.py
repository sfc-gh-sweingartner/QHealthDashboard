import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import altair as alt
# Note: matplotlib and seaborn removed due to Snowflake conda channel compatibility
# Using Plotly and Altair for all visualizations to ensure compatibility

# Import custom modules
from utils.snowflake_conn import ensure_connection, execute_query
from utils.viz_components import create_performance_monitor
from utils.queries import get_query

# Page configuration
st.set_page_config(
    page_title="Healthcare Visualizations Gallery",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS for gallery
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .gallery-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .viz-title {
        font-size: 1.3rem;
        color: #333;
        font-weight: 600;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
        padding-left: 1rem;
    }
    .viz-description {
        color: #666;
        font-style: italic;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background: #e9ecef;
        border-radius: 5px;
    }
    .category-header {
        font-size: 2rem;
        color: #495057;
        text-align: center;
        margin: 3rem 0 2rem 0;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f3f6;
        border-radius: 4px;
        gap: 12px;
        padding-left: 12px;
        padding-right: 12px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def generate_sample_data():
    """Generate comprehensive sample healthcare data for visualizations"""
    np.random.seed(42)  # For reproducible results
    
    # Patient demographics
    n_patients = 5000
    patients_df = pd.DataFrame({
        'patient_id': range(1, n_patients + 1),
        'age': np.random.normal(45, 15, n_patients).clip(18, 90),
        'gender': np.random.choice(['Male', 'Female'], n_patients, p=[0.48, 0.52]),
        'province': np.random.choice([
            'Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape',
            'Limpopo', 'Mpumalanga', 'North West', 'Free State', 'Northern Cape'
        ], n_patients, p=[0.25, 0.18, 0.15, 0.12, 0.1, 0.08, 0.06, 0.04, 0.02]),
        'bmi': np.random.normal(26, 4, n_patients).clip(15, 50),
        'blood_pressure_systolic': np.random.normal(125, 20, n_patients).clip(90, 200),
        'cholesterol': np.random.normal(180, 30, n_patients).clip(100, 300),
        'satisfaction_score': np.random.normal(7.5, 1.5, n_patients).clip(1, 10)
    })
    
    # Time series data
    dates = pd.date_range('2020-01-01', '2024-12-31', freq='D')
    time_series_df = pd.DataFrame({
        'date': dates,
        'admissions': np.random.poisson(50, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 10,
        'discharges': np.random.poisson(48, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 8,
        'bed_occupancy': np.random.normal(75, 10, len(dates)).clip(40, 100),
        'er_wait_time': np.random.exponential(30, len(dates)).clip(5, 180)
    })
    
    # Clinical biomarkers correlation matrix
    biomarkers = ['Glucose', 'Hemoglobin', 'WBC_Count', 'Platelet_Count', 'Creatinine', 'ALT', 'AST']
    n_biomarkers = len(biomarkers)
    correlation_matrix = np.random.uniform(-0.8, 0.8, (n_biomarkers, n_biomarkers))
    correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2
    np.fill_diagonal(correlation_matrix, 1)
    
    # Clinic performance data
    clinics_df = pd.DataFrame({
        'clinic_name': [f'Clinic {chr(65+i)}' for i in range(20)],
        'patient_volume': np.random.randint(500, 3000, 20),
        'avg_wait_time': np.random.normal(25, 8, 20).clip(5, 60),
        'satisfaction_score': np.random.uniform(6.5, 9.5, 20),
        'staff_count': np.random.randint(10, 50, 20)
    })
    
    # Gene expression data (volcano plot)
    n_genes = 1000
    genes_df = pd.DataFrame({
        'gene_id': [f'Gene_{i:04d}' for i in range(n_genes)],
        'log2_fold_change': np.random.normal(0, 2, n_genes),
        'p_value': np.random.exponential(0.1, n_genes).clip(0.001, 1),
        'significance': lambda x: x < 0.05
    })
    genes_df['neg_log10_p'] = -np.log10(genes_df['p_value'])
    genes_df['significance'] = genes_df['p_value'] < 0.05
    
    # Treatment pathway data
    pathways_df = pd.DataFrame({
        'admission_type': np.random.choice(['Emergency', 'Planned', 'Urgent'], 300, p=[0.4, 0.4, 0.2]),
        'diagnosis_group': np.random.choice(['Cardiovascular', 'Respiratory', 'Neurological', 'Orthopedic'], 300),
        'treatment_phase': np.random.choice(['Initial', 'Treatment', 'Recovery', 'Discharge'], 300),
        'patient_count': np.random.randint(5, 50, 300)
    })
    
    # Disease prevalence over time
    diseases = ['Diabetes', 'Hypertension', 'Heart Disease', 'Cancer', 'Stroke']
    years = range(2015, 2024)
    disease_trends = []
    for year in years:
        for disease in diseases:
            base_rate = {'Diabetes': 0.15, 'Hypertension': 0.25, 'Heart Disease': 0.10, 'Cancer': 0.08, 'Stroke': 0.05}[disease]
            trend = base_rate + (year - 2015) * np.random.uniform(-0.005, 0.01)
            disease_trends.append({
                'year': year,
                'disease': disease,
                'prevalence_rate': trend + np.random.normal(0, 0.01),
                'patient_count': int(trend * 100000 + np.random.normal(0, 1000))
            })
    disease_trends_df = pd.DataFrame(disease_trends)
    
    # Network data for referral patterns
    providers = [f'Provider_{i}' for i in range(20)]
    network_df = pd.DataFrame({
        'source': np.random.choice(providers, 100),
        'target': np.random.choice(providers, 100),
        'referral_count': np.random.randint(1, 50, 100)
    })
    
    return {
        'patients': patients_df,
        'time_series': time_series_df,
        'biomarkers': biomarkers,
        'correlation_matrix': correlation_matrix,
        'clinics': clinics_df,
        'genes': genes_df,
        'pathways': pathways_df,
        'disease_trends': disease_trends_df,
        'network': network_df
    }

def create_plotly_visualizations(data):
    """Create Plotly-based visualizations"""
    
    st.markdown('<h2 class="category-header">🚀 Plotly Interactive Visualizations</h2>', unsafe_allow_html=True)
    
    # 1. Interactive Patient Cohort Scatter Plot
    with st.container():
        st.markdown('<div class="viz-title">1. Interactive Patient Cohort Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Explore correlations between age, cholesterol, and BMI with gender segmentation</div>', unsafe_allow_html=True)
        
        fig1 = px.scatter(
            data['patients'],
            x='age',
            y='cholesterol',
            color='gender',
            size='bmi',
            hover_data=['patient_id', 'province', 'satisfaction_score'],
            title='Patient Demographics: Age vs Cholesterol (sized by BMI)',
            color_discrete_map={'Male': '#1f77b4', 'Female': '#ff7f0e'},
            template='plotly_white'
        )
        fig1.update_layout(height=500, font=dict(size=12))
        st.plotly_chart(fig1, use_container_width=True, theme="streamlit")
    
    # 2. Animated Time Series for Hospital Metrics
    with st.container():
        st.markdown('<div class="viz-title">2. Dynamic Hospital Operations Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Real-time view of admissions, discharges, and bed occupancy over time</div>', unsafe_allow_html=True)
        
        # Prepare data for animation
        ts_melted = data['time_series'].melt(
            id_vars=['date'], 
            value_vars=['admissions', 'discharges', 'bed_occupancy'],
            var_name='metric', value_name='value'
        )
        ts_melted['month'] = ts_melted['date'].dt.to_period('M').astype(str)
        ts_monthly = ts_melted.groupby(['month', 'metric'])['value'].mean().reset_index()
        
        fig2 = px.line(
            ts_monthly,
            x='month',
            y='value',
            color='metric',
            title='Hospital Operations Trends (Monthly Averages)',
            animation_frame='month',
            range_y=[0, ts_monthly['value'].max() * 1.1]
        )
        fig2.update_layout(height=500, xaxis_tickangle=45)
        st.plotly_chart(fig2, use_container_width=True, theme="streamlit")
    
    # 3. 3D Scatter Plot for Patient Clustering
    with st.container():
        st.markdown('<div class="viz-title">3. Advanced 3D Patient Clustering</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Three-dimensional analysis of patient health metrics</div>', unsafe_allow_html=True)
        
        fig3 = px.scatter_3d(
            data['patients'].sample(500),  # Sample for performance
            x='age',
            y='bmi',
            z='blood_pressure_systolic',
            color='province',
            size='satisfaction_score',
            hover_data=['patient_id'],
            title='3D Patient Health Profile Analysis',
            template='plotly_dark'
        )
        fig3.update_layout(height=600, scene=dict(camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))))
        st.plotly_chart(fig3, use_container_width=True, theme="streamlit")
    
    # 4. Clinical Biomarker Correlation Heatmap
    with st.container():
        st.markdown('<div class="viz-title">4. Clinical Biomarker Correlation Matrix</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Interactive heatmap showing relationships between lab results</div>', unsafe_allow_html=True)
        
        fig4 = px.imshow(
            data['correlation_matrix'],
            x=data['biomarkers'],
            y=data['biomarkers'],
            color_continuous_scale='RdBu',
            text_auto=True,
            title='Biomarker Correlation Analysis',
            aspect='auto'
        )
        fig4.update_layout(height=500)
        st.plotly_chart(fig4, use_container_width=True, theme="streamlit")
    
    # 5. Sunburst Chart for Treatment Pathways
    with st.container():
        st.markdown('<div class="viz-title">5. Patient Treatment Journey Visualization</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Hierarchical view of patient pathways through healthcare system</div>', unsafe_allow_html=True)
        
        fig5 = px.sunburst(
            data['pathways'],
            path=['admission_type', 'diagnosis_group', 'treatment_phase'],
            values='patient_count',
            title='Patient Treatment Pathways',
            color='patient_count',
            color_continuous_scale='Viridis'
        )
        fig5.update_layout(height=600)
        st.plotly_chart(fig5, use_container_width=True, theme="streamlit")
    
    # 6. Bubble Chart for Clinic Performance
    with st.container():
        st.markdown('<div class="viz-title">6. Multi-Dimensional Clinic Performance Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Comprehensive view of clinic efficiency metrics</div>', unsafe_allow_html=True)
        
        fig6 = px.scatter(
            data['clinics'],
            x='patient_volume',
            y='avg_wait_time',
            size='satisfaction_score',
            color='staff_count',
            hover_name='clinic_name',
            title='Clinic Performance: Volume vs Wait Time (sized by satisfaction)',
            color_continuous_scale='Plasma',
            size_max=60
        )
        fig6.update_layout(height=500)
        st.plotly_chart(fig6, use_container_width=True, theme="streamlit")
    
    # 7. Volcano Plot for Gene Expression
    with st.container():
        st.markdown('<div class="viz-title">7. Genomic Research: Differential Gene Expression</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Volcano plot highlighting significant gene expression changes</div>', unsafe_allow_html=True)
        
        fig7 = px.scatter(
            data['genes'],
            x='log2_fold_change',
            y='neg_log10_p',
            color='significance',
            hover_data=['gene_id'],
            title='Volcano Plot: Differential Gene Expression Analysis',
            color_discrete_map={True: '#e74c3c', False: '#95a5a6'},
            labels={'neg_log10_p': '-log10(p-value)', 'log2_fold_change': 'Log2 Fold Change'}
        )
        fig7.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="red", 
                      annotation_text="Significance Threshold (p=0.05)")
        fig7.update_layout(height=500)
        st.plotly_chart(fig7, use_container_width=True, theme="streamlit")
    
    # 8. Advanced Box Plot with Outliers
    with st.container():
        st.markdown('<div class="viz-title">8. Statistical Distribution Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Box plots showing patient metric distributions by province</div>', unsafe_allow_html=True)
        
        fig8 = px.box(
            data['patients'],
            x='province',
            y='satisfaction_score',
            color='province',
            points='outliers',
            title='Patient Satisfaction Distribution by Province',
            template='seaborn'
        )
        fig8.update_layout(height=500, xaxis_tickangle=45, showlegend=False)
        st.plotly_chart(fig8, use_container_width=True, theme="streamlit")

def create_altair_visualizations(data):
    """Create Altair-based declarative visualizations"""
    
    st.markdown('<h2 class="category-header">📊 Altair Declarative Visualizations</h2>', unsafe_allow_html=True)
    
    # 9. Linked Histograms with Brushing
    with st.container():
        st.markdown('<div class="viz-title">9. Interactive Patient Demographics Explorer</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Linked visualizations with interactive brushing and filtering</div>', unsafe_allow_html=True)
        
        brush = alt.selection_interval(encodings=['x'])
        
        age_hist = alt.Chart(data['patients']).mark_bar(color='steelblue').encode(
            alt.X('age:Q', bin=alt.Bin(step=5), title='Patient Age'),
            alt.Y('count()', title='Number of Patients'),
            tooltip=['count()']
        ).add_params(brush).properties(
            title='Age Distribution (Select to filter)',
            width=300,
            height=200
        )
        
        gender_chart = alt.Chart(data['patients']).mark_bar().encode(
            alt.X('gender:N', title='Gender'),
            alt.Y('count()', title='Number of Patients'),
            color=alt.Color('gender:N', scale=alt.Scale(range=['#1f77b4', '#ff7f0e'])),
            tooltip=['gender:N', 'count()']
        ).transform_filter(brush).properties(
            title='Gender Distribution (Filtered)',
            width=300,
            height=200
        )
        
        combined = alt.hconcat(age_hist, gender_chart).resolve_scale(y='independent')
        st.altair_chart(combined, use_container_width=True, theme="streamlit")
    
    # 10. Stacked Area Chart for Disease Trends
    with st.container():
        st.markdown('<div class="viz-title">10. Disease Prevalence Trends Over Time</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Stacked area visualization showing disease burden evolution</div>', unsafe_allow_html=True)
        
        area_chart = alt.Chart(data['disease_trends']).mark_area().encode(
            x=alt.X('year:T', title='Year'),
            y=alt.Y('patient_count:Q', stack='normalize', title='Proportion of Cases'),
            color=alt.Color('disease:N', 
                          scale=alt.Scale(range=['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'])),
            tooltip=['year:T', 'disease:N', 'patient_count:Q', 'prevalence_rate:Q']
        ).properties(
            title='Disease Prevalence Trends (Normalized)',
            width=600,
            height=400
        )
        st.altair_chart(area_chart, use_container_width=True, theme="streamlit")
    
    # 11. Diverging Bar Chart for Satisfaction Scores
    with st.container():
        st.markdown('<div class="viz-title">11. Patient Satisfaction Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Diverging bar chart showing satisfaction above/below average</div>', unsafe_allow_html=True)
        
        # Calculate province averages
        province_satisfaction = data['patients'].groupby('province')['satisfaction_score'].mean().reset_index()
        overall_avg = data['patients']['satisfaction_score'].mean()
        province_satisfaction['deviation'] = province_satisfaction['satisfaction_score'] - overall_avg
        province_satisfaction['above_average'] = province_satisfaction['deviation'] > 0
        
        diverging_chart = alt.Chart(province_satisfaction).mark_bar().encode(
            x=alt.X('deviation:Q', title='Deviation from Average Satisfaction'),
            y=alt.Y('province:N', sort='-x', title='Province'),
            color=alt.condition(
                alt.datum.above_average,
                alt.value('#2ecc71'),  # Green for above average
                alt.value('#e74c3c')   # Red for below average
            ),
            tooltip=['province:N', 'satisfaction_score:Q', 'deviation:Q']
        ).properties(
            title='Province Satisfaction vs National Average',
            width=500,
            height=300
        )
        st.altair_chart(diverging_chart, use_container_width=True, theme="streamlit")
    
    # 12. Multi-Series Line Chart with Tooltips
    with st.container():
        st.markdown('<div class="viz-title">12. Hospital Operations Multi-Metric Tracker</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Interactive multi-line chart with dynamic tooltips</div>', unsafe_allow_html=True)
        
        # Prepare monthly aggregated data
        ts_monthly = data['time_series'].copy()
        ts_monthly['month'] = ts_monthly['date'].dt.to_period('M').astype(str)
        ts_agg = ts_monthly.groupby('month')[['admissions', 'discharges', 'bed_occupancy']].mean().reset_index()
        ts_melted = ts_agg.melt(id_vars=['month'], var_name='metric', value_name='value')
        
        selector = alt.selection_point(fields=['month'], nearest=True, on='mouseover', empty='none')
        
        lines = alt.Chart(ts_melted).mark_line(point=True).encode(
            x=alt.X('month:T', title='Month'),
            y=alt.Y('value:Q', title='Value'),
            color=alt.Color('metric:N', scale=alt.Scale(range=['#1f77b4', '#ff7f0e', '#2ca02c']))
        ).properties(
            title='Hospital Metrics Trends',
            width=600,
            height=300
        )
        
        points = lines.mark_point().add_params(selector)
        
        text = lines.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(selector, 'value:Q', alt.value(' '))
        )
        
        combined = (lines + points + text).resolve_scale(color='independent')
        st.altair_chart(combined, use_container_width=True, theme="streamlit")

def create_plotly_statistical_visualizations(data):
    """Create statistical visualizations using Plotly (Snowflake compatible)"""
    
    st.markdown('<h2 class="category-header">📈 Statistical Visualizations (Plotly)</h2>', unsafe_allow_html=True)
    
    # 13. Violin Plot for Patient Outcomes (Plotly version)
    with st.container():
        st.markdown('<div class="viz-title">13. Patient Outcome Distribution Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Violin plots showing distribution density of satisfaction scores by gender</div>', unsafe_allow_html=True)
        
        fig13 = px.violin(
            data['patients'], 
            x='gender', 
            y='satisfaction_score',
            color='gender',
            box=True,
            points='outliers',
            title='Patient Satisfaction Score Distribution by Gender',
            color_discrete_map={'Male': '#1f77b4', 'Female': '#ff7f0e'}
        )
        fig13.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig13, use_container_width=True, theme="streamlit")
    
    # 14. Enhanced Correlation Heatmap (already exists - skip duplicate)
    
    # 15. Multi-Variable Scatter Matrix (Plotly version)
    with st.container():
        st.markdown('<div class="viz-title">15. Multi-Variable Health Relationship Explorer</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Comprehensive scatter matrix of patient health metrics</div>', unsafe_allow_html=True)
        
        # Select numeric columns for scatter matrix
        numeric_cols = ['age', 'bmi', 'blood_pressure_systolic', 'cholesterol', 'satisfaction_score']
        sample_data = data['patients'][numeric_cols + ['gender']].sample(500)
        
        fig15 = px.scatter_matrix(
            sample_data,
            dimensions=numeric_cols,
            color='gender',
            title='Patient Health Metrics Scatter Matrix Analysis',
            color_discrete_map={'Male': '#1f77b4', 'Female': '#ff7f0e'}
        )
        fig15.update_layout(height=700, width=700)
        st.plotly_chart(fig15, use_container_width=True, theme="streamlit")
    
    # 16. Enhanced Box Plot with Statistical Annotations (Plotly version)
    with st.container():
        st.markdown('<div class="viz-title">16. Provincial Health Metrics Comparison</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Statistical comparison of BMI distributions across provinces</div>', unsafe_allow_html=True)
        
        fig16 = px.box(
            data['patients'], 
            x='province', 
            y='bmi',
            points='outliers',
            title='BMI Distribution by Province',
            color='province'
        )
        fig16.update_layout(
            height=500, 
            xaxis_tickangle=45,
            showlegend=False
        )
        st.plotly_chart(fig16, use_container_width=True, theme="streamlit")

def create_advanced_plotly_visualizations(data):
    """Create advanced Plotly visualizations"""
    
    st.markdown('<h2 class="category-header">🔬 Advanced Interactive Analytics</h2>', unsafe_allow_html=True)
    
    # 17. Waterfall Chart for Financial Breakdown
    with st.container():
        st.markdown('<div class="viz-title">17. Healthcare Cost Breakdown Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Waterfall chart showing cost component contributions</div>', unsafe_allow_html=True)
        
        # Simulate cost breakdown data
        cost_components = ['Base Cost', 'Staff Costs', 'Equipment', 'Medications', 'Overhead', 'Final Total']
        values = [100000, 45000, 25000, 30000, 15000, 0]  # Final total will be calculated
        values[-1] = sum(values[:-1])  # Calculate total
        
        fig17 = go.Figure(go.Waterfall(
            name="Cost Breakdown",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "relative", "total"],
            x=cost_components,
            textposition="outside",
            text=[f"${v:,.0f}" for v in values],
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#2ecc71"}},
            decreasing={"marker": {"color": "#e74c3c"}},
            totals={"marker": {"color": "#3498db"}}
        ))
        
        fig17.update_layout(
            title="Healthcare Cost Components Waterfall Analysis",
            height=500,
            yaxis_title="Cost (USD)"
        )
        st.plotly_chart(fig17, use_container_width=True, theme="streamlit")
    
    # 18. Radar Chart for Clinic Performance
    with st.container():
        st.markdown('<div class="viz-title">18. Multi-Dimensional Clinic Performance Radar</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Radar chart comparing clinic performance across multiple metrics</div>', unsafe_allow_html=True)
        
        # Select top 3 clinics
        top_clinics = data['clinics'].nlargest(3, 'patient_volume')
        
        # Normalize metrics to 0-100 scale
        metrics = ['patient_volume', 'satisfaction_score', 'staff_count']
        for metric in metrics:
            max_val = top_clinics[metric].max()
            min_val = top_clinics[metric].min()
            top_clinics[f'{metric}_norm'] = ((top_clinics[metric] - min_val) / (max_val - min_val)) * 100
        
        # Invert wait time (lower is better)
        max_wait = top_clinics['avg_wait_time'].max()
        min_wait = top_clinics['avg_wait_time'].min()
        top_clinics['wait_time_norm'] = ((max_wait - top_clinics['avg_wait_time']) / (max_wait - min_wait)) * 100
        
        fig18 = go.Figure()
        
        categories = ['Patient Volume', 'Satisfaction', 'Staff Count', 'Wait Time (inverted)']
        
        for i, row in top_clinics.iterrows():
            values = [
                row['patient_volume_norm'],
                row['satisfaction_score_norm'],
                row['staff_count_norm'],
                row['wait_time_norm']
            ]
            values += values[:1]  # Close the radar chart
            
            fig18.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + categories[:1],
                fill='toself',
                name=row['clinic_name'],
                line=dict(width=2)
            ))
        
        fig18.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Clinic Performance Comparison (Normalized Scores)",
            height=500
        )
        st.plotly_chart(fig18, use_container_width=True, theme="streamlit")
    
    # 19. Animated Bubble Chart
    with st.container():
        st.markdown('<div class="viz-title">19. Dynamic Province Health Evolution</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Animated bubble chart showing health metrics evolution over time</div>', unsafe_allow_html=True)
        
        # Create time-based data for provinces
        provinces = data['patients']['province'].unique()
        years = range(2020, 2025)
        
        animated_data = []
        for year in years:
            for province in provinces:
                province_data = data['patients'][data['patients']['province'] == province]
                animated_data.append({
                    'year': year,
                    'province': province,
                    'avg_satisfaction': province_data['satisfaction_score'].mean() + np.random.normal(0, 0.2),
                    'avg_bmi': province_data['bmi'].mean() + np.random.normal(0, 0.5),
                    'population': len(province_data) * (1 + (year - 2020) * 0.02),  # Simulate growth
                    'health_index': np.random.uniform(60, 95)
                })
        
        animated_df = pd.DataFrame(animated_data)
        
        fig19 = px.scatter(
            animated_df,
            x='avg_satisfaction',
            y='health_index',
            size='population',
            color='province',
            hover_name='province',
            animation_frame='year',
            title='Province Health Metrics Evolution (2020-2024)',
            size_max=60,
            range_x=[6, 9],
            range_y=[50, 100]
        )
        fig19.update_layout(height=500)
        st.plotly_chart(fig19, use_container_width=True, theme="streamlit")
    
    # 20. Treemap Visualization
    with st.container():
        st.markdown('<div class="viz-title">20. Healthcare Resource Allocation Treemap</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Hierarchical view of resource distribution across healthcare system</div>', unsafe_allow_html=True)
        
        # Create hierarchical resource data
        resource_data = []
        categories = ['Emergency', 'Surgery', 'Outpatient', 'ICU']
        subcategories = {
            'Emergency': ['Trauma', 'Cardiac', 'General'],
            'Surgery': ['Orthopedic', 'Cardiac', 'General', 'Neuro'],
            'Outpatient': ['Cardiology', 'Dermatology', 'Family Medicine'],
            'ICU': ['Medical ICU', 'Surgical ICU', 'Cardiac ICU']
        }
        
        for category in categories:
            for subcategory in subcategories[category]:
                resource_data.append({
                    'category': category,
                    'subcategory': subcategory,
                    'budget': np.random.randint(50000, 500000),
                    'utilization': np.random.uniform(0.6, 0.95)
                })
        
        resource_df = pd.DataFrame(resource_data)
        
        fig20 = px.treemap(
            resource_df,
            path=[px.Constant("Healthcare System"), 'category', 'subcategory'],
            values='budget',
            color='utilization',
            color_continuous_scale='RdYlGn',
            title='Healthcare Budget Allocation and Utilization'
        )
        fig20.update_layout(height=600)
        st.plotly_chart(fig20, use_container_width=True, theme="streamlit")

def create_specialty_visualizations(data):
    """Create specialty and experimental visualizations"""
    
    st.markdown('<h2 class="category-header">🎯 Specialty & Experimental Visualizations</h2>', unsafe_allow_html=True)
    
    # 21. Sankey Diagram for Patient Flow
    with st.container():
        st.markdown('<div class="viz-title">21. Patient Flow Through Healthcare System</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Sankey diagram showing patient journey pathways</div>', unsafe_allow_html=True)
        
        # Create Sankey data
        nodes = ['Emergency Dept', 'Admission', 'Surgery', 'ICU', 'General Ward', 'Discharge', 'Transfer']
        
        fig21 = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]
            ),
            link=dict(
                source=[0, 0, 1, 1, 1, 2, 3, 4, 4],
                target=[1, 6, 2, 3, 4, 4, 4, 5, 6],
                value=[300, 50, 120, 80, 100, 90, 70, 200, 30],
                color=["rgba(31, 119, 180, 0.6)"] * 9
            )
        )])
        
        fig21.update_layout(
            title_text="Patient Flow Through Healthcare System",
            font_size=12,
            height=500
        )
        st.plotly_chart(fig21, use_container_width=True, theme="streamlit")
    
    # 22. Gauge Chart for KPIs
    with st.container():
        st.markdown('<div class="viz-title">22. Real-Time Healthcare KPI Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Gauge charts showing critical performance indicators</div>', unsafe_allow_html=True)
        
        # Create gauge subplots
        fig22 = make_subplots(
            rows=2, cols=2,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}]],
            subplot_titles=('Patient Satisfaction', 'Bed Occupancy', 'Staff Efficiency', 'Cost Control')
        )
        
        # Satisfaction gauge
        fig22.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=85,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Satisfaction %"},
            delta={'reference': 80},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "#2ecc71"},
                   'steps': [
                       {'range': [0, 60], 'color': "#e74c3c"},
                       {'range': [60, 80], 'color': "#f39c12"},
                       {'range': [80, 100], 'color': "#2ecc71"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 90}}),
            row=1, col=1)
        
        # Bed occupancy gauge
        fig22.add_trace(go.Indicator(
            mode="gauge+number",
            value=78,
            title={'text': "Bed Occupancy %"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "#3498db"},
                   'steps': [
                       {'range': [0, 50], 'color': "#ecf0f1"},
                       {'range': [50, 85], 'color': "#bdc3c7"},
                       {'range': [85, 100], 'color': "#e74c3c"}]}),
            row=1, col=2)
        
        # Staff efficiency gauge
        fig22.add_trace(go.Indicator(
            mode="gauge+number",
            value=92,
            title={'text': "Staff Efficiency %"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "#9b59b6"}}),
            row=2, col=1)
        
        # Cost control gauge
        fig22.add_trace(go.Indicator(
            mode="gauge+number",
            value=88,
            title={'text': "Cost Control %"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "#f39c12"}}),
            row=2, col=2)
        
        fig22.update_layout(height=600, title_text="Healthcare KPI Dashboard")
        st.plotly_chart(fig22, use_container_width=True, theme="streamlit")
    
    # 23. Funnel Chart for Patient Conversion
    with st.container():
        st.markdown('<div class="viz-title">23. Patient Care Conversion Funnel</div>', unsafe_allow_html=True)
        st.markdown('<div class="viz-description">Funnel analysis showing patient progression through care stages</div>', unsafe_allow_html=True)
        
        stages = ['Initial Consultation', 'Diagnosis', 'Treatment Plan', 'Treatment Start', 'Treatment Complete', 'Follow-up']
        values = [1000, 850, 720, 680, 620, 580]
        
        fig23 = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            textposition="inside",
            textfont=dict(color="white", size=12),
            connector={"line": {"color": "#3498db", "dash": "dot", "width": 3}},
            marker={"color": ["#e74c3c", "#e67e22", "#f39c12", "#2ecc71", "#27ae60", "#16a085"]}
        ))
        
        fig23.update_layout(
            title="Patient Care Journey Conversion Rates",
            height=500
        )
        st.plotly_chart(fig23, use_container_width=True, theme="streamlit")

def main():
    """Main function to run the visualization gallery"""
    
    # Header
    st.markdown('<h1 class="main-header">🎨 Healthcare Visualizations Gallery</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;">
        <p><strong>Showcasing Streamlit's Visual Power</strong> • Competing with Power BI & Tableau</p>
        <p style="font-size: 1rem;">✨ Interactive • 🎯 Professional • 📊 Data-Driven • 🚀 Performance Optimized</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance monitoring
    start_time = time.time()
    
    # Generate sample data
    with st.spinner("🎨 Generating sample healthcare data for visualization gallery..."):
        data = generate_sample_data()
    
    load_time = time.time() - start_time
    create_performance_monitor(load_time, target_time=2.0)
    
    # Statistics about the gallery
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Visualizations", "23", help="Comprehensive gallery of chart types")
    with col2:
        st.metric("Libraries Used", "2", help="Plotly, Altair (Snowflake compatible)")
    with col3:
        st.metric("Sample Data Points", "5,000+", help="Rich synthetic healthcare dataset")
    with col4:
        st.metric("Load Time", f"{load_time:.1f}s", help="Performance optimized for demos")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Plotly Interactive", 
        "📊 Altair Declarative", 
        "📈 Statistical Analysis",
        "🔬 Advanced Analytics",
        "🎯 Specialty Charts"
    ])
    
    with tab1:
        create_plotly_visualizations(data)
    
    with tab2:
        create_altair_visualizations(data)
    
    with tab3:
        create_plotly_statistical_visualizations(data)
    
    with tab4:
        create_advanced_plotly_visualizations(data)
    
    with tab5:
        create_specialty_visualizations(data)
    
    # Footer with technical details
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem;">
        <h4>🏆 Gallery Highlights</h4>
        <p><strong>Interactive Features:</strong> Brushing, Linking, Animations, Hover Details, Selection Events</p>
        <p><strong>Chart Types:</strong> 3D Scatter, Volcano Plots, Sankey Diagrams, Radar Charts, Treemaps, Gauges</p>
        <p><strong>Statistical Analysis:</strong> Correlations, Distributions, Clustering, Anomaly Detection</p>
        <p><strong>Snowflake Compatible:</strong> Uses only Plotly & Altair from Snowflake Anaconda channel</p>
        <p><strong>Professional Aesthetics:</strong> Custom Color Palettes, Typography, Layouts, Themes</p>
        <br>
        <p>🎯 <strong>Demo Purpose:</strong> Showcasing Streamlit's capability to create publication-quality, 
           interactive visualizations that rival dedicated BI tools like Power BI and Tableau</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()