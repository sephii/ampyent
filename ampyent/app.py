import logging

from flask import Flask, render_template, redirect, url_for
from application import ampyent_app

logging.basicConfig(level=logging.DEBUG)
print(ampyent_app.scenarios)

app = Flask(__name__)


@app.route('/')
def home():
    scenarios = ampyent_app.scenarios
    return render_template('home.html', scenarios=scenarios)


@app.route('/scenario/<scenario_name>/')
def show_scenario(scenario_name):
    selected_scenario = ampyent_app.get_scenario_by_name(scenario_name)

    return render_template('scenario.html', scenario=selected_scenario)


@app.route('/scenario/<scenario_name>/<scene_name>/')
def play_scene(scenario_name, scene_name):
    selected_scenario = ampyent_app.get_scenario_by_name(scenario_name)
    selected_scene = selected_scenario.get_scene_by_name(scene_name)

    ampyent_app.play_scene(selected_scene)

    return redirect(url_for('show_scenario', scenario_name=scenario_name))


@app.context_processor
def inject_current_scene():
    return dict(current_scene=ampyent_app.current_scene)

app.run(debug=True)
