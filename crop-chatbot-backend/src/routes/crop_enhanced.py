from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import os

crop_enhanced_bp = Blueprint('crop_enhanced', __name__)

# Load the enhanced agricultural knowledge base
def load_agricultural_knowledge():
    try:
        with open('/home/ubuntu/agricultural_knowledge.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

AGRICULTURAL_KNOWLEDGE = load_agricultural_knowledge()

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
        "description": "Rice is a staple food crop that requires high humidity and abundant water.",
        "fielding": {
            "land_preparation": "Prepare flooded fields with proper leveling. Use puddling to create a water-tight layer.",
            "planting": "Transplant 20-25 day old seedlings with 20x15 cm spacing. Plant 2-3 seedlings per hill.",
            "spacing": "20 cm between rows, 15 cm between plants"
        },
        "management": {
            "water": "Maintain 2-5 cm water depth throughout growing season. Drain before harvest.",
            "nutrients": "Apply 120 kg N, 60 kg P2O5, 40 kg K2O per hectare in split doses.",
            "weeds": "Use pre-emergence herbicides and manual weeding at 20-25 days after transplanting."
        },
        "maintenance": {
            "disease_prevention": "Use resistant varieties, proper spacing, and avoid excessive nitrogen.",
            "pest_control": "Monitor for stem borer, brown planthopper. Use IPM strategies.",
            "harvesting": "Harvest when 80% of grains are golden yellow. Moisture content should be 20-25%."
        }
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
        "description": "Maize is a versatile crop that can grow in various climatic conditions.",
        "fielding": {
            "land_preparation": "Deep plowing followed by 2-3 harrowings. Create ridges and furrows for drainage.",
            "planting": "Plant seeds 2-3 cm deep with 60-75 cm row spacing and 20-25 cm plant spacing.",
            "spacing": "60-75 cm between rows, 20-25 cm between plants"
        },
        "management": {
            "water": "Requires 500-800 mm water. Critical stages: tasseling and grain filling.",
            "nutrients": "Apply 150 kg N, 75 kg P2O5, 50 kg K2O per hectare. Side-dress nitrogen at knee-high stage.",
            "weeds": "Pre-emergence herbicides followed by inter-cultivation at 25-30 days."
        },
        "maintenance": {
            "disease_prevention": "Use certified seeds, crop rotation, and balanced nutrition.",
            "pest_control": "Monitor for fall armyworm, corn borer. Use pheromone traps and biological control.",
            "harvesting": "Harvest when husks are dry and kernels have black layer formation. Moisture 15-20%."
        }
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
        "description": "Wheat is a major cereal grain and staple food worldwide.",
        "fielding": {
            "land_preparation": "Deep plowing in summer, followed by 2-3 cultivations. Level the field properly.",
            "planting": "Sow seeds 2-3 cm deep with 20-23 cm row spacing. Seed rate: 100-125 kg/ha.",
            "spacing": "20-23 cm between rows, continuous seeding within rows"
        },
        "management": {
            "water": "Requires 450-650 mm water. Critical stages: crown root initiation, tillering, flowering.",
            "nutrients": "Apply 120 kg N, 60 kg P2O5, 40 kg K2O per hectare in split applications.",
            "weeds": "Use pre-emergence herbicides and one hand weeding at 30-35 days."
        },
        "maintenance": {
            "disease_prevention": "Use resistant varieties, seed treatment, and proper crop rotation.",
            "pest_control": "Monitor for aphids, termites. Use integrated pest management.",
            "harvesting": "Harvest when grains are hard and moisture content is 12-14%."
        }
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
        "description": "Cotton is an important cash crop used in textile production.",
        "fielding": {
            "land_preparation": "Deep plowing followed by harrowing. Create ridges and furrows for proper drainage.",
            "planting": "Plant seeds 2-3 cm deep with 60-90 cm row spacing and 10-15 cm plant spacing.",
            "spacing": "60-90 cm between rows, 10-15 cm between plants"
        },
        "management": {
            "water": "Requires 700-1300 mm water. Critical stages: flowering and boll development.",
            "nutrients": "Apply 150 kg N, 75 kg P2O5, 75 kg K2O per hectare in split doses.",
            "weeds": "Use pre-emergence herbicides and 2-3 inter-cultivations."
        },
        "maintenance": {
            "disease_prevention": "Use resistant varieties, seed treatment, and crop rotation.",
            "pest_control": "Monitor for bollworm, whitefly. Use IPM with pheromone traps and beneficial insects.",
            "harvesting": "Hand-pick when bolls are fully opened and fibers are dry. Multiple pickings required."
        }
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
        "description": "Apples are popular fruits that require temperate climate conditions.",
        "fielding": {
            "land_preparation": "Prepare pits 1m x 1m x 1m size. Fill with organic matter and topsoil.",
            "planting": "Plant grafted saplings during dormant season. Space 4-6 meters apart.",
            "spacing": "4-6 meters between trees in all directions"
        },
        "management": {
            "water": "Deep watering weekly. Drip irrigation preferred. Mulch around trees.",
            "nutrients": "Apply balanced NPK fertilizer. Organic compost annually in spring.",
            "weeds": "Maintain weed-free circle around trees. Use mulching and manual weeding."
        },
        "maintenance": {
            "disease_prevention": "Prune for air circulation. Use copper sprays during dormancy.",
            "pest_control": "Monitor for codling moth, aphids. Use pheromone traps and beneficial insects.",
            "harvesting": "Harvest when fruits are fully colored and easily separate from branch. Handle gently.",
            "pruning": "Annual pruning during dormancy. Remove dead, diseased, and crossing branches."
        }
    }
}

