// Offline Crop Recommendation Model
// This provides crop recommendations without requiring server connectivity

class OfflineCropModel {
    constructor() {
        // Crop data with optimal conditions
        this.cropData = {
            "rice": {
                "name": "Rice",
                "category": "cereal",
                "optimal_conditions": {
                    "temperature": [20, 35],
                    "humidity": [80, 90],
                    "rainfall": [150, 300],
                    "ph": [5.5, 7.0],
                    "nitrogen": [80, 120],
                    "phosphorus": [40, 80],
                    "potassium": [40, 80]
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
                    "temperature": [21, 27],
                    "humidity": [60, 70],
                    "rainfall": [50, 75],
                    "ph": [6.0, 7.5],
                    "nitrogen": [100, 150],
                    "phosphorus": [60, 100],
                    "potassium": [40, 80]
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
                    "temperature": [15, 25],
                    "humidity": [50, 60],
                    "rainfall": [30, 100],
                    "ph": [6.0, 7.5],
                    "nitrogen": [80, 120],
                    "phosphorus": [40, 80],
                    "potassium": [30, 60]
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
                    "temperature": [21, 30],
                    "humidity": [50, 80],
                    "rainfall": [50, 100],
                    "ph": [5.8, 8.0],
                    "nitrogen": [120, 180],
                    "phosphorus": [60, 100],
                    "potassium": [60, 120]
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
                    "temperature": [15, 25],
                    "humidity": [60, 70],
                    "rainfall": [100, 125],
                    "ph": [6.0, 7.0],
                    "nitrogen": [60, 100],
                    "phosphorus": [40, 80],
                    "potassium": [80, 120]
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
        };
    }

    // Calculate suitability score for a crop based on input conditions
    calculateSuitability(cropName, conditions) {
        const crop = this.cropData[cropName];
        if (!crop) return 0;

        const optimal = crop.optimal_conditions;
        let score = 0;
        let factors = 0;

        // Temperature score
        if (this.isInRange(conditions.temperature, optimal.temperature)) {
            score += 1;
        } else {
            score += Math.max(0, 1 - Math.abs(conditions.temperature - this.getMidpoint(optimal.temperature)) / 10);
        }
        factors++;

        // Humidity score
        if (this.isInRange(conditions.humidity, optimal.humidity)) {
            score += 1;
        } else {
            score += Math.max(0, 1 - Math.abs(conditions.humidity - this.getMidpoint(optimal.humidity)) / 20);
        }
        factors++;

        // Rainfall score
        if (this.isInRange(conditions.rainfall, optimal.rainfall)) {
            score += 1;
        } else {
            score += Math.max(0, 1 - Math.abs(conditions.rainfall - this.getMidpoint(optimal.rainfall)) / 50);
        }
        factors++;

        // pH score
        if (this.isInRange(conditions.ph, optimal.ph)) {
            score += 1;
        } else {
            score += Math.max(0, 1 - Math.abs(conditions.ph - this.getMidpoint(optimal.ph)) / 2);
        }
        factors++;

        // Nutrient scores (NPK)
        if (this.isInRange(conditions.N, optimal.nitrogen)) {
            score += 0.5;
        } else {
            score += Math.max(0, 0.5 - Math.abs(conditions.N - this.getMidpoint(optimal.nitrogen)) / 100);
        }
        factors += 0.5;

        if (this.isInRange(conditions.P, optimal.phosphorus)) {
            score += 0.5;
        } else {
            score += Math.max(0, 0.5 - Math.abs(conditions.P - this.getMidpoint(optimal.phosphorus)) / 50);
        }
        factors += 0.5;

        if (this.isInRange(conditions.K, optimal.potassium)) {
            score += 0.5;
        } else {
            score += Math.max(0, 0.5 - Math.abs(conditions.K - this.getMidpoint(optimal.potassium)) / 50);
        }
        factors += 0.5;

        return score / factors;
    }

    // Check if value is within range
    isInRange(value, range) {
        return value >= range[0] && value <= range[1];
    }

    // Get midpoint of range
    getMidpoint(range) {
        return (range[0] + range[1]) / 2;
    }

    // Get crop recommendation based on input conditions
    recommend(conditions) {
        const recommendations = [];

        for (const cropName in this.cropData) {
            const suitability = this.calculateSuitability(cropName, conditions);
            recommendations.push({
                crop: cropName,
                confidence: suitability
            });
        }

        // Sort by confidence (highest first)
        recommendations.sort((a, b) => b.confidence - a.confidence);

        const bestCrop = recommendations[0].crop;
        const cropDetails = this.cropData[bestCrop];

        return {
            success: true,
            input_conditions: conditions,
            recommended_crop: bestCrop,
            top_recommendations: recommendations.slice(0, 3),
            crop_details: {
                ...cropDetails,
                temperature_range: cropDetails.optimal_conditions.temperature,
                humidity_range: cropDetails.optimal_conditions.humidity,
                rainfall_range: cropDetails.optimal_conditions.rainfall,
                ph_range: cropDetails.optimal_conditions.ph
            },
            detailed_guidance: {
                fielding: cropDetails.fielding,
                management: cropDetails.management,
                maintenance: cropDetails.maintenance
            },
            note: 'Offline recommendation system with detailed guidance',
            offline_mode: true
        };
    }

    // Get information about a specific crop
    getCropInfo(cropName) {
        return this.cropData[cropName.toLowerCase()] || null;
    }

    // Get list of all available crops
    getAllCrops() {
        return Object.keys(this.cropData);
    }
}

// Create global instance
window.offlineCropModel = new OfflineCropModel();

