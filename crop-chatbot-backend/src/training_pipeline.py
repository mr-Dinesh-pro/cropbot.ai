import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import json
import os
from datetime import datetime

class CropModelTrainer:
    def __init__(self, data_path=None):
        self.data_path = data_path or '/home/ubuntu/upload/Crop_recommendation.csv'
        self.model = None
        self.label_encoder = None
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        self.model_path = 'crop_recommendation_model.pkl'
        self.encoder_path = 'label_encoder.pkl'
        self.crop_info_path = 'crop_info.json'
        
    def load_data(self):
        """Load and prepare the training data"""
        try:
            df = pd.read_csv(self.data_path)
            print(f"Loaded dataset with shape: {df.shape}")
            
            # Prepare features and target
            X = df[self.feature_names]
            y = df['label']
            
            return X, y
        except Exception as e:
            print(f"Error loading data: {e}")
            return None, None
    
    def train_model(self, X, y, test_size=0.2, random_state=42):
        """Train the crop recommendation model"""
        try:
            # Encode the target labels
            self.label_encoder = LabelEncoder()
            y_encoded = self.label_encoder.fit_transform(y)
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
            )
            
            # Create and train the model
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=random_state,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2
            )
            
            print("Training the model...")
            self.model.fit(X_train, y_train)
            
            # Evaluate the model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"Model Accuracy: {accuracy:.4f}")
            
            # Cross-validation
            cv_scores = cross_val_score(self.model, X, y_encoded, cv=5)
            print(f"Cross-validation scores: {cv_scores}")
            print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
            
            # Feature importance
            feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
            print("\nFeature Importance:")
            for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
                print(f"{feature}: {importance:.4f}")
            
            return accuracy, cv_scores.mean()
            
        except Exception as e:
            print(f"Error training model: {e}")
            return None, None
    
    def generate_crop_info(self, X, y):
        """Generate detailed crop information for the knowledge base"""
        try:
            df = pd.DataFrame(X, columns=self.feature_names)
            df['label'] = y
            
            crop_info = {}
            for crop in self.label_encoder.classes_:
                crop_data = df[df['label'] == crop]
                crop_info[crop] = {
                    'avg_N': float(crop_data['N'].mean()),
                    'avg_P': float(crop_data['P'].mean()),
                    'avg_K': float(crop_data['K'].mean()),
                    'avg_temperature': float(crop_data['temperature'].mean()),
                    'avg_humidity': float(crop_data['humidity'].mean()),
                    'avg_ph': float(crop_data['ph'].mean()),
                    'avg_rainfall': float(crop_data['rainfall'].mean()),
                    'N_range': [float(crop_data['N'].min()), float(crop_data['N'].max())],
                    'P_range': [float(crop_data['P'].min()), float(crop_data['P'].max())],
                    'K_range': [float(crop_data['K'].min()), float(crop_data['K'].max())],
                    'temperature_range': [float(crop_data['temperature'].min()), float(crop_data['temperature'].max())],
                    'humidity_range': [float(crop_data['humidity'].min()), float(crop_data['humidity'].max())],
                    'ph_range': [float(crop_data['ph'].min()), float(crop_data['ph'].max())],
                    'rainfall_range': [float(crop_data['rainfall'].min()), float(crop_data['rainfall'].max())],
                    'sample_count': len(crop_data)
                }
            
            return crop_info
            
        except Exception as e:
            print(f"Error generating crop info: {e}")
            return {}
    
    def save_model(self):
        """Save the trained model and related files"""
        try:
            if self.model is None or self.label_encoder is None:
                print("No model to save. Train the model first.")
                return False
            
            # Save model and encoder
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.label_encoder, self.encoder_path)
            
            print(f"Model saved to {self.model_path}")
            print(f"Label encoder saved to {self.encoder_path}")
            
            return True
            
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def save_crop_info(self, crop_info):
        """Save crop information to JSON file"""
        try:
            with open(self.crop_info_path, 'w') as f:
                json.dump(crop_info, f, indent=2)
            
            print(f"Crop information saved to {self.crop_info_path}")
            return True
            
        except Exception as e:
            print(f"Error saving crop info: {e}")
            return False
    
    def validate_model(self, X, y):
        """Validate the trained model with additional metrics"""
        try:
            if self.model is None or self.label_encoder is None:
                print("No model to validate. Train the model first.")
                return False
            
            y_encoded = self.label_encoder.transform(y)
            y_pred = self.model.predict(X)
            
            # Classification report
            print("\nClassification Report:")
            print(classification_report(y_encoded, y_pred, target_names=self.label_encoder.classes_))
            
            # Per-class accuracy
            print("\nPer-class accuracy:")
            for i, crop in enumerate(self.label_encoder.classes_):
                crop_mask = y_encoded == i
                if crop_mask.sum() > 0:
                    crop_accuracy = accuracy_score(y_encoded[crop_mask], y_pred[crop_mask])
                    print(f"{crop}: {crop_accuracy:.4f}")
            
            return True
            
        except Exception as e:
            print(f"Error validating model: {e}")
            return False
    
    def retrain_with_new_data(self, new_data_path):
        """Retrain the model with additional data"""
        try:
            # Load existing data
            X_old, y_old = self.load_data()
            if X_old is None:
                return False
            
            # Load new data
            new_df = pd.read_csv(new_data_path)
            X_new = new_df[self.feature_names]
            y_new = new_df['label']
            
            # Combine datasets
            X_combined = pd.concat([X_old, X_new], ignore_index=True)
            y_combined = pd.concat([y_old, y_new], ignore_index=True)
            
            print(f"Combined dataset shape: {X_combined.shape}")
            
            # Retrain the model
            accuracy, cv_accuracy = self.train_model(X_combined, y_combined)
            
            if accuracy is not None:
                # Generate updated crop info
                crop_info = self.generate_crop_info(X_combined, y_combined)
                
                # Save everything
                self.save_model()
                self.save_crop_info(crop_info)
                
                print("Model retrained successfully!")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error retraining model: {e}")
            return False
    
    def full_training_pipeline(self):
        """Complete training pipeline"""
        print("Starting full training pipeline...")
        print("=" * 50)
        
        # Load data
        X, y = self.load_data()
        if X is None:
            return False
        
        # Train model
        accuracy, cv_accuracy = self.train_model(X, y)
        if accuracy is None:
            return False
        
        # Validate model
        self.validate_model(X, y)
        
        # Generate crop info
        crop_info = self.generate_crop_info(X, y)
        
        # Save everything
        model_saved = self.save_model()
        info_saved = self.save_crop_info(crop_info)
        
        if model_saved and info_saved:
            print("\n" + "=" * 50)
            print("Training pipeline completed successfully!")
            print(f"Final accuracy: {accuracy:.4f}")
            print(f"Cross-validation accuracy: {cv_accuracy:.4f}")
            print(f"Number of crops: {len(self.label_encoder.classes_)}")
            return True
        
        return False

def main():
    """Main function to run the training pipeline"""
    trainer = CropModelTrainer()
    success = trainer.full_training_pipeline()
    
    if success:
        print("\nModel training completed successfully!")
    else:
        print("\nModel training failed!")

if __name__ == "__main__":
    main()

