from flask import Flask, render_template, redirect, url_for, session, request
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load scene data from JSON files
def load_scene_data(scene_name):
    with open(f'scenes/{scene_name}.json') as f:
        return json.load(f)

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('show_scene', scene_name='begin'))

@app.route('/scene/<scene_name>', methods=['GET', 'POST'])
def show_scene(scene_name):
    if 'history' not in session:
        session['history'] = []

    try:
        if request.method == 'POST':
            next_scene = request.form['next_scene']
            session['history'].append(next_scene)
            return redirect(url_for('show_scene', scene_name=next_scene))
        
        scene_data = load_scene_data(scene_name)
        session['history'].append(scene_name)
        return render_template('scene.html', scene=scene_data)
    except Exception as e:
        return str(e), 500

@app.route('/choose', methods=['POST', 'GET'])
def choose():
    if request.method == 'POST':
        next_scene = request.form['next_scene']
        return redirect(url_for('show_scene', scene_name=next_scene))
    return render_template('choose.html')

@app.route('/reset', methods=['POST', 'GET'])
def reset():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

