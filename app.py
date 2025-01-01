from flask import Flask, render_template
from data.plants import plants

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', plants=plants)

@app.route('/plant/<plant_id>')
def plant_care(plant_id):
    plant = plants.get(plant_id)
    if plant:
        return render_template('plant_care/plant_care.html', plant=plant)
    return 'Plant not found', 404

if __name__ == '__main__':
    app.run(debug=True)