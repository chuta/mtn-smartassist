import pandas as pd
import numpy as np
from typing import Dict, List

class DataProcessor:
    """Utility functions for data processing"""
    
    @staticmethod
    def load_customer_data(file_path: str) -> pd.DataFrame:
        """Load customer data from CSV"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def validate_customer_data(df: pd.DataFrame) -> Dict:
        """Validate customer data format"""
        required_columns = [
            'customer_id', 'tenure_months', 'monthly_spend',
            'data_usage_gb', 'call_minutes', 'complaints', 'last_recharge_days'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {
                'valid': False,
                'error': f"Missing columns: {', '.join(missing_columns)}"
            }
        
        # Check for null values
        null_counts = df[required_columns].isnull().sum()
        if null_counts.any():
            return {
                'valid': False,
                'error': f"Null values found in columns: {null_counts[null_counts > 0].to_dict()}"
            }
        
        return {'valid': True, 'message': 'Data validation passed'}
    
    @staticmethod
    def get_customer_segments(df: pd.DataFrame) -> Dict:
        """Segment customers based on behavior"""
        segments = {}
        
        # Segment by spend
        segments['high_value'] = df[df['monthly_spend'] > df['monthly_spend'].quantile(0.75)]
        segments['medium_value'] = df[(df['monthly_spend'] > df['monthly_spend'].quantile(0.25)) & 
                                       (df['monthly_spend'] <= df['monthly_spend'].quantile(0.75))]
        segments['low_value'] = df[df['monthly_spend'] <= df['monthly_spend'].quantile(0.25)]
        
        # Segment by tenure
        segments['new_customers'] = df[df['tenure_months'] <= 6]
        segments['established_customers'] = df[(df['tenure_months'] > 6) & (df['tenure_months'] <= 24)]
        segments['loyal_customers'] = df[df['tenure_months'] > 24]
        
        return segments
    
    @staticmethod
    def calculate_customer_metrics(df: pd.DataFrame) -> Dict:
        """Calculate aggregate customer metrics"""
        metrics = {
            'total_customers': len(df),
            'avg_tenure': df['tenure_months'].mean(),
            'avg_monthly_spend': df['monthly_spend'].mean(),
            'avg_data_usage': df['data_usage_gb'].mean(),
            'total_complaints': df['complaints'].sum(),
            'avg_complaints': df['complaints'].mean(),
        }
        
        if 'churn' in df.columns:
            metrics['churn_rate'] = df['churn'].mean()
            metrics['churned_customers'] = df['churn'].sum()
        
        if 'churn_probability' in df.columns:
            metrics['avg_churn_risk'] = df['churn_probability'].mean()
            metrics['high_risk_customers'] = len(df[df['churn_probability'] > 0.6])
        
        return metrics
