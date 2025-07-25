from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys
import os
import json
import joblib
import numpy as np

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from crop_chatbot import CropChatbot

crop_bp = Blueprint('crop', __name__)

# Initialize the chatbot
chatbot = None

def init_chatbot():
    global chatbot
    try:
        chatbot = CropChatbot()
        return True
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        return False

@crop_bp.route('/recommend', methods=['POST'])
@cross_origin()
def recommend_crop():
    """Endpoint for crop recommendation based on soil and climate data"""
    global chatbot
    
    if chatbot is None:
        if not init_chatbot():
            return jsonify({'error': 'Chatbot initialization failed'}), 500
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract values
        N = float(data['N'])
        P = float(data['P'])
        K = float(data['K'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])
        
        # Validate ranges
        if not (0 <= N <= 200):
            return jsonify({'error': 'Nitrogen (N) should be between 0-200'}), 400
        if not (0 <= P <= 200):
            return jsonify({'error': 'Phosphorus (P) should be between 0-200'}), 400
        if not (0 <= K <= 200):
            return jsonify({'error': 'Potassium (K) should be between 0-200'}), 400
        if not (0 <= temperature <= 50):
            return jsonify({'error': 'Temperature should be between 0-50°C'}), 400
        if not (0 <= humidity <= 100):
            return jsonify({'error': 'Humidity should be between 0-100%'}), 400
        if not (0 <= ph <= 14):
            return jsonify({'error': 'pH should be between 0-14'}), 400
        if not (0 <= rainfall <= 500):
            return jsonify({'error': 'Rainfall should be between 0-500mm'}), 400
        
        # Get recommendation
        best_crop, top_crops = chatbot.predict_crop(N, P, K, temperature, humidity, ph, rainfall)
        crop_details = chatbot.get_crop_details(best_crop)
        
        response = {
            'success': True,
            'input_conditions': {
                'N': N,
                'P': P,
                'K': K,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            },
            'recommended_crop': best_crop,
            'top_recommendations': [
                {'crop': crop, 'confidence': float(confidence)}
                for crop, confidence in top_crops
            ],
            'crop_details': crop_details,
            'formatted_recommendation': chatbot.format_crop_recommendation(
                N, P, K, temperature, humidity, ph, rainfall
            )
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    """Endpoint for general agricultural chat"""
    global chatbot
    
    if chatbot is None:
        if not init_chatbot():
            return jsonify({'error': 'Chatbot initialization failed'}), 500
    
    try:
        data = request.get_json()
        
        if 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        user_message = data['message']
        conversation_history = data.get('conversation_history', [])
        
        # Process the message
        response_text = chatbot.process_user_input(user_message)
        
        response = {
            'success': True,
            'user_message': user_message,
            'bot_response': response_text,
            'timestamp': str(np.datetime64('now'))
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_bp.route('/crops', methods=['GET'])
@cross_origin()
def get_crops():
    """Endpoint to get list of available crops"""
    global chatbot
    
    if chatbot is None:
        if not init_chatbot():
            return jsonify({'error': 'Chatbot initialization failed'}), 500
    
    try:
        crops = list(chatbot.label_encoder.classes_)
        crop_categories = chatbot.agricultural_knowledge['crop_categories']
        
        response = {
            'success': True,
            'crops': crops,
            'categories': crop_categories,
            'total_crops': len(crops)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_bp.route('/crop/<crop_name>', methods=['GET'])
@cross_origin()
def get_crop_info(crop_name):
    """Endpoint to get detailed information about a specific crop"""
    global chatbot
    
    if chatbot is None:
        if not init_chatbot():
            return jsonify({'error': 'Chatbot initialization failed'}), 500
    
    try:
        crop_name_lower = crop_name.lower()
        
        # Check if crop exists
        if crop_name_lower not in [crop.lower() for crop in chatbot.label_encoder.classes_]:
            return jsonify({'error': f'Crop "{crop_name}" not found'}), 404
        
        # Find the exact crop name
        exact_crop_name = None
        for crop in chatbot.label_encoder.classes_:
            if crop.lower() == crop_name_lower:
                exact_crop_name = crop
                break
        
        crop_details = chatbot.get_crop_details(exact_crop_name)
        
        # Get additional information from knowledge base
        soil_req = chatbot.agricultural_knowledge.get('soil_requirements', {}).get(exact_crop_name, {})
        climate_req = chatbot.agricultural_knowledge.get('climate_requirements', {}).get(exact_crop_name, {})
        
        response = {
            'success': True,
            'crop_name': exact_crop_name,
            'crop_details': crop_details,
            'soil_requirements': soil_req,
            'climate_requirements': climate_req
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_bp.route('/advice/<topic>', methods=['GET'])
@cross_origin()
def get_agricultural_advice(topic):
    """Endpoint to get agricultural advice on specific topics"""
    global chatbot
    
    if chatbot is None:
        if not init_chatbot():
            return jsonify({'error': 'Chatbot initialization failed'}), 500
    
    try:
        advice = chatbot.get_agricultural_advice(topic)
        
        response = {
            'success': True,
            'topic': topic,
            'advice': advice
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint"""
    global chatbot
    
    chatbot_status = 'initialized' if chatbot is not None else 'not_initialized'
    
    return jsonify({
        'success': True,
        'status': 'healthy',
        'chatbot_status': chatbot_status,
        'message': 'Crop recommendation API is running'
    })

# Initialize chatbot when module is imported
init_chatbot()

