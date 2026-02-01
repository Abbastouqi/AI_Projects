"""
Anomaly Detection Module
Flags unusual spikes that might indicate outbreaks
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class AnomalyDetector:
    def __init__(self):
        self.isolation_forest = None
        self.scaler = StandardScaler()
        self.anomaly_threshold = {}
        self.seasonal_baselines = {}
        
    def calculate_seasonal_baseline(self, df: pd.DataFrame, 
                                  target_col: str = 'total_cases') -> Dict[str, Dict[int, float]]:
        """Calculate seasonal baseline for each city and week"""
        baselines = {}
        
        for city in df['city'].unique():
            city_data = df[df['city'] == city].copy()
            city_baselines = {}
            
            for week in range(1, 53):  # Weeks 1-52
                week_data = city_data[city_data['weekofyear'] == week][target_col]
                if len(week_data) > 0:
                    # Use median as baseline (more robust to outliers)
                    baseline = week_data.median()
                    city_baselines[week] = baseline
                else:
                    city_baselines[week] = 0
            
            baselines[city] = city_baselines
        
        self.seasonal_baselines = baselines
        return baselines
    
    def detect_statistical_anomalies(self, df: pd.DataFrame, 
                                   target_col: str = 'total_cases',
                                   method: str = 'modified_zscore',
                                   multiplier: float = 2.0) -> pd.DataFrame:
        """Detect anomalies using statistical methods"""
        df_anomalies = df.copy()
        df_anomalies['is_anomaly_statistical'] = False
        df_anomalies['anomaly_score_statistical'] = 0.0
        
        for city in df['city'].unique():
            city_mask = df_anomalies['city'] == city
            city_data = df_anomalies[city_mask][target_col]
            
            if method == 'iqr':
                Q1 = city_data.quantile(0.25)
                Q3 = city_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - multiplier * IQR
                upper_bound = Q3 + multiplier * IQR
                
                anomaly_mask = (city_data < lower_bound) | (city_data > upper_bound)
                
            elif method == 'zscore':
                z_scores = np.abs((city_data - city_data.mean()) / city_data.std())
                anomaly_mask = z_scores > multiplier
                df_anomalies.loc[city_mask, 'anomaly_score_statistical'] = z_scores
                
            elif method == 'modified_zscore':
                median = city_data.median()
                mad = np.median(np.abs(city_data - median))
                if mad > 0:
                    modified_z_scores = 0.6745 * (city_data - median) / mad
                    anomaly_mask = np.abs(modified_z_scores) > multiplier
                    df_anomalies.loc[city_mask, 'anomaly_score_statistical'] = np.abs(modified_z_scores)
                else:
                    anomaly_mask = pd.Series([False] * len(city_data), index=city_data.index)
            
            df_anomalies.loc[city_mask, 'is_anomaly_statistical'] = anomaly_mask
        
        return df_anomalies
    
    def detect_seasonal_anomalies(self, df: pd.DataFrame, 
                                target_col: str = 'total_cases',
                                threshold_multiplier: float = 3.0) -> pd.DataFrame:
        """Detect anomalies based on seasonal patterns"""
        if not self.seasonal_baselines:
            self.calculate_seasonal_baseline(df, target_col)
        
        df_anomalies = df.copy()
        df_anomalies['is_anomaly_seasonal'] = False
        df_anomalies['seasonal_baseline'] = 0.0
        df_anomalies['seasonal_deviation'] = 0.0
        
        for idx, row in df_anomalies.iterrows():
            city = row['city']
            week = row['weekofyear']
            actual_cases = row[target_col]
            
            if city in self.seasonal_baselines and week in self.seasonal_baselines[city]:
                baseline = self.seasonal_baselines[city][week]
                df_anomalies.loc[idx, 'seasonal_baseline'] = baseline
                
                # Calculate deviation from baseline
                if baseline > 0:
                    deviation = (actual_cases - baseline) / baseline
                else:
                    deviation = actual_cases
                
                df_anomalies.loc[idx, 'seasonal_deviation'] = deviation
                
                # Flag as anomaly if deviation exceeds threshold
                if deviation > threshold_multiplier:
                    df_anomalies.loc[idx, 'is_anomaly_seasonal'] = True
        
        return df_anomalies
    
    def detect_ml_anomalies(self, df: pd.DataFrame, 
                          contamination: float = 0.1) -> pd.DataFrame:
        """Detect anomalies using Isolation Forest"""
        # Prepare features for anomaly detection
        feature_cols = [col for col in df.columns if col not in 
                       ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases']]
        
        X = df[feature_cols].select_dtypes(include=[np.number]).fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        
        anomaly_labels = self.isolation_forest.fit_predict(X_scaled)
        anomaly_scores = self.isolation_forest.score_samples(X_scaled)
        
        df_anomalies = df.copy()
        df_anomalies['is_anomaly_ml'] = anomaly_labels == -1
        df_anomalies['anomaly_score_ml'] = -anomaly_scores  # Convert to positive scores
        
        return df_anomalies
    
    def detect_outbreak_patterns(self, df: pd.DataFrame, 
                               target_col: str = 'total_cases',
                               min_duration: int = 2,
                               min_increase: float = 2.0) -> pd.DataFrame:
        """Detect potential outbreak patterns (sustained increases)"""
        df_outbreaks = df.copy()
        df_outbreaks['is_outbreak_pattern'] = False
        df_outbreaks['outbreak_intensity'] = 0.0
        
        for city in df['city'].unique():
            city_data = df_outbreaks[df_outbreaks['city'] == city].copy()
            city_data = city_data.sort_values(['year', 'weekofyear'])
            
            # Calculate rolling average for comparison
            city_data['rolling_avg'] = city_data[target_col].rolling(window=4, min_periods=1).mean()
            
            outbreak_start = None
            for idx in city_data.index:
                current_cases = city_data.loc[idx, target_col]
                rolling_avg = city_data.loc[idx, 'rolling_avg']
                
                # Check if current cases significantly exceed rolling average
                if rolling_avg > 0 and current_cases > min_increase * rolling_avg:
                    if outbreak_start is None:
                        outbreak_start = idx
                    
                    # Calculate outbreak intensity
                    intensity = current_cases / rolling_avg if rolling_avg > 0 else 1
                    df_outbreaks.loc[idx, 'outbreak_intensity'] = intensity
                    
                else:
                    # Check if we had a sustained outbreak
                    if outbreak_start is not None:
                        outbreak_indices = city_data.loc[outbreak_start:idx].index[:-1]
                        if len(outbreak_indices) >= min_duration:
                            df_outbreaks.loc[outbreak_indices, 'is_outbreak_pattern'] = True
                    
                    outbreak_start = None
        
        return df_outbreaks
    
    def comprehensive_anomaly_detection(self, df: pd.DataFrame, 
                                      target_col: str = 'total_cases') -> pd.DataFrame:
        """Run comprehensive anomaly detection using multiple methods"""
        print("Running comprehensive anomaly detection...")
        
        # Statistical anomalies
        print("1. Detecting statistical anomalies...")
        df_result = self.detect_statistical_anomalies(df, target_col, method='modified_zscore')
        
        # Seasonal anomalies
        print("2. Detecting seasonal anomalies...")
        df_result = self.detect_seasonal_anomalies(df_result, target_col)
        
        # ML-based anomalies
        print("3. Detecting ML-based anomalies...")
        df_result = self.detect_ml_anomalies(df_result)
        
        # Outbreak patterns
        print("4. Detecting outbreak patterns...")
        df_result = self.detect_outbreak_patterns(df_result, target_col)
        
        # Create combined anomaly flag
        df_result['is_anomaly_combined'] = (
            df_result['is_anomaly_statistical'] |
            df_result['is_anomaly_seasonal'] |
            df_result['is_anomaly_ml'] |
            df_result['is_outbreak_pattern']
        )
        
        # Calculate combined anomaly score
        df_result['anomaly_score_combined'] = (
            df_result['anomaly_score_statistical'] +
            df_result['seasonal_deviation'].abs() +
            df_result['anomaly_score_ml'] +
            df_result['outbreak_intensity']
        ) / 4
        
        print(f"Anomaly detection completed. Found {df_result['is_anomaly_combined'].sum()} anomalies.")
        
        return df_result
    
    def get_anomaly_summary(self, df_anomalies: pd.DataFrame) -> Dict[str, int]:
        """Get summary of detected anomalies"""
        summary = {
            'total_records': len(df_anomalies),
            'statistical_anomalies': df_anomalies['is_anomaly_statistical'].sum(),
            'seasonal_anomalies': df_anomalies['is_anomaly_seasonal'].sum(),
            'ml_anomalies': df_anomalies['is_anomaly_ml'].sum(),
            'outbreak_patterns': df_anomalies['is_outbreak_pattern'].sum(),
            'combined_anomalies': df_anomalies['is_anomaly_combined'].sum()
        }
        
        print("Anomaly Detection Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        return summary
    
    def get_top_anomalies(self, df_anomalies: pd.DataFrame, 
                         top_n: int = 10,
                         sort_by: str = 'anomaly_score_combined') -> pd.DataFrame:
        """Get top N anomalies sorted by score"""
        if sort_by not in df_anomalies.columns:
            sort_by = 'total_cases'
        
        top_anomalies = df_anomalies[df_anomalies['is_anomaly_combined']].nlargest(top_n, sort_by)
        
        display_cols = ['city', 'year', 'weekofyear', 'week_start_date', 'total_cases']
        if sort_by in df_anomalies.columns:
            display_cols.append(sort_by)
        
        display_cols = [col for col in display_cols if col in df_anomalies.columns]
        
        print(f"Top {top_n} Anomalies:")
        print(top_anomalies[display_cols])
        
        return top_anomalies