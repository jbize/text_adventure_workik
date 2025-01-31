
from flask import Flask, render_template, redirect, url_for, session, request
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_scene_data(scene_name):
    """
    Load the scene data from a JSON file.

    Args:
        scene_name (str): The name of the scene to load.

    Returns:
        dict: The data of the scene loaded from the JSON file.
    """
    with open(f'scenes/{scene_name}.json') as f:
        return json.load(f)

@app.route('/', methods=['GET'])
def home():
    """
    Redirect to the initial scene.

    Returns:
        Response: A redirect response to the 'show_scene' route with the 'begin' scene.
    """
    return redirect(url_for('show_scene', scene_name='begin'))

@app.route('/scene/<scene_name>', methods=['GET', 'POST'])
def show_scene(scene_name):
    """
    Display or process the current scene.

    Args:
        scene_name (str): The name of the scene to display.

    Returns:
        Response: A rendered template of the scene or a redirect to the next scene.
    """
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
    """
    Display the scene choice form or process the chosen scene.

    Returns:
        Response: A rendered template of the choice form or a redirect to the chosen scene.
    """
    if request.method == 'POST':
        next_scene = request.form['next_scene']
        return redirect(url_for('show_scene', scene_name=next_scene))
    return render_template('choose.html')

@app.route('/reset', methods=['POST', 'GET'])
def reset():
    """
    Clear the session and redirect to the home route.

    Returns:
        Response: A redirect response to the 'home' route.
    """
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
