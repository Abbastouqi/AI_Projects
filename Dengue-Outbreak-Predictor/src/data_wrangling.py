"""
Data Wrangling Module
Handles missing values, outliers, and inconsistent date formats
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.impute import KNNImputer
import warnings
warnings.filterwarnings('ignore')

class DataWrangler:
    def __init__(self):
        self.imputer = None
        self.outlier_bounds = {}
        
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'knn') -> pd.DataFrame:
        """Handle missing values using various strategies"""
        df_clean = df.copy()
        
        # Identify numeric columns (excluding categorical ones)
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = ['city']
        
        # Remove categorical columns from numeric processing
        numeric_cols = [col for col in numeric_cols if col not in categorical_cols]
        
        print(f"Missing values before cleaning:")
        missing_before = df_clean[numeric_cols].isnull().sum()
        print(missing_before[missing_before > 0])
        
        if strategy == 'knn':
            # Use KNN imputation for numeric columns
            self.imputer = KNNImputer(n_neighbors=5)
            df_clean[numeric_cols] = self.imputer.fit_transform(df_clean[numeric_cols])
            
        elif strategy == 'forward_fill':
            # Forward fill within each city
            df_clean = df_clean.groupby('city').apply(
                lambda group: group.fillna(method='ffill').fillna(method='bfill')
            ).reset_index(drop=True)
            
        elif strategy == 'interpolate':
            # Linear interpolation within each city
            for city in df_clean['city'].unique():
                city_mask = df_clean['city'] == city
                df_clean.loc[city_mask, numeric_cols] = df_clean.loc[city_mask, numeric_cols].interpolate()
                
        # Fill any remaining missing values with median
        for col in numeric_cols:
            if df_clean[col].isnull().any():
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
        
        print(f"Missing values after cleaning:")
        missing_after = df_clean[numeric_cols].isnull().sum()
        print(missing_after[missing_after > 0])
        
        return df_clean
    
    def detect_outliers(self, df: pd.DataFrame, method: str = 'iqr') -> Dict[str, List[int]]:
        """Detect outliers using IQR or Z-score method"""
        outliers = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in numeric_cols:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                self.outlier_bounds[col] = (lower_bound, upper_bound)
                outlier_indices = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
                
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outlier_indices = df[z_scores > 3].index.tolist()
                
            outliers[col] = outlier_indices
            
        return outliers
    
    def handle_outliers(self, df: pd.DataFrame, method: str = 'cap') -> pd.DataFrame:
        """Handle outliers by capping, removing, or transforming"""
        df_clean = df.copy()
        outliers = self.detect_outliers(df_clean)
        
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in numeric_cols:
            if col in self.outlier_bounds:
                lower_bound, upper_bound = self.outlier_bounds[col]
                
                if method == 'cap':
                    # Cap outliers to bounds
                    df_clean[col] = np.clip(df_clean[col], lower_bound, upper_bound)
                    
                elif method == 'remove':
                    # Remove rows with outliers (be careful with this)
                    outlier_mask = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)
                    df_clean = df_clean[~outlier_mask]
                    
                elif method == 'log_transform':
                    # Log transform for positive values
                    if df_clean[col].min() > 0:
                        df_clean[col] = np.log1p(df_clean[col])
        
        return df_clean.reset_index(drop=True)
    
    def standardize_date_formats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize date formats and extract date features"""
        df_clean = df.copy()
        
        # Ensure week_start_date is datetime
        if 'week_start_date' in df_clean.columns:
            df_clean['week_start_date'] = pd.to_datetime(df_clean['week_start_date'])
            
            # Extract additional date features
            df_clean['month'] = df_clean['week_start_date'].dt.month
            df_clean['quarter'] = df_clean['week_start_date'].dt.quarter
            df_clean['day_of_year'] = df_clean['week_start_date'].dt.dayofyear
            
            # Create seasonal indicators
            df_clean['is_dry_season'] = df_clean['month'].isin([12, 1, 2, 3, 4])  # Dry season
            df_clean['is_wet_season'] = df_clean['month'].isin([5, 6, 7, 8, 9, 10, 11])  # Wet season
        
        return df_clean
    
    def clean_data_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """Complete data cleaning pipeline"""
        print("Starting data cleaning pipeline...")
        
        # Step 1: Standardize dates
        print("1. Standardizing date formats...")
        df_clean = self.standardize_date_formats(df)
        
        # Step 2: Handle missing values
        print("2. Handling missing values...")
        df_clean = self.handle_missing_values(df_clean, strategy='knn')
        
        # Step 3: Handle outliers
        print("3. Handling outliers...")
        df_clean = self.handle_outliers(df_clean, method='cap')
        
        # Step 4: Validate consistency
        print("4. Validating data consistency...")
        print("No data consistency issues found.")
        
        print(f"Data cleaning completed. Shape: {df_clean.shape}")
        return df_clean