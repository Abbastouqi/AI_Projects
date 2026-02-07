"""
Data Collection Module
Handles merging climate data with case reports and database operations
"""

import pandas as pd
import sqlite3
import os
from typing import Tuple, Optional

class DataCollector:
    def __init__(self, db_path: str = "dengue_data.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect_db(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def close_db(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def load_raw_data(self, data_dir: str = "archive (4)") -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load raw training and test data"""
        train_features = pd.read_csv(f"{data_dir}/DengAI_Predicting_Disease_Spread_-_Training_Data_Features.csv")
        train_labels = pd.read_csv(f"{data_dir}/DengAI_Predicting_Disease_Spread_-_Training_Data_Labels.csv")
        test_features = pd.read_csv(f"{data_dir}/DengAI_Predicting_Disease_Spread_-_Test_Data_Features.csv")
        
        return train_features, train_labels, test_features
    
    def merge_training_data(self, features_df: pd.DataFrame, labels_df: pd.DataFrame) -> pd.DataFrame:
        """Merge climate features with case reports"""
        merged_df = pd.merge(
            features_df, 
            labels_df, 
            on=['city', 'year', 'weekofyear'], 
            how='inner'
        )
        
        # Convert week_start_date to datetime
        merged_df['week_start_date'] = pd.to_datetime(merged_df['week_start_date'])
        
        return merged_df
    
    def create_database_schema(self):
        """Create database tables"""
        self.connect_db()
        
        # Create main data table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS dengue_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            year INTEGER NOT NULL,
            weekofyear INTEGER NOT NULL,
            week_start_date DATE,
            ndvi_ne REAL,
            ndvi_nw REAL,
            ndvi_se REAL,
            ndvi_sw REAL,
            precipitation_amt_mm REAL,
            reanalysis_air_temp_k REAL,
            reanalysis_avg_temp_k REAL,
            reanalysis_dew_point_temp_k REAL,
            reanalysis_max_air_temp_k REAL,
            reanalysis_min_air_temp_k REAL,
            reanalysis_precip_amt_kg_per_m2 REAL,
            reanalysis_relative_humidity_percent REAL,
            reanalysis_sat_precip_amt_mm REAL,
            reanalysis_specific_humidity_g_per_kg REAL,
            reanalysis_tdtr_k REAL,
            station_avg_temp_c REAL,
            station_diur_temp_rng_c REAL,
            station_max_temp_c REAL,
            station_min_temp_c REAL,
            station_precip_mm REAL,
            total_cases INTEGER,
            UNIQUE(city, year, weekofyear)
        );
        """
        
        self.conn.execute(create_table_sql)
        self.conn.commit()
        
    def store_data_to_db(self, df: pd.DataFrame):
        """Store merged data to SQLite database"""
        if self.conn is None:
            self.connect_db()
            
        df.to_sql('dengue_data', self.conn, if_exists='replace', index=False)
        self.conn.commit()
        
    def extract_features_by_region_month(self, city: Optional[str] = None, 
                                       year: Optional[int] = None, 
                                       month: Optional[int] = None) -> pd.DataFrame:
        """Extract features by region and month using SQL queries"""
        if self.conn is None:
            self.connect_db()
            
        base_query = """
        SELECT city, year, 
               CAST(strftime('%m', week_start_date) AS INTEGER) as month,
               AVG(reanalysis_avg_temp_k) as avg_temp,
               AVG(reanalysis_relative_humidity_percent) as avg_humidity,
               AVG(precipitation_amt_mm) as avg_precipitation,
               SUM(total_cases) as total_cases,
               COUNT(*) as weeks_count
        FROM dengue_data
        WHERE 1=1
        """
        
        params = []
        if city:
            base_query += " AND city = ?"
            params.append(city)
        if year:
            base_query += " AND year = ?"
            params.append(year)
        if month:
            base_query += " AND CAST(strftime('%m', week_start_date) AS INTEGER) = ?"
            params.append(month)
            
        base_query += " GROUP BY city, year, month ORDER BY city, year, month"
        
        return pd.read_sql_query(base_query, self.conn, params=params)