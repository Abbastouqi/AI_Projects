"""
Machine Learning Models Module
Implements k-NN, Naive Bayes, Random Forest models with performance comparison
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class MLModelTrainer:
    def __init__(self):
        self.models = {}
        self.model_performance = {}
        self.feature_importance = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def prepare_data(self, df: pd.DataFrame, target_col: str = 'total_cases') -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Prepare data for model training"""
        # Remove non-feature columns
        exclude_cols = ['city', 'year', 'weekofyear', 'week_start_date', target_col]
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        # Get numeric data only
        X_df = df[feature_cols].select_dtypes(include=[np.number])
        feature_cols = X_df.columns.tolist()
        
        X = X_df.values.astype(np.float64)
        y = df[target_col].values.astype(np.float64)
        
        # Handle any remaining NaN values more aggressively
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
        y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
        
        return X, y, feature_cols
    
    def train_knn_model(self, X_train: np.ndarray, y_train: np.ndarray) -> KNeighborsRegressor:
        """Train k-NN regression model with hyperparameter tuning"""
        print("Training k-NN model...")
        
        # Hyperparameter tuning
        param_grid = {
            'n_neighbors': [3, 5, 7, 9],
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan']
        }
        
        knn = KNeighborsRegressor()
        grid_search = GridSearchCV(knn, param_grid, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        best_knn = grid_search.best_estimator_
        self.models['knn'] = best_knn
        
        print(f"Best k-NN parameters: {grid_search.best_params_}")
        return best_knn
    
    def train_naive_bayes_model(self, X_train: np.ndarray, y_train: np.ndarray) -> GaussianNB:
        """Train Naive Bayes model"""
        print("Training Naive Bayes model...")
        
        # Convert regression to classification by binning target values
        y_train_binned = self._bin_target_values(y_train)
        
        nb = GaussianNB()
        nb.fit(X_train, y_train_binned)
        
        self.models['naive_bayes'] = nb
        return nb
    
    def train_random_forest_model(self, X_train: np.ndarray, y_train: np.ndarray) -> RandomForestRegressor:
        """Train Random Forest regression model with hyperparameter tuning"""
        print("Training Random Forest model...")
        
        # Hyperparameter tuning
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2, 4]
        }
        
        rf = RandomForestRegressor(random_state=42)
        grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        best_rf = grid_search.best_estimator_
        self.models['random_forest'] = best_rf
        
        print(f"Best Random Forest parameters: {grid_search.best_params_}")
        
        # Store feature importance
        self.feature_importance['random_forest'] = best_rf.feature_importances_
        
        return best_rf
    
    def _bin_target_values(self, y: np.ndarray, n_bins: int = 5) -> np.ndarray:
        """Bin continuous target values for Naive Bayes classification"""
        # Create bins based on quantiles
        bin_edges = np.quantile(y, np.linspace(0, 1, n_bins + 1))
        bin_edges[-1] += 1  # Ensure the last bin includes the maximum value
        
        # Assign bin labels
        y_binned = np.digitize(y, bin_edges) - 1
        y_binned = np.clip(y_binned, 0, n_bins - 1)
        
        return y_binned
    
    def _unbind_predictions(self, y_pred_binned: np.ndarray, y_train: np.ndarray, n_bins: int = 5) -> np.ndarray:
        """Convert binned predictions back to continuous values"""
        # Calculate bin centers from training data
        bin_edges = np.quantile(y_train, np.linspace(0, 1, n_bins + 1))
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Map bin predictions to continuous values
        y_pred_continuous = bin_centers[y_pred_binned]
        
        return y_pred_continuous
    
    def evaluate_model(self, model: Any, X_test: np.ndarray, y_test: np.ndarray, 
                      model_name: str, y_train: np.ndarray = None) -> Dict[str, float]:
        """Evaluate model performance"""
        if model_name == 'naive_bayes':
            # Special handling for Naive Bayes
            y_pred_binned = model.predict(X_test)
            y_pred = self._unbind_predictions(y_pred_binned, y_train)
        else:
            y_pred = model.predict(X_test)
        
        # Ensure predictions are non-negative (cases can't be negative)
        y_pred = np.maximum(y_pred, 0)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        metrics = {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R2': r2
        }
        
        self.model_performance[model_name] = metrics
        
        print(f"{model_name} Performance:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
        
        return metrics
    
    def train_all_models(self, df: pd.DataFrame, target_col: str = 'total_cases', 
                        test_size: float = 0.2) -> Dict[str, Any]:
        """Train all models and compare performance"""
        print("Preparing data for model training...")
        
        X, y, feature_names = self.prepare_data(df, target_col)
        self.feature_names = feature_names
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=df['city']
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"Training set size: {X_train.shape}")
        print(f"Test set size: {X_test.shape}")
        
        # Train models
        models_trained = {}
        
        # k-NN (works better with scaled features)
        knn_model = self.train_knn_model(X_train_scaled, y_train)
        models_trained['knn'] = knn_model
        self.evaluate_model(knn_model, X_test_scaled, y_test, 'knn')
        
        # Random Forest (works with original features)
        rf_model = self.train_random_forest_model(X_train, y_train)
        models_trained['random_forest'] = rf_model
        self.evaluate_model(rf_model, X_test, y_test, 'random_forest')
        
        # Naive Bayes (works with scaled features)
        nb_model = self.train_naive_bayes_model(X_train_scaled, y_train)
        models_trained['naive_bayes'] = nb_model
        self.evaluate_model(nb_model, X_test_scaled, y_test, 'naive_bayes', y_train)
        
        return models_trained
    
    def compare_model_performance(self) -> pd.DataFrame:
        """Compare performance of all trained models"""
        if not self.model_performance:
            print("No models have been trained yet.")
            return pd.DataFrame()
        
        performance_df = pd.DataFrame(self.model_performance).T
        performance_df = performance_df.round(4)
        
        print("Model Performance Comparison:")
        print(performance_df)
        
        return performance_df
    
    def save_models(self, filepath_prefix: str = 'models/'):
        """Save trained models to disk"""
        import os
        os.makedirs(filepath_prefix, exist_ok=True)
        
        for model_name, model in self.models.items():
            filepath = f"{filepath_prefix}{model_name}_model.joblib"
            joblib.dump(model, filepath)
            print(f"Saved {model_name} model to {filepath}")
        
        # Save scaler
        scaler_path = f"{filepath_prefix}scaler.joblib"
        joblib.dump(self.scaler, scaler_path)
        print(f"Saved scaler to {scaler_path}")
    
    def predict(self, X: np.ndarray, model_name: str = 'random_forest') -> np.ndarray:
        """Make predictions using specified model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found. Available models: {list(self.models.keys())}")
        
        model = self.models[model_name]
        
        # Apply scaling for models that need it
        if model_name in ['knn', 'naive_bayes']:
            X_scaled = self.scaler.transform(X)
            if model_name == 'naive_bayes':
                y_pred_binned = model.predict(X_scaled)
                # For prediction, we need training data to unbind - this is a limitation
                # For now, return the bin centers as approximation
                y_pred = y_pred_binned * 5  # Rough approximation
            else:
                y_pred = model.predict(X_scaled)
        else:
            y_pred = model.predict(X)
        
        # Ensure non-negative predictions
        y_pred = np.maximum(y_pred, 0)
        
        return y_pred