"""
Feature Engineering Module
Creates lag features, rolling averages, and other derived features
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder

class FeatureEngineer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def create_lag_features(self, df: pd.DataFrame, target_col: str = 'total_cases', 
                           lags: List[int] = [1, 2, 3, 4]) -> pd.DataFrame:
        """Create lag features for cases from previous weeks"""
        df_features = df.copy()
        
        # Sort by city and date to ensure proper lag calculation
        df_features = df_features.sort_values(['city', 'year', 'weekofyear'])
        
        for city in df_features['city'].unique():
            city_mask = df_features['city'] == city
            city_data = df_features[city_mask].copy()
            
            for lag in lags:
                lag_col = f'{target_col}_lag_{lag}'
                city_data[lag_col] = city_data[target_col].shift(lag)
                df_features.loc[city_mask, lag_col] = city_data[lag_col]
        
        return df_features
    
    def create_rolling_features(self, df: pd.DataFrame, 
                              columns: List[str] = None, 
                              windows: List[int] = [2, 4, 8]) -> pd.DataFrame:
        """Create rolling average features"""
        df_features = df.copy()
        
        if columns is None:
            # Default columns for rolling features
            columns = [
                'reanalysis_avg_temp_k', 'reanalysis_relative_humidity_percent',
                'precipitation_amt_mm', 'total_cases'
            ]
        
        # Filter columns that exist in the dataframe
        columns = [col for col in columns if col in df_features.columns]
        
        df_features = df_features.sort_values(['city', 'year', 'weekofyear'])
        
        for city in df_features['city'].unique():
            city_mask = df_features['city'] == city
            city_data = df_features[city_mask].copy()
            
            for col in columns:
                for window in windows:
                    rolling_col = f'{col}_rolling_{window}w'
                    city_data[rolling_col] = city_data[col].rolling(window=window, min_periods=1).mean()
                    df_features.loc[city_mask, rolling_col] = city_data[rolling_col]
        
        return df_features
    
    def create_seasonal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create seasonal and cyclical features"""
        df_features = df.copy()
        
        if 'weekofyear' in df_features.columns:
            # Cyclical encoding for week of year
            df_features['week_sin'] = np.sin(2 * np.pi * df_features['weekofyear'] / 52)
            df_features['week_cos'] = np.cos(2 * np.pi * df_features['weekofyear'] / 52)
        
        if 'month' in df_features.columns:
            # Cyclical encoding for month
            df_features['month_sin'] = np.sin(2 * np.pi * df_features['month'] / 12)
            df_features['month_cos'] = np.cos(2 * np.pi * df_features['month'] / 12)
        
        # Temperature-based seasonal indicators
        if 'reanalysis_avg_temp_k' in df_features.columns:
            temp_mean = df_features['reanalysis_avg_temp_k'].mean()
            df_features['temp_above_mean'] = (df_features['reanalysis_avg_temp_k'] > temp_mean).astype(int)
        
        # Precipitation-based seasonal indicators
        if 'precipitation_amt_mm' in df_features.columns:
            precip_75th = df_features['precipitation_amt_mm'].quantile(0.75)
            df_features['high_precipitation'] = (df_features['precipitation_amt_mm'] > precip_75th).astype(int)
        
        return df_features
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features between climate variables"""
        df_features = df.copy()
        
        # Temperature-humidity interaction
        if 'reanalysis_avg_temp_k' in df_features.columns and 'reanalysis_relative_humidity_percent' in df_features.columns:
            df_features['temp_humidity_interaction'] = (
                df_features['reanalysis_avg_temp_k'] * df_features['reanalysis_relative_humidity_percent']
            )
        
        # Temperature-precipitation interaction
        if 'reanalysis_avg_temp_k' in df_features.columns and 'precipitation_amt_mm' in df_features.columns:
            df_features['temp_precip_interaction'] = (
                df_features['reanalysis_avg_temp_k'] * df_features['precipitation_amt_mm']
            )
        
        # NDVI average (vegetation index)
        ndvi_cols = [col for col in df_features.columns if col.startswith('ndvi_')]
        if ndvi_cols:
            df_features['ndvi_avg'] = df_features[ndvi_cols].mean(axis=1)
            df_features['ndvi_std'] = df_features[ndvi_cols].std(axis=1)
        
        # Temperature range features
        if 'reanalysis_max_air_temp_k' in df_features.columns and 'reanalysis_min_air_temp_k' in df_features.columns:
            df_features['temp_range'] = (
                df_features['reanalysis_max_air_temp_k'] - df_features['reanalysis_min_air_temp_k']
            )
        
        return df_features
    
    def encode_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical features"""
        df_features = df.copy()
        
        # Label encode city
        if 'city' in df_features.columns:
            if 'city' not in self.label_encoders:
                self.label_encoders['city'] = LabelEncoder()
                df_features['city_encoded'] = self.label_encoders['city'].fit_transform(df_features['city'])
            else:
                df_features['city_encoded'] = self.label_encoders['city'].transform(df_features['city'])
        
        return df_features
    
    def feature_engineering_pipeline(self, df: pd.DataFrame, 
                                   target_col: str = 'total_cases',
                                   is_training: bool = True) -> pd.DataFrame:
        """Complete feature engineering pipeline"""
        print("Starting feature engineering pipeline...")
        
        df_features = df.copy()
        
        # Step 1: Create lag features (only for training data with target)
        if is_training and target_col in df_features.columns:
            print("1. Creating lag features...")
            df_features = self.create_lag_features(df_features, target_col)
        
        # Step 2: Create rolling features
        print("2. Creating rolling features...")
        df_features = self.create_rolling_features(df_features)
        
        # Step 3: Create seasonal features
        print("3. Creating seasonal features...")
        df_features = self.create_seasonal_features(df_features)
        
        # Step 4: Create interaction features
        print("4. Creating interaction features...")
        df_features = self.create_interaction_features(df_features)
        
        # Step 5: Encode categorical features
        print("6. Encoding categorical features...")
        df_features = self.encode_categorical_features(df_features)
        
        # Step 6: Final cleanup - fill any remaining NaN values
        print("7. Final cleanup...")
        numeric_cols = df_features.select_dtypes(include=[np.number]).columns
        df_features[numeric_cols] = df_features[numeric_cols].fillna(0)
        
        # Replace any infinite values
        df_features = df_features.replace([np.inf, -np.inf], 0)
        
        print(f"Feature engineering completed. Shape: {df_features.shape}")
        return df_features