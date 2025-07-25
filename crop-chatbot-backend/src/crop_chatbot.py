import openai
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any

class CropChatbot:
    def __init__(self):
        # Load the trained model and label encoder
        self.model = joblib.load('/home/ubuntu/crop_recommendation_model.pkl')
        self.label_encoder = joblib.load('/home/ubuntu/label_encoder.pkl')
        
        # Load knowledge bases
        with open('/home/ubuntu/crop_info.json', 'r') as f:
            self.crop_info = json.load(f)
        
        with open('/home/ubuntu/agricultural_knowledge.json', 'r') as f:
            self.agricultural_knowledge = json.load(f)
        
        with open('/home/ubuntu/quick_agricultural_facts.json', 'r') as f:
            self.quick_facts = json.load(f)
        
        # System prompt for the chatbot
        self.system_prompt = """You are an expert agricultural advisor and crop recommendation specialist. You have access to:

1. A machine learning model that can predict the best crops based on soil and climate conditions
2. Comprehensive agricultural knowledge including soil requirements, climate needs, pest management, and sustainable practices
3. Detailed information about 22 different crops including cereals, legumes, fruits, and cash crops

Your role is to:
- Provide accurate crop recommendations based on soil and climate data
- Offer practical farming advice and best practices
- Help with pest management, fertilizer recommendations, and irrigation guidance
- Suggest sustainable farming practices
- Answer questions about crop diseases, harvesting, and post-harvest handling

Always provide helpful, accurate, and practical advice. When making crop recommendations, explain the reasoning behind your suggestions. Be conversational but professional, and ask clarifying questions when needed."""

    def predict_crop(self, N: float, P: float, K: float, temperature: float, 
                    humidity: float, ph: float, rainfall: float) -> Tuple[str, List[Tuple[str, float]]]:
        """Predict the best crop for given conditions"""
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = self.model.predict(features)[0]
        crop_name = self.label_encoder.inverse_transform([prediction])[0]
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(features)[0]
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_crops = [(self.label_encoder.inverse_transform([idx])[0], probabilities[idx]) 
                      for idx in top_3_indices]
        
        return crop_name, top_3_crops

    def get_crop_details(self, crop_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific crop"""
        if crop_name in self.crop_info:
            return self.crop_info[crop_name]
        return {}

    def format_crop_recommendation(self, N: float, P: float, K: float, temperature: float, 
                                 humidity: float, ph: float, rainfall: float) -> str:
        """Format a comprehensive crop recommendation"""
        best_crop, top_crops = self.predict_crop(N, P, K, temperature, humidity, ph, rainfall)
        
        recommendation = f"""Based on your soil and climate conditions:
- Nitrogen (N): {N}
- Phosphorus (P): {P}
- Potassium (K): {K}
- Temperature: {temperature}°C
- Humidity: {humidity}%
- pH: {ph}
- Rainfall: {rainfall}mm

**Recommended Crop: {best_crop.title()}**

**Top 3 Recommendations:**
"""
        for i, (crop, confidence) in enumerate(top_crops, 1):
            recommendation += f"{i}. {crop.title()} (Confidence: {confidence:.1%})\n"
        
        # Add crop-specific details
        crop_details = self.get_crop_details(best_crop)
        if crop_details:
            recommendation += f"\n**Optimal conditions for {best_crop.title()}:**\n"
            recommendation += f"- Average N requirement: {crop_details['avg_N']:.1f}\n"
            recommendation += f"- Average P requirement: {crop_details['avg_P']:.1f}\n"
            recommendation += f"- Average K requirement: {crop_details['avg_K']:.1f}\n"
            recommendation += f"- Temperature range: {crop_details['temperature_range'][0]:.1f}-{crop_details['temperature_range'][1]:.1f}°C\n"
            recommendation += f"- Humidity range: {crop_details['humidity_range'][0]:.1f}-{crop_details['humidity_range'][1]:.1f}%\n"
            recommendation += f"- pH range: {crop_details['ph_range'][0]:.1f}-{crop_details['ph_range'][1]:.1f}\n"
            recommendation += f"- Rainfall range: {crop_details['rainfall_range'][0]:.1f}-{crop_details['rainfall_range'][1]:.1f}mm\n"
        
        return recommendation

    def get_agricultural_advice(self, topic: str) -> str:
        """Get specific agricultural advice on various topics"""
        topic_lower = topic.lower()
        
        if 'pest' in topic_lower:
            return json.dumps(self.agricultural_knowledge['pest_management'], indent=2)
        elif 'fertilizer' in topic_lower or 'nutrient' in topic_lower:
            return json.dumps(self.agricultural_knowledge['fertilizer_recommendations'], indent=2)
        elif 'irrigation' in topic_lower or 'water' in topic_lower:
            return json.dumps(self.agricultural_knowledge['irrigation_practices'], indent=2)
        elif 'disease' in topic_lower:
            return json.dumps(self.agricultural_knowledge['crop_diseases'], indent=2)
        elif 'sustainable' in topic_lower or 'organic' in topic_lower:
            return json.dumps(self.agricultural_knowledge['sustainable_practices'], indent=2)
        elif 'harvest' in topic_lower:
            return json.dumps(self.agricultural_knowledge['harvesting_guidelines'], indent=2)
        else:
            return "I can help with pest management, fertilizers, irrigation, crop diseases, sustainable practices, and harvesting. What specific topic would you like to know about?"

    def chat_with_openai(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using OpenAI API with agricultural context"""
        if conversation_history is None:
            conversation_history = []
        
        # Prepare context with agricultural knowledge
        context = f"""
Agricultural Knowledge Available:
- Crop Categories: {json.dumps(self.agricultural_knowledge['crop_categories'])}
- Quick Facts: {json.dumps(self.quick_facts)}
- Available crops for recommendation: {', '.join(self.label_encoder.classes_)}

User Message: {user_message}
"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": context}
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm having trouble connecting to my AI service. However, I can still help you with crop recommendations and agricultural advice using my built-in knowledge. Error: {str(e)}"

    def process_user_input(self, user_input: str) -> str:
        """Process user input and provide appropriate response"""
        user_input_lower = user_input.lower()
        
        # Check if user is asking for crop recommendation with specific values
        if any(keyword in user_input_lower for keyword in ['recommend', 'suggest', 'predict', 'best crop']):
            # Try to extract numerical values for crop prediction
            try:
                # This is a simplified extraction - in a real app, you'd use more sophisticated NLP
                numbers = [float(s) for s in user_input.split() if s.replace('.', '').isdigit()]
                if len(numbers) >= 7:
                    N, P, K, temp, humidity, ph, rainfall = numbers[:7]
                    return self.format_crop_recommendation(N, P, K, temp, humidity, ph, rainfall)
            except:
                pass
        
        # Check for specific agricultural topics
        if any(keyword in user_input_lower for keyword in ['pest', 'fertilizer', 'irrigation', 'disease', 'sustainable', 'harvest']):
            advice = self.get_agricultural_advice(user_input)
            return f"Here's information about {user_input}:\n\n{advice}"
        
        # Use OpenAI for general conversation
        return self.chat_with_openai(user_input)

# Test the chatbot
if __name__ == "__main__":
    chatbot = CropChatbot()
    
    print("Crop Recommendation Chatbot initialized successfully!")
    print("Testing crop recommendation...")
    
    # Test crop recommendation
    test_recommendation = chatbot.format_crop_recommendation(90, 42, 43, 20.88, 82.00, 6.50, 202.94)
    print("\nTest Recommendation:")
    print(test_recommendation)
    
    print("\nChatbot ready for use!")

