import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import joblib
import os

class ChurnPredictor:
    """Churn prediction model using Gradient Boosting"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'tenure_months', 'monthly_spend', 'data_usage_gb',
            'call_minutes', 'complaints', 'last_recharge_days'
        ]
        self.model_path = 'models/churn_model.pkl'
        self.scaler_path = 'models/scaler.pkl'
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for modeling"""
        # Create derived features
        df = df.copy()
        df['spend_per_month'] = df['monthly_spend'] / (df['tenure_months'] + 1)
        df['data_per_month'] = df['data_usage_gb'] / (df['tenure_months'] + 1)
        df['complaint_rate'] = df['complaints'] / (df['tenure_months'] + 1)
        df['recharge_frequency'] = df['tenure_months'] / (df['last_recharge_days'] + 1)
        
        return df
    
    def train(self, data_file: str = 'data/customer_data.csv'):
        """Train the churn prediction model"""
        # Load data
        df = pd.read_csv(data_file)
        
        # Prepare features
        df = self.prepare_features(df)
        
        # Define feature columns including derived features
        all_features = self.feature_columns + [
            'spend_per_month', 'data_per_month', 
            'complaint_rate', 'recharge_frequency'
        ]
        
        X = df[all_features]
        y = df['churn']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        metrics = {
            'auc': auc_score,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'feature_importance': dict(zip(all_features, self.model.feature_importances_))
        }
        
        # Save model
        self.save_model()
        
        return metrics
    
    def predict(self, customer_data: pd.DataFrame) -> pd.DataFrame:
        """Predict churn probability for customers"""
        if self.model is None:
            self.load_model()
        
        # Prepare features
        df = self.prepare_features(customer_data)
        
        # Get all features
        all_features = self.feature_columns + [
            'spend_per_month', 'data_per_month',
            'complaint_rate', 'recharge_frequency'
        ]
        
        X = df[all_features]
        X_scaled = self.scaler.transform(X)
        
        # Predict
        churn_proba = self.model.predict_proba(X_scaled)[:, 1]
        churn_pred = self.model.predict(X_scaled)
        
        # Add predictions to dataframe
        result = customer_data.copy()
        result['churn_probability'] = churn_proba
        result['churn_prediction'] = churn_pred
        result['risk_level'] = pd.cut(
            churn_proba,
            bins=[0, 0.3, 0.6, 1.0],
            labels=['Low', 'Medium', 'High']
        )
        
        return result
    
    def save_model(self):
        """Save trained model and scaler"""
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
    
    def load_model(self):
        """Load trained model and scaler"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        return False
    
    def get_feature_importance(self) -> dict:
        """Get feature importance from trained model"""
        if self.model is None:
            return {}
        
        all_features = self.feature_columns + [
            'spend_per_month', 'data_per_month',
            'complaint_rate', 'recharge_frequency'
        ]
        
        importance = dict(zip(all_features, self.model.feature_importances_))
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

if __name__ == "__main__":
    predictor = ChurnPredictor()
    print("Training churn prediction model...")
    metrics = predictor.train()
    print(f"\nModel Performance:")
    print(f"AUC Score: {metrics['auc']:.4f}")
    print(f"\nClassification Report:\n{metrics['classification_report']}")
    print(f"\nFeature Importance:")
    for feature, importance in sorted(metrics['feature_importance'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {feature}: {importance:.4f}")
