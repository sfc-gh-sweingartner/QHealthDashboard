import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Any, Optional
import time
import numpy as np
from scipy import interpolate

def create_metric_card(title: str, value: str, subtitle: str = ""):
    """Create a styled metric card"""
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="margin:0; color: #1f77b4;">{title}</h3>
        <h2 style="margin:0.2rem 0; color: #333;">{value}</h2>
        <p style="margin:0; color: #666; font-size: 0.9rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def create_performance_monitor(execution_time: float, target_time: float = 3.0):
    """Create performance monitoring badge"""
    if execution_time <= target_time:
        badge_color = "#28a745"
        icon = "🚀"
        status = "Fast"
    elif execution_time <= target_time * 2:
        badge_color = "#ffc107"
        icon = "⚠️"
        status = "Slow"
    else:
        badge_color = "#dc3545"
        icon = "🐌"
        status = "Very Slow"
    
    st.markdown(f"""
    <div style="background: {badge_color}; color: white; padding: 0.5rem 1rem; 
                border-radius: 15px; text-align: center; margin: 1rem 0;">
        {icon} <strong>{status}</strong> - {execution_time:.1f}s 
        (Target: {target_time}s)
    </div>
    """, unsafe_allow_html=True)

def create_kpi_dashboard(metrics: Dict[str, Any], title: str = "Key Performance Indicators"):
    """Create a KPI dashboard with multiple metrics"""
    st.subheader(title)
    
    # Calculate number of columns based on metrics count
    n_metrics = len(metrics)
    n_cols = min(n_metrics, 4)
    cols = st.columns(n_cols)
    
    for i, (key, value) in enumerate(metrics.items()):
        with cols[i % n_cols]:
            # Handle different value types
            if isinstance(value, dict):
                display_value = value.get('value', 'N/A')
                subtitle = value.get('subtitle', '')
                delta = value.get('delta', None)
            else:
                display_value = value
                subtitle = ''
                delta = None
            
            # Format large numbers
            if isinstance(display_value, (int, float)) and display_value > 1000:
                if display_value >= 1_000_000:
                    display_value = f"{display_value/1_000_000:.1f}M"
                elif display_value >= 1_000:
                    display_value = f"{display_value/1_000:.1f}K"
            
            st.metric(
                label=key.replace('_', ' ').title(),
                value=display_value,
                delta=delta,
                help=subtitle
            )

def create_geographic_map(df: pd.DataFrame, location_col: str, value_col: str, title: str):
    """Create a choropleth map for South African provinces"""
    
    # South African province mapping
    province_mapping = {
        'Western Cape': 'ZA-WC',
        'Eastern Cape': 'ZA-EC', 
        'Northern Cape': 'ZA-NC',
        'Free State': 'ZA-FS',
        'KwaZulu-Natal': 'ZA-KN',
        'North West': 'ZA-NW',
        'Gauteng': 'ZA-GP',
        'Mpumalanga': 'ZA-MP',
        'Limpopo': 'ZA-LP'
    }
    
    # Add ISO codes for mapping
    df_map = df.copy()
    df_map['iso_code'] = df_map[location_col].map(province_mapping)
    
    fig = px.choropleth(
        df_map,
        locations='iso_code',
        color=value_col,
        hover_name=location_col,
        hover_data=[value_col],
        title=title,
        color_continuous_scale='Blues',
        scope='africa'
    )
    
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue"
    )
    
    fig.update_layout(height=500)
    return fig

def create_hierarchy_sunburst(df: pd.DataFrame, hierarchy_cols: List[str], value_col: str, title: str):
    """Create a sunburst chart for hierarchical data"""
    
    fig = px.sunburst(
        df,
        path=hierarchy_cols,
        values=value_col,
        title=title,
        color=value_col,
        color_continuous_scale='RdYlBu'
    )
    
    fig.update_layout(
        height=600,
        font_size=12
    )
    
    return fig

