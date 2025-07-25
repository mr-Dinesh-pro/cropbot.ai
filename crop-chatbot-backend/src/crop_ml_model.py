import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import json

# Load the dataset
df = pd.read_csv('/home/ubuntu/upload/Crop_recommendation.csv')

# Prepare features and target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# Encode the target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")

# Get feature importance
feature_importance = dict(zip(X.columns, model.feature_importances_))
print("\nFeature Importance:")
for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
    print(f"{feature}: {importance:.4f}")

# Save the model and label encoder
joblib.dump(model, '/home/ubuntu/crop_recommendation_model.pkl')
joblib.dump(label_encoder, '/home/ubuntu/label_encoder.pkl')

# Save crop information for the chatbot
crop_info = {}
for crop in label_encoder.classes_:
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
        'rainfall_range': [float(crop_data['rainfall'].min()), float(crop_data['rainfall'].max())]
    }

with open('/home/ubuntu/crop_info.json', 'w') as f:
    json.dump(crop_info, f, indent=2)

print("\nModel and crop information saved successfully!")

# Function to predict crop
def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    """Predict the best crop for given conditions"""
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    prediction = model.predict(features)[0]
    crop_name = label_encoder.inverse_transform([prediction])[0]
    
    # Get prediction probabilities
    probabilities = model.predict_proba(features)[0]
    top_3_indices = np.argsort(probabilities)[-3:][::-1]
    top_3_crops = [(label_encoder.inverse_transform([idx])[0], probabilities[idx]) for idx in top_3_indices]
    
    return crop_name, top_3_crops

# Test the prediction function
print("\nTesting prediction function:")
test_crop, top_crops = predict_crop(90, 42, 43, 20.88, 82.00, 6.50, 202.94)
print(f"Predicted crop: {test_crop}")
print("Top 3 recommendations:")
for crop, prob in top_crops:
    print(f"  {crop}: {prob:.4f}")

print(f"\nModel training complete. Accuracy: {accuracy:.4f}")

