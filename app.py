# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Plant data
plants = {
    'aloe_vera': {
        'name': 'Aloe Vera',
        'description': 'A succulent plant species with healing properties.',
        'image': 'aloe_vera.jpg',
        'difficulty': 'Easy to grow',
        'care_instructions': {
            'light': 'Bright indirect light',
            'water': 'Water every 2-3 weeks',
            'placement': 'Indoor'
        }
    },
    'snake_plant': {
        'name': 'Snake Plant',
        'description': 'An air-purifying plant that is very easy to maintain.',
        'image': 'snake_plant.jpg',
        'difficulty': 'Easy to grow',
        'care_instructions': {
            'light': 'Low to bright indirect light',
            'water': 'Water every 2-4 weeks',
            'placement': 'Indoor'
        }
    },
    'mint': {
        'name': 'Mint',
        'description': 'A fragrant herb that grows quickly and spreads easily.',
        'image': 'mint.jpg',
        'difficulty': 'Easy to grow',
        'care_instructions': {
            'light': 'Full sun to partial shade',
            'water': 'Keep soil moist',
            'placement': 'Outdoor'
        }
    },
    'tomatoes': {
        'name': 'Tomatoes',
        'description': 'A popular vegetable plant that needs regular care.',
        'image': 'tomatoes.jpg',
        'difficulty': 'Moderately easy to grow',
        'care_instructions': {
            'light': 'Full sun',
            'water': 'Regular watering',
            'placement': 'Outdoor'
        }
    },
    'peppers': {
        'name': 'Peppers',
        'description': 'Colorful vegetable plants that thrive in warm weather.',
        'image': 'peppers.jpg',
        'difficulty': 'Moderately easy to grow',
        'care_instructions': {
            'light': 'Full sun',
            'water': 'Moderate watering',
            'placement': 'Outdoor'
        }
    },
    'lavender': {
        'name': 'Lavender',
        'description': 'A fragrant herb known for its purple flowers.',
        'image': 'lavender.jpg',
        'difficulty': 'Moderately easy to grow',
        'care_instructions': {
            'light': 'Full sun',
            'water': 'Low water needs',
            'placement': 'Outdoor'
        }
    }
}

@app.route('/')
def home():
    search_query = request.args.get('search', '').lower()
    filter_type = request.args.get('filter', 'all').lower()
    
    filtered_plants = {}
    
    for plant_id, plant in plants.items():
        # Apply search filter
        if search_query and search_query not in plant['name'].lower() and search_query not in plant['description'].lower():
            continue
            
        # Apply category filter
        if filter_type == 'easy to grow' and 'Easy' not in plant['difficulty']:
            continue
        elif filter_type == 'indoor' and 'indoor' not in plant['care_instructions']['placement'].lower():
            continue
        elif filter_type == 'outdoor' and 'outdoor' not in plant['care_instructions']['placement'].lower():
            continue
            
        filtered_plants[plant_id] = plant
    
    return render_template('home.html', plants=filtered_plants)

@app.route('/plant_care/<plant_id>')
def plant_care(plant_id):
    plant = plants.get(plant_id)
    if plant:
        return render_template('plant_care/plant_care.html', plant=plant)
    return "Plant not found", 404

@app.route('/api/search')
def search_plants():
    query = request.args.get('query', '').lower()
    results = {
        id: plant for id, plant in plants.items()
        if query in plant['name'].lower() or query in plant['description'].lower()
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)