def create_trend_analysis(df: pd.DataFrame, date_col: str, value_col: str, 
                         category_col: Optional[str] = None, title: str = "Trend Analysis"):
    """Create time series trend analysis using scipy for trend lines"""
    
    # Convert date column to pandas datetime to ensure compatibility with plotly
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Sort by date for proper trend line calculation
    df = df.sort_values(date_col)
    
    if category_col:
        fig = px.line(
            df,
            x=date_col,
            y=value_col,
            color=category_col,
            title=title,
            markers=True
        )
    else:
        fig = px.line(
            df,
            x=date_col,
            y=value_col,
            title=title,
            markers=True
        )
    
    # Add smooth trend line using scipy interpolation instead of statsmodels
    try:
        # Convert dates to numeric for interpolation
        x_numeric = np.arange(len(df))
        y_values = df[value_col].dropna()
        x_values = x_numeric[:len(y_values)]
        
        if len(x_values) > 3:  # Need at least 4 points for interpolation
            # Use scipy's UnivariateSpline for smooth trend line
            spline = interpolate.UnivariateSpline(x_values, y_values, s=len(y_values))
            
            # Generate smooth curve points
            x_smooth = np.linspace(x_values.min(), x_values.max(), len(x_values) * 2)
            y_smooth = spline(x_smooth)
            
            # Map back to datetime for plotting
            date_smooth = pd.date_range(start=df[date_col].min(), end=df[date_col].max(), periods=len(x_smooth))
            
            # Add trend line to figure
            fig.add_trace(
                go.Scatter(
                    x=date_smooth,
                    y=y_smooth,
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', width=2, dash='dash'),
                    hovertemplate='Trend: %{y:.2f}<extra></extra>'
                )
            )
    except Exception:
        # If trend line calculation fails, continue without it
        pass
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title=value_col.replace('_', ' ').title()
    )
    
    return fig

def create_provider_performance_chart(df: pd.DataFrame, title: str = "Provider Performance Analysis"):
    """Create provider performance comparison chart"""
    
    # Create subplot with secondary y-axis
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Claims Volume", "Average Cost", "Geographic Distribution", "Performance Score"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Volume chart
    top_providers = df.nlargest(10, 'total_claims')
    fig.add_trace(
        go.Bar(x=top_providers['provider_name'], y=top_providers['total_claims'], name="Claims"),
        row=1, col=1
    )
    
    # Cost chart
    fig.add_trace(
        go.Bar(x=top_providers['provider_name'], y=top_providers['avg_cost'], name="Avg Cost"),
        row=1, col=2
    )
    
    # Geographic distribution
    if 'province' in df.columns:
        province_counts = df.groupby('province')['total_claims'].sum().reset_index()
        fig.add_trace(
            go.Pie(labels=province_counts['province'], values=province_counts['total_claims'], name="Geographic"),
            row=2, col=1
        )
    
    # Performance score (efficiency metric)
    if 'efficiency_score' in df.columns:
        fig.add_trace(
            go.Scatter(x=top_providers['total_claims'], y=top_providers['efficiency_score'], 
                      mode='markers', marker=dict(size=10), name="Efficiency"),
            row=2, col=2
        )
    
    fig.update_layout(height=800, title_text=title, showlegend=True)
    return fig

def create_financial_breakdown(df: pd.DataFrame, amount_cols: List[str], title: str = "Financial Breakdown"):
    """Create financial breakdown visualization"""
    
    # Calculate totals for each amount column
    totals = {col: df[col].sum() for col in amount_cols if col in df.columns}
    
    # Create pie chart
    fig = go.Figure(data=[
        go.Pie(
            labels=list(totals.keys()),
            values=list(totals.values()),
            hole=0.4,
            textinfo='label+percent',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=title,
        height=500,
        annotations=[dict(text='Financial<br>Breakdown', x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    return fig

def create_anomaly_detection_chart(df: pd.DataFrame, value_col: str, threshold: float = 2.0):
    """Create anomaly detection visualization using statistical methods"""
    
    # Calculate statistical thresholds
    mean_val = df[value_col].mean()
    std_val = df[value_col].std()
    upper_threshold = mean_val + (threshold * std_val)
    lower_threshold = mean_val - (threshold * std_val)
    
    # Identify anomalies
    df['is_anomaly'] = (df[value_col] > upper_threshold) | (df[value_col] < lower_threshold)
    
    # Create scatter plot
    fig = px.scatter(
        df,
        x=df.index,
        y=value_col,
        color='is_anomaly',
        color_discrete_map={True: 'red', False: 'blue'},
        title=f"Anomaly Detection - {value_col.replace('_', ' ').title()}",
        labels={'is_anomaly': 'Anomaly Status'}
    )
    
    # Add threshold lines
    fig.add_hline(y=upper_threshold, line_dash="dash", line_color="red", 
                  annotation_text=f"Upper Threshold ({threshold}σ)")
    fig.add_hline(y=lower_threshold, line_dash="dash", line_color="red",
                  annotation_text=f"Lower Threshold ({threshold}σ)")
    fig.add_hline(y=mean_val, line_dash="dot", line_color="green",
                  annotation_text="Mean")
    
    fig.update_layout(height=500)
    return fig

def display_data_table(df: pd.DataFrame, title: str = "Data Table", max_rows: int = 100):
    """Display data table with formatting and download option"""
    
    st.subheader(title)
    
    # Show basic stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        if len(df) > max_rows:
            st.warning(f"Showing first {max_rows} rows")
        else:
            st.success("All rows shown")
    
    # Display table
    display_df = df.head(max_rows)
    st.dataframe(display_df, use_container_width=True)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"{title.lower().replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )