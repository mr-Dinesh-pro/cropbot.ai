from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import os

crop_bp = Blueprint('crop', __name__)

# Simple crop data without ML dependencies
CROP_DATA = {
    "rice": {
        "name": "Rice",
        "category": "cereal",
        "optimal_conditions": {
            "temperature": "20-35°C",
            "humidity": "80-90%",
            "rainfall": "150-300cm",
            "ph": "5.5-7.0"
        },
        "description": "Rice is a staple food crop that requires high humidity and abundant water."
    },
    "maize": {
        "name": "Maize",
        "category": "cereal", 
        "optimal_conditions": {
            "temperature": "21-27°C",
            "humidity": "60-70%",
            "rainfall": "50-75cm",
            "ph": "6.0-7.5"
        },
        "description": "Maize is a versatile crop that can grow in various climatic conditions."
    },
    "wheat": {
        "name": "Wheat",
        "category": "cereal",
        "optimal_conditions": {
            "temperature": "15-25°C",
            "humidity": "50-60%",
            "rainfall": "30-100cm",
            "ph": "6.0-7.5"
        },
        "description": "Wheat is a major cereal grain and staple food worldwide."
    },
    "cotton": {
        "name": "Cotton",
        "category": "cash_crop",
        "optimal_conditions": {
            "temperature": "21-30°C",
            "humidity": "50-80%",
            "rainfall": "50-100cm",
            "ph": "5.8-8.0"
        },
        "description": "Cotton is an important cash crop used in textile production."
    },
    "apple": {
        "name": "Apple",
        "category": "fruit",
        "optimal_conditions": {
            "temperature": "15-25°C",
            "humidity": "60-70%",
            "rainfall": "100-125cm",
            "ph": "6.0-7.0"
        },
        "description": "Apples are popular fruits that require temperate climate conditions."
    }
}

AGRICULTURAL_ADVICE = {
    "pest": {
        "title": "Pest Management",
        "advice": [
            "Use integrated pest management (IPM) approaches",
            "Encourage beneficial insects and natural predators",
            "Rotate crops to break pest cycles",
            "Use organic pesticides when necessary",
            "Monitor crops regularly for early detection"
        ]
    },
    "fertilizer": {
        "title": "Fertilizer Recommendations",
        "advice": [
            "Test soil before applying fertilizers",
            "Use organic compost and manure when possible",
            "Apply nitrogen for leaf growth",
            "Use phosphorus for root development",
            "Potassium helps with disease resistance"
        ]
    },
    "irrigation": {
        "title": "Irrigation Best Practices",
        "advice": [
            "Water early morning or late evening",
            "Use drip irrigation for water efficiency",
            "Monitor soil moisture levels",
            "Avoid overwatering to prevent root rot",
            "Mulch around plants to retain moisture"
        ]
    }
}

@crop_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Crop recommendation API is running (simplified version)',
        'version': '1.0.0-simple'
    })

@crop_bp.route('/crops', methods=['GET'])
@cross_origin()
def get_crops():
    """Get list of available crops"""
    crops = list(CROP_DATA.keys())
    categories = {}
    
    for crop, data in CROP_DATA.items():
        category = data['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(crop)
    
    return jsonify({
        'success': True,
        'crops': crops,
        'categories': categories,
        'total_crops': len(crops)
    })

@crop_bp.route('/recommend', methods=['POST'])
@cross_origin()
def recommend_crop():
    """Simple crop recommendation based on basic rules"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract values
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])
        
        # Simple rule-based recommendation
        recommendations = []
        
        # Rice conditions
        if (20 <= temperature <= 35 and humidity >= 80 and 
            5.5 <= ph <= 7.0 and rainfall >= 150):
            recommendations.append(('rice', 0.9))
        
        # Maize conditions  
        if (21 <= temperature <= 27 and 60 <= humidity <= 70 and
            6.0 <= ph <= 7.5 and 50 <= rainfall <= 75):
            recommendations.append(('maize', 0.85))
        
        # Wheat conditions
        if (15 <= temperature <= 25 and 50 <= humidity <= 60 and
            6.0 <= ph <= 7.5 and 30 <= rainfall <= 100):
            recommendations.append(('wheat', 0.8))
        
        # Cotton conditions
        if (21 <= temperature <= 30 and 50 <= humidity <= 80 and
            5.8 <= ph <= 8.0 and 50 <= rainfall <= 100):
            recommendations.append(('cotton', 0.75))
        
        # Apple conditions
        if (15 <= temperature <= 25 and 60 <= humidity <= 70 and
            6.0 <= ph <= 7.0 and 100 <= rainfall <= 125):
            recommendations.append(('apple', 0.7))
        
        # Default recommendation if no specific match
        if not recommendations:
            recommendations = [('rice', 0.5), ('maize', 0.4), ('wheat', 0.3)]
        
        # Sort by confidence
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        # Format response
        best_crop = recommendations[0][0]
        top_recommendations = [
            {'crop': crop, 'confidence': confidence}
            for crop, confidence in recommendations[:3]
        ]
        
        crop_details = CROP_DATA.get(best_crop, {})
        
        response = {
            'success': True,
            'input_conditions': {
                'N': data['N'],
                'P': data['P'], 
                'K': data['K'],
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            },
            'recommended_crop': best_crop,
            'top_recommendations': top_recommendations,
            'crop_details': crop_details,
            'note': 'This is a simplified recommendation system'
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    """Simple chat responses"""
    try:
        data = request.get_json()
        
        if 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        user_message = data['message'].lower()
        
        # Simple keyword-based responses
        if any(word in user_message for word in ['rice', 'paddy']):
            response = "Rice is a water-intensive crop that grows best in warm, humid conditions with abundant rainfall. It requires flooded fields and temperatures between 20-35°C."
        elif any(word in user_message for word in ['maize', 'corn']):
            response = "Maize is a versatile crop that can adapt to various climatic conditions. It prefers well-drained soil and moderate rainfall of 50-75cm annually."
        elif any(word in user_message for word in ['pest', 'insect']):
            response = "For pest control, use integrated pest management (IPM). Encourage beneficial insects, rotate crops, and use organic pesticides when necessary."
        elif any(word in user_message for word in ['fertilizer', 'nutrient']):
            response = "Always test your soil before applying fertilizers. Use organic compost when possible. Nitrogen promotes leaf growth, phosphorus helps roots, and potassium improves disease resistance."
        elif any(word in user_message for word in ['water', 'irrigation']):
            response = "Water your crops early morning or late evening. Use drip irrigation for efficiency and monitor soil moisture. Avoid overwatering to prevent root rot."
        elif any(word in user_message for word in ['soil', 'ph']):
            response = "Soil pH is crucial for nutrient availability. Most crops prefer slightly acidic to neutral soil (pH 6.0-7.0). Test your soil regularly and amend as needed."
        else:
            response = "I'm here to help with agricultural questions! Ask me about crops, pest control, fertilizers, irrigation, or soil management."
        
        return jsonify({
            'success': True,
            'user_message': data['message'],
            'bot_response': response,
            'note': 'This is a simplified chat system'
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_bp.route('/crop/<crop_name>', methods=['GET'])
@cross_origin()
def get_crop_info(crop_name):
    """Get information about a specific crop"""
    crop_name_lower = crop_name.lower()
    
    if crop_name_lower not in CROP_DATA:
        return jsonify({'error': f'Crop "{crop_name}" not found'}), 404
    
    crop_info = CROP_DATA[crop_name_lower]
    
    return jsonify({
        'success': True,
        'crop_name': crop_name_lower,
        'crop_details': crop_info
    })

@crop_bp.route('/advice/<topic>', methods=['GET'])
@cross_origin()
def get_agricultural_advice(topic):
    """Get agricultural advice on specific topics"""
    topic_lower = topic.lower()
    
    if topic_lower not in AGRICULTURAL_ADVICE:
        return jsonify({
            'success': True,
            'topic': topic,
            'advice': "General agricultural advice: Focus on soil health, proper irrigation, integrated pest management, and sustainable farming practices."
        })
    
    advice_data = AGRICULTURAL_ADVICE[topic_lower]
    
    return jsonify({
        'success': True,
        'topic': topic,
        'advice': advice_data
    })