ENHANCED_AGRICULTURAL_ADVICE = {
    "land_preparation": {
        "title": "Land Preparation Techniques",
        "advice": [
            "Primary tillage: Deep plowing to break hardpan and improve soil structure",
            "Secondary tillage: Disking and harrowing to create fine seedbed",
            "Clearing: Remove weeds, crop residues, and debris from previous season",
            "Leveling: Ensure uniform water distribution and prevent waterlogging",
            "Pre-irrigation: Moisten soil for easier cultivation and weed germination"
        ]
    },
    "planting": {
        "title": "Planting Methods and Best Practices",
        "advice": [
            "Direct seeding: Broadcasting, drilling, or precision planting based on crop type",
            "Transplanting: Start seedlings in nursery and transplant at appropriate stage",
            "Proper spacing: Ensure adequate space for growth, air circulation, and light penetration",
            "Seed depth: Plant at 2-3 times the seed diameter for optimal germination",
            "Timing: Plant according to local climate and crop requirements"
        ]
    },
    "nutrient_management": {
        "title": "Comprehensive Nutrient Management",
        "advice": [
            "Soil testing: Conduct regular tests to determine nutrient status",
            "Balanced fertilization: Apply N, P, K, and micronutrients as per crop needs",
            "Organic amendments: Use compost, farmyard manure, and green manure",
            "Split application: Apply nutrients in multiple doses for better efficiency",
            "Timing: Apply nutrients when crops can best utilize them"
        ]
    },
    "water_management": {
        "title": "Efficient Water Management",
        "advice": [
            "Irrigation scheduling: Water based on crop growth stage and soil moisture",
            "Drip irrigation: Use for water-efficient and precise application",
            "Mulching: Reduce evaporation and maintain soil moisture",
            "Rainwater harvesting: Collect and store rainwater for dry periods",
            "Drainage: Ensure proper drainage to prevent waterlogging"
        ]
    },
    "weed_control": {
        "title": "Integrated Weed Management",
        "advice": [
            "Prevention: Use clean seeds, equipment, and avoid weed seed spread",
            "Cultural control: Crop rotation, proper spacing, and cover cropping",
            "Mechanical control: Tillage, hand weeding, and inter-cultivation",
            "Biological control: Use natural enemies and allelopathic crops",
            "Chemical control: Herbicides as last resort with proper safety measures"
        ]
    },
    "disease_prevention": {
        "title": "Disease Prevention Strategies",
        "advice": [
            "Resistant varieties: Choose disease-resistant cultivars when available",
            "Crop rotation: Break disease cycles by rotating with non-host crops",
            "Sanitation: Remove infected plant material and clean tools",
            "Proper spacing: Ensure good air circulation to reduce humidity",
            "Balanced nutrition: Maintain plant health through proper fertilization",
            "Seed treatment: Use fungicide-treated seeds to prevent soil-borne diseases"
        ]
    },
    "pruning": {
        "title": "Pruning Techniques for Better Growth",
        "advice": [
            "Timing: Prune during dormant season for most fruit trees",
            "Thinning cuts: Remove entire branches to improve light penetration",
            "Heading cuts: Cut back to lateral buds to encourage branching",
            "Deadheading: Remove spent flowers to promote continued blooming",
            "Tool maintenance: Use clean, sharp tools to prevent disease spread"
        ]
    },
    "harvesting": {
        "title": "Optimal Harvesting Practices",
        "advice": [
            "Timing: Harvest at proper maturity for best quality and storage life",
            "Early morning: Best time for harvesting most crops when cool and hydrated",
            "Gentle handling: Avoid bruising and damage during harvest",
            "Proper tools: Use appropriate harvesting tools for each crop type",
            "Post-harvest care: Clean, sort, and store under optimal conditions"
        ]
    }
}

