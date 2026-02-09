"""
Streamlit Dashboard Module
Creates interactive dashboard showing risk maps and predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Import our modules
try:
    from data_collection import DataCollector
    from data_wrangling import DataWrangler
    from feature_engineering import FeatureEngineer
    from ml_models import MLModelTrainer
    from anomaly_detection import AnomalyDetector
except ImportError:
    st.error("Please run 'python main.py' first to generate the required data and models.")
    st.stop()

class DengueDashboard:
    def __init__(self):
        self.data_collector = DataCollector()
        self.data_wrangler = DataWrangler()
        self.feature_engineer = FeatureEngineer()
        self.ml_trainer = MLModelTrainer()
        self.anomaly_detector = AnomalyDetector()
        
        # City coordinates for mapping
        self.city_coords = {
            'sj': {'lat': 18.4655, 'lon': -66.1057, 'name': 'San Juan'},
            'iq': {'lat': -3.7437, 'lon': -73.2516, 'name': 'Iquitos'}
        }
    
    def load_and_process_data(self):
        """Load and process data for dashboard"""
        if 'processed_data' not in st.session_state:
            with st.spinner('Loading and processing data...'):
                try:
                    # Load raw data
                    train_features, train_labels, test_features = self.data_collector.load_raw_data()
                    
                    # Merge training data
                    merged_data = self.data_collector.merge_training_data(train_features, train_labels)
                    
                    # Clean data
                    clean_data = self.data_wrangler.clean_data_pipeline(merged_data)
                    
                    # Engineer features
                    processed_data = self.feature_engineer.feature_engineering_pipeline(clean_data)
                    
                    # Detect anomalies
                    anomaly_data = self.anomaly_detector.comprehensive_anomaly_detection(processed_data)
                    
                    st.session_state.processed_data = anomaly_data
                    st.session_state.test_features = test_features
                except Exception as e:
                    st.error(f"Error processing data: {e}")
                    st.stop()
        
        return st.session_state.processed_data, st.session_state.test_features
    
    def create_time_series_plot(self, df: pd.DataFrame, city: str = None):
        """Create interactive time series plot"""
        if city:
            plot_data = df[df['city'] == city].copy()
            title = f'Dengue Cases Over Time - {self.city_coords.get(city, {}).get("name", city)}'
        else:
            plot_data = df.copy()
            title = 'Dengue Cases Over Time - All Cities'
        
        plot_data = plot_data.sort_values(['year', 'weekofyear'])
        
        fig = go.Figure()
        
        if city:
            # Single city plot
            fig.add_trace(go.Scatter(
                x=plot_data['week_start_date'],
                y=plot_data['total_cases'],
                mode='lines+markers',
                name='Cases',
                line=dict(color='blue', width=2),
                marker=dict(size=4)
            ))
            
            # Highlight anomalies
            if 'is_anomaly_combined' in plot_data.columns:
                anomalies = plot_data[plot_data['is_anomaly_combined']]
                if len(anomalies) > 0:
                    fig.add_trace(go.Scatter(
                        x=anomalies['week_start_date'],
                        y=anomalies['total_cases'],
                        mode='markers',
                        name='Anomalies',
                        marker=dict(color='red', size=8, symbol='diamond')
                    ))
        else:
            # Multi-city plot
            for city_code in plot_data['city'].unique():
                city_data = plot_data[plot_data['city'] == city_code]
                city_name = self.city_coords.get(city_code, {}).get('name', city_code)
                
                fig.add_trace(go.Scatter(
                    x=city_data['week_start_date'],
                    y=city_data['total_cases'],
                    mode='lines+markers',
                    name=city_name,
                    line=dict(width=2),
                    marker=dict(size=4)
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Total Cases',
            hovermode='x unified',
            height=500
        )
        
        return fig
    
    def run_dashboard(self):
        """Main dashboard function"""
        st.set_page_config(
            page_title="Dengue Outbreak Predictor",
            page_icon="🦟",
            layout="wide"
        )
        
        st.title("🦟 Dengue Outbreak Predictor Dashboard")
        st.markdown("Real-time dengue fever outbreak prediction and risk assessment")
        
        # Load data
        df, test_df = self.load_and_process_data()
        
        # Sidebar
        st.sidebar.header("Dashboard Controls")
        
        # City selection
        cities = df['city'].unique()
        city_names = [self.city_coords.get(city, {}).get('name', city) for city in cities]
        city_options = dict(zip(city_names, cities))
        
        selected_city_name = st.sidebar.selectbox(
            "Select City",
            ["All Cities"] + city_names
        )
        
        selected_city = city_options.get(selected_city_name) if selected_city_name != "All Cities" else None
        
        # Date range
        min_date = df['week_start_date'].min()
        max_date = df['week_start_date'].max()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Filter data based on selections
        filtered_df = df.copy()
        if selected_city:
            filtered_df = filtered_df[filtered_df['city'] == selected_city]
        
        if len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['week_start_date'] >= pd.to_datetime(date_range[0])) &
                (filtered_df['week_start_date'] <= pd.to_datetime(date_range[1]))
            ]
        
        # Main dashboard tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview", "📈 Time Series", "🔍 Anomalies", "📋 Data"
        ])
        
        with tab1:
            st.header("Overview")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_cases = filtered_df['total_cases'].sum()
                st.metric("Total Cases", f"{total_cases:,}")
            
            with col2:
                avg_cases = filtered_df['total_cases'].mean()
                st.metric("Average Cases/Week", f"{avg_cases:.1f}")
            
            with col3:
                if 'is_anomaly_combined' in filtered_df.columns:
                    anomaly_count = filtered_df['is_anomaly_combined'].sum()
                    st.metric("Anomalies Detected", f"{anomaly_count:,}")
                else:
                    st.metric("Anomalies Detected", "N/A")
            
            with col4:
                if 'is_anomaly_combined' in filtered_df.columns:
                    anomaly_rate = (anomaly_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
                    st.metric("Anomaly Rate", f"{anomaly_rate:.1f}%")
                else:
                    st.metric("Anomaly Rate", "N/A")
            
            # Summary statistics
            st.subheader("Summary Statistics")
            summary_stats = filtered_df.groupby('city').agg({
                'total_cases': ['count', 'mean', 'max', 'std']
            }).round(2)
            
            summary_stats.columns = ['Weeks', 'Avg Cases', 'Max Cases', 'Std Cases']
            summary_stats.index = [self.city_coords.get(city, {}).get('name', city) for city in summary_stats.index]
            
            st.dataframe(summary_stats)
        
        with tab2:
            st.header("Time Series Analysis")
            
            # Time series plot
            time_series_fig = self.create_time_series_plot(filtered_df, selected_city)
            st.plotly_chart(time_series_fig, use_container_width=True)
            
            # Seasonal patterns
            st.subheader("Seasonal Patterns")
            if 'month' in filtered_df.columns:
                seasonal_data = filtered_df.groupby(['month', 'city'])['total_cases'].mean().reset_index()
                
                seasonal_fig = px.line(
                    seasonal_data,
                    x='month',
                    y='total_cases',
                    color='city',
                    title='Average Cases by Month',
                    labels={'month': 'Month', 'total_cases': 'Average Cases'}
                )
                st.plotly_chart(seasonal_fig, use_container_width=True)
        
        with tab3:
            st.header("Anomaly Detection")
            
            if 'is_anomaly_combined' in filtered_df.columns:
                # Anomaly summary
                anomaly_summary = {
                    'Total Records': len(filtered_df),
                    'Anomalies Detected': filtered_df['is_anomaly_combined'].sum(),
                    'Anomaly Rate': f"{(filtered_df['is_anomaly_combined'].sum() / len(filtered_df) * 100):.1f}%"
                }
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Records", anomaly_summary['Total Records'])
                with col2:
                    st.metric("Anomalies", anomaly_summary['Anomalies Detected'])
                with col3:
                    st.metric("Anomaly Rate", anomaly_summary['Anomaly Rate'])
                
                # Top anomalies table
                st.subheader("Top Anomalies")
                anomalies = filtered_df[filtered_df['is_anomaly_combined']].copy()
                
                if len(anomalies) > 0:
                    if 'anomaly_score_combined' in anomalies.columns:
                        top_anomalies = anomalies.nlargest(10, 'anomaly_score_combined')
                    else:
                        top_anomalies = anomalies.nlargest(10, 'total_cases')
                    
                    display_cols = ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases']
                    display_cols = [col for col in display_cols if col in top_anomalies.columns]
                    st.dataframe(top_anomalies[display_cols])
                else:
                    st.info("No anomalies detected in the selected data.")
            else:
                st.info("Anomaly detection data not available. Please run the main pipeline first.")
        
        with tab4:
            st.header("Raw Data")
            
            # Data overview
            st.subheader("Dataset Overview")
            st.write(f"**Shape:** {filtered_df.shape[0]} rows × {filtered_df.shape[1]} columns")
            st.write(f"**Date Range:** {filtered_df['week_start_date'].min()} to {filtered_df['week_start_date'].max()}")
            st.write(f"**Cities:** {', '.join([self.city_coords.get(city, {}).get('name', city) for city in filtered_df['city'].unique()])}")
            
            # Display data
            st.subheader("Data Sample")
            display_cols = ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases', 
                          'reanalysis_avg_temp_k', 'reanalysis_relative_humidity_percent', 'precipitation_amt_mm']
            display_cols = [col for col in display_cols if col in filtered_df.columns]
            
            st.dataframe(filtered_df[display_cols].head(100))
        
        # Footer
        st.markdown("---")
        st.markdown("Built with Streamlit • Data from DengAI Competition")

def main():
    dashboard = DengueDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()