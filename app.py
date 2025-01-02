from flask import Flask, render_template, request, redirect, url_for, flash
from data.plants import plants
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages
reminders = {}  # Dictionary to store reminders

@app.route('/')
def home():
    search_query = request.args.get('search', '').lower()
    filter_type = request.args.get('filter', 'all').lower()
    
    filtered_plants = {}
    
    for plant_id, plant in plants.items():
        matches_search = (not search_query or 
                        search_query in plant['name'].lower() or 
                        search_query in plant['description'].lower())
        
        matches_filter = (
            filter_type == 'all' or
            (filter_type == 'easy to grow' and 'Easy' in plant['difficulty']) or
            (filter_type == 'indoor' and 'Indoor' in plant['care_instructions']['placement']) or
            (filter_type == 'outdoor' and 'Outdoor' in plant['care_instructions']['placement'])
        )
        
        if matches_search and matches_filter:
            filtered_plants[plant_id] = plant
    
    return render_template('home.html', plants=filtered_plants)

@app.route('/plant_care/<plant_id>', methods=['GET', 'POST'])
def plant_care(plant_id):
    plant = plants.get(plant_id)
    if not plant:
        return "Plant not found", 404

    plant_reminders = reminders.get(plant_id, [])
    return render_template('plant_care.html', plant=plant, reminders=plant_reminders)

@app.route('/set_reminder/<plant_id>', methods=['POST'])
def set_reminder(plant_id):
    plant = plants.get(plant_id)
    if not plant:
        return "Plant not found", 404
    
    # Determine the watering frequency in days
    watering_frequency = plant['care_instructions']['water'].lower()
    if 'every day' in watering_frequency:
        days = 1
    elif 'every week' in watering_frequency:
        days = 7
    elif 'every 2 weeks' in watering_frequency:
        days = 14
    elif 'every 3 weeks' in watering_frequency:
        days = 21
    elif 'every month' in watering_frequency:
        days = 30
    else:
        # Default to 7 days if frequency is not clearly specified
        days = 7

    # Set the reminder date based on the current date and watering frequency
    reminder_date = datetime.now() + timedelta(days=days)
    reminder_date_str = reminder_date.strftime('%Y-%m-%d')

    if plant_id not in reminders:
        reminders[plant_id] = []
    reminders[plant_id].append(reminder_date_str)
    
    flash('Reminder set for {}'.format(reminder_date_str), 'success')
    return redirect(url_for('plant_care', plant_id=plant_id))

if __name__ == '__main__':
    app.run(debug=True)