@crop_enhanced_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Enhanced Crop recommendation API is running',
        'version': '2.0.0-enhanced',
        'features': ['crop_recommendation', 'detailed_chat', 'fielding_guidance', 'management_advice', 'maintenance_tips']
    })

@crop_enhanced_bp.route('/crops', methods=['GET'])
@cross_origin()
def get_crops():
    """Get list of available crops with enhanced information"""
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
        'total_crops': len(crops),
        'enhanced_features': ['fielding', 'management', 'maintenance']
    })

@crop_enhanced_bp.route('/recommend', methods=['POST'])
@cross_origin()
def recommend_crop():
    """Enhanced crop recommendation with detailed guidance"""
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
        
        # Format response with enhanced details
        best_crop = recommendations[0][0]
        top_recommendations = [
            {'crop': crop, 'confidence': confidence}
            for crop, confidence in recommendations[:3]
        ]
        
        crop_details = CROP_DATA.get(best_crop, {})
        
        # Extract ranges from optimal conditions for frontend compatibility
        optimal_conditions = crop_details.get('optimal_conditions', {})
        
        # Parse temperature range
        temp_str = optimal_conditions.get('temperature', '20-30°C')
        temp_range = [20, 30]  # default
        try:
            temp_parts = temp_str.replace('°C', '').split('-')
            if len(temp_parts) == 2:
                temp_range = [float(temp_parts[0]), float(temp_parts[1])]
        except:
            pass
            
        # Parse humidity range
        humidity_str = optimal_conditions.get('humidity', '60-80%')
        humidity_range = [60, 80]  # default
        try:
            humidity_parts = humidity_str.replace('%', '').split('-')
            if len(humidity_parts) == 2:
                humidity_range = [float(humidity_parts[0]), float(humidity_parts[1])]
        except:
            pass
            
        # Parse rainfall range
        rainfall_str = optimal_conditions.get('rainfall', '100-200cm')
        rainfall_range = [100, 200]  # default
        try:
            rainfall_parts = rainfall_str.replace('cm', '').replace('mm', '').split('-')
            if len(rainfall_parts) == 2:
                rainfall_range = [float(rainfall_parts[0]), float(rainfall_parts[1])]
        except:
            pass
            
        # Parse pH range
        ph_str = optimal_conditions.get('ph', '6.0-7.0')
        ph_range = [6.0, 7.0]  # default
        try:
            ph_parts = ph_str.split('-')
            if len(ph_parts) == 2:
                ph_range = [float(ph_parts[0]), float(ph_parts[1])]
        except:
            pass
        
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
            'crop_details': {
                **crop_details,
                'temperature_range': temp_range,
                'humidity_range': humidity_range,
                'rainfall_range': rainfall_range,
                'ph_range': ph_range
            },
            'detailed_guidance': {
                'fielding': crop_details.get('fielding', {}),
                'management': crop_details.get('management', {}),
                'maintenance': crop_details.get('maintenance', {})
            },
            'note': 'Enhanced recommendation system with detailed guidance'
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_enhanced_bp.route('/chat', methods=['POST'])
@cross_origin()
def enhanced_chat():
    """Enhanced chat responses with detailed agricultural guidance"""
    try:
        data = request.get_json()
        
        if 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        user_message = data['message'].lower()
        
        # Enhanced keyword-based responses
        response = ""
        
        # Land preparation queries
        if any(word in user_message for word in ['land preparation', 'prepare land', 'soil preparation', 'tillage', 'plowing']):
            response = """Land preparation is crucial for successful crop establishment. Here's a step-by-step guide:

1. **Primary Tillage**: Deep plowing (20-25 cm) to break hardpan and improve soil structure
2. **Secondary Tillage**: Disking and harrowing to create a fine, level seedbed
3. **Clearing**: Remove weeds, crop residues, and debris from the previous season
4. **Leveling**: Ensure uniform surface for proper water distribution
5. **Pre-irrigation**: Light watering to settle soil and promote weed germination for control

Benefits: Improves soil aeration, water infiltration, nutrient availability, and weed control."""

        # Planting queries
        elif any(word in user_message for word in ['planting', 'sowing', 'seeding', 'transplanting', 'spacing']):
            response = """Proper planting techniques ensure optimal crop establishment:

**Planting Methods**:
- **Direct seeding**: Broadcasting, drilling, or precision planting
- **Transplanting**: Starting seedlings in nursery and moving to field

**Key Principles**:
- **Seed depth**: 2-3 times the seed diameter
- **Spacing**: Adequate space for growth and air circulation
- **Timing**: Plant according to local climate and crop requirements
- **Seed quality**: Use certified, disease-free seeds

**Spacing Examples**:
- Rice: 20x15 cm (transplanting)
- Maize: 60-75 cm rows, 20-25 cm plants
- Wheat: 20-23 cm row spacing"""

        # Nutrient management queries
        elif any(word in user_message for word in ['nutrient', 'fertilizer', 'nitrogen', 'phosphorus', 'potassium', 'npk']):
            response = """Comprehensive nutrient management follows the 4R principles:

**The 4Rs**:
1. **Right Source**: Choose appropriate fertilizer type
2. **Right Rate**: Apply correct amount based on soil test
3. **Right Time**: Apply when crops need nutrients most
4. **Right Place**: Apply where roots can access nutrients

**Best Practices**:
- Conduct regular soil testing
- Use balanced NPK fertilization
- Apply organic amendments (compost, manure)
- Split applications for better efficiency
- Consider micronutrients (Zn, B, Fe, Mn)

**Deficiency Signs**:
- Nitrogen: Yellowing of older leaves
- Phosphorus: Purple/reddish leaves, poor roots
- Potassium: Brown leaf edges, weak stems"""

        # Water management queries
        elif any(word in user_message for word in ['water', 'irrigation', 'watering', 'drought', 'moisture']):
            response = """Efficient water management is essential for crop productivity:

**Irrigation Methods**:
- **Drip irrigation**: Most efficient, 90-95% efficiency
- **Sprinkler**: Good for field crops, 75-85% efficiency
- **Furrow**: Traditional for row crops, 60-70% efficiency
- **Flood**: Used for rice, 40-60% efficiency

**Best Practices**:
- Monitor soil moisture regularly
- Water during early morning or evening
- Use mulching to reduce evaporation
- Implement rainwater harvesting
- Choose drought-resistant varieties

**Critical Growth Stages** (when water is most important):
- Germination and establishment
- Flowering and fruit/grain development"""

        # Weed control queries
        elif any(word in user_message for word in ['weed', 'weeding', 'herbicide', 'weed control']):
            response = """Integrated Weed Management (IWM) combines multiple strategies:

**Prevention**:
- Use clean, certified seeds
- Clean equipment between fields
- Prevent weed seed spread

**Cultural Control**:
- Crop rotation to break weed cycles
- Proper plant spacing and density
- Cover cropping and mulching

**Mechanical Control**:
- Timely tillage and cultivation
- Hand weeding when labor is available
- Mowing to prevent seed production

**Biological Control**:
- Encourage beneficial insects
- Use allelopathic crops (suppress weeds naturally)

**Chemical Control** (last resort):
- Pre-emergence herbicides
- Post-emergence selective herbicides
- Always follow label instructions"""

        # Disease prevention queries
        elif any(word in user_message for word in ['disease', 'fungus', 'bacteria', 'virus', 'disease prevention']):
            response = """Disease prevention is more effective than treatment:

**Prevention Strategies**:
1. **Resistant Varieties**: Choose disease-resistant cultivars
2. **Crop Rotation**: Break disease cycles (3-4 year rotation)
3. **Sanitation**: Remove infected plant material, clean tools
4. **Proper Spacing**: Ensure good air circulation
5. **Balanced Nutrition**: Healthy plants resist diseases better
6. **Seed Treatment**: Use fungicide-treated seeds

**Cultural Practices**:
- Avoid overhead watering when possible
- Plant in well-drained soils
- Avoid working in wet conditions
- Remove crop residues that harbor pathogens

**Early Detection**:
- Scout fields regularly
- Learn to identify disease symptoms
- Take action at first signs of disease"""

        # Pruning queries
        elif any(word in user_message for word in ['pruning', 'trimming', 'cutting', 'prune']):
            response = """Proper pruning improves plant health and productivity:

**Pruning Techniques**:
- **Thinning**: Remove entire branches to improve light penetration
- **Heading**: Cut back to lateral buds to encourage branching
- **Pinching**: Remove growing tips to promote bushiness
- **Deadheading**: Remove spent flowers for continued blooming

**Best Practices**:
- Use clean, sharp tools to prevent disease spread
- Make cuts at 45-degree angle above buds
- Prune during dormant season for most fruit trees
- Remove dead, diseased, and crossing branches first

**Benefits**:
- Improved air circulation
- Better light penetration
- Enhanced fruit/flower production
- Disease prevention"""

        # Harvesting queries
        elif any(word in user_message for word in ['harvest', 'harvesting', 'picking', 'when to harvest']):
            response = """Optimal harvesting ensures maximum quality and yield:

**Timing Indicators**:
- **Color**: Fruits/vegetables reach characteristic color
- **Firmness**: Appropriate texture for the crop
- **Size**: Reached expected mature size
- **Moisture content**: Especially important for grains

**Best Practices**:
- Harvest in early morning when cool and hydrated
- Use appropriate tools for each crop
- Handle gently to avoid bruising
- Harvest at proper maturity stage

**Post-Harvest Handling**:
- Clean and sort immediately
- Store under optimal conditions (temperature, humidity)
- Implement pest control in storage
- Process or market quickly for best quality

**Crop-Specific Examples**:
- Rice: 80% grains golden, 20-25% moisture
- Tomatoes: Full color, slight give when pressed
- Apples: Easy separation from branch, full color"""

        # Crop-specific queries
        elif any(word in user_message for word in ['rice', 'paddy']):
            crop_info = CROP_DATA.get('rice', {})
            response = f"""Rice cultivation guide:

**Land Preparation**: {crop_info.get('fielding', {}).get('land_preparation', 'Prepare flooded fields with proper leveling.')}

**Planting**: {crop_info.get('fielding', {}).get('planting', 'Transplant seedlings with proper spacing.')}

**Water Management**: {crop_info.get('management', {}).get('water', 'Maintain proper water depth.')}

**Nutrient Management**: {crop_info.get('management', {}).get('nutrients', 'Apply balanced fertilizers.')}

**Harvesting**: {crop_info.get('maintenance', {}).get('harvesting', 'Harvest at proper maturity.')}

Rice requires flooded conditions and is typically grown in monsoon season."""

        elif any(word in user_message for word in ['maize', 'corn']):
            crop_info = CROP_DATA.get('maize', {})
            response = f"""Maize cultivation guide:

**Land Preparation**: {crop_info.get('fielding', {}).get('land_preparation', 'Deep plowing with proper drainage.')}

**Planting**: {crop_info.get('fielding', {}).get('planting', 'Plant seeds at proper depth and spacing.')}

**Water Management**: {crop_info.get('management', {}).get('water', 'Requires adequate water during critical stages.')}

**Nutrient Management**: {crop_info.get('management', {}).get('nutrients', 'Apply balanced fertilizers with side-dressing.')}

**Harvesting**: {crop_info.get('maintenance', {}).get('harvesting', 'Harvest when kernels are mature.')}

Maize is versatile and can adapt to various climatic conditions."""

        elif any(word in user_message for word in ['wheat']):
            crop_info = CROP_DATA.get('wheat', {})
            response = f"""Wheat cultivation guide:

**Land Preparation**: {crop_info.get('fielding', {}).get('land_preparation', 'Deep plowing and proper field preparation.')}

**Planting**: {crop_info.get('fielding', {}).get('planting', 'Sow seeds at proper depth and spacing.')}

**Water Management**: {crop_info.get('management', {}).get('water', 'Requires water during critical growth stages.')}

**Nutrient Management**: {crop_info.get('management', {}).get('nutrients', 'Apply balanced fertilizers in split doses.')}

**Harvesting**: {crop_info.get('maintenance', {}).get('harvesting', 'Harvest when grains are hard and dry.')}

Wheat is a major cereal crop grown in cooler seasons."""

        elif any(word in user_message for word in ['cotton']):
            crop_info = CROP_DATA.get('cotton', {})
            response = f"""Cotton cultivation guide:

**Land Preparation**: {crop_info.get('fielding', {}).get('land_preparation', 'Prepare ridges and furrows for drainage.')}

**Planting**: {crop_info.get('fielding', {}).get('planting', 'Plant seeds with proper spacing.')}

**Water Management**: {crop_info.get('management', {}).get('water', 'Requires water during flowering and boll development.')}

**Nutrient Management**: {crop_info.get('management', {}).get('nutrients', 'Apply balanced fertilizers in split applications.')}

**Harvesting**: {crop_info.get('maintenance', {}).get('harvesting', 'Hand-pick when bolls are fully opened.')}

Cotton is an important cash crop requiring warm climate."""

        elif any(word in user_message for word in ['apple']):
            crop_info = CROP_DATA.get('apple', {})
            response = f"""Apple cultivation guide:

**Land Preparation**: {crop_info.get('fielding', {}).get('land_preparation', 'Prepare large pits with organic matter.')}

**Planting**: {crop_info.get('fielding', {}).get('planting', 'Plant grafted saplings with adequate spacing.')}

**Water Management**: {crop_info.get('management', {}).get('water', 'Deep watering with drip irrigation preferred.')}

**Nutrient Management**: {crop_info.get('management', {}).get('nutrients', 'Apply balanced fertilizers and organic compost.')}

**Pruning**: {crop_info.get('maintenance', {}).get('pruning', 'Annual pruning during dormancy.')}

**Harvesting**: {crop_info.get('maintenance', {}).get('harvesting', 'Harvest when fruits are fully colored.')}

Apples require temperate climate and careful management."""

        # General agricultural advice
        else:
            response = """I'm your agricultural assistant! I can help you with:

🌱 **Crop Fielding**: Land preparation, planting methods, spacing guidelines
🌾 **Crop Management**: Nutrient management, water management, weed control
🌿 **Crop Maintenance**: Pruning, disease prevention, harvesting

**Ask me about**:
- How to prepare land for planting
- Best planting methods and spacing
- Nutrient and fertilizer management
- Irrigation and water management
- Weed control strategies
- Disease prevention techniques
- Pruning and maintenance
- Harvesting guidelines
- Specific crops: rice, maize, wheat, cotton, apple

**Example questions**:
- "How do I prepare land for rice cultivation?"
- "What's the best spacing for maize planting?"
- "How do I manage nutrients in wheat?"
- "When should I harvest cotton?"

Feel free to ask about any aspect of crop cultivation!"""
        
        return jsonify({
            'success': True,
            'user_message': data['message'],
            'bot_response': response,
            'response_type': 'enhanced_guidance',
            'note': 'Enhanced chat system with detailed agricultural guidance'
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@crop_enhanced_bp.route('/crop/<crop_name>', methods=['GET'])
@cross_origin()
def get_enhanced_crop_info(crop_name):
    """Get enhanced information about a specific crop"""
    crop_name_lower = crop_name.lower()
    
    if crop_name_lower not in CROP_DATA:
        return jsonify({'error': f'Crop "{crop_name}" not found'}), 404
    
    crop_info = CROP_DATA[crop_name_lower]
    
    return jsonify({
        'success': True,
        'crop_name': crop_name_lower,
        'crop_details': crop_info,
        'enhanced_features': ['fielding', 'management', 'maintenance']
    })

@crop_enhanced_bp.route('/advice/<topic>', methods=['GET'])
@cross_origin()
def get_enhanced_agricultural_advice(topic):
    """Get enhanced agricultural advice on specific topics"""
    topic_lower = topic.lower()
    
    if topic_lower not in ENHANCED_AGRICULTURAL_ADVICE:
        return jsonify({
            'success': True,
            'topic': topic,
            'advice': "General agricultural advice: Focus on soil health, proper irrigation, integrated pest management, and sustainable farming practices. For detailed guidance, try topics like: land_preparation, planting, nutrient_management, water_management, weed_control, disease_prevention, pruning, harvesting."
        })
    
    advice_data = ENHANCED_AGRICULTURAL_ADVICE[topic_lower]
    
    return jsonify({
        'success': True,
        'topic': topic,
        'advice': advice_data
    })

@crop_enhanced_bp.route('/guidance/<crop_name>/<guidance_type>', methods=['GET'])
@cross_origin()
def get_crop_guidance(crop_name, guidance_type):
    """Get specific guidance for a crop (fielding, management, or maintenance)"""
    crop_name_lower = crop_name.lower()
    guidance_type_lower = guidance_type.lower()
    
    if crop_name_lower not in CROP_DATA:
        return jsonify({'error': f'Crop "{crop_name}" not found'}), 404
    
    if guidance_type_lower not in ['fielding', 'management', 'maintenance']:
        return jsonify({'error': f'Guidance type "{guidance_type}" not supported. Use: fielding, management, or maintenance'}), 400
    
    crop_info = CROP_DATA[crop_name_lower]
    guidance_data = crop_info.get(guidance_type_lower, {})
    
    return jsonify({
        'success': True,
        'crop_name': crop_name_lower,
        'guidance_type': guidance_type_lower,
        'guidance': guidance_data
    })

