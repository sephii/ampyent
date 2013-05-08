import logging

from flask import Flask, render_template, redirect, request, url_for
from application import ampyent_app
from scene import Scenario, Scene

logging.basicConfig(level=logging.DEBUG)
print(ampyent_app.scenarios)

app = Flask(__name__)


@app.route('/')
def home():
    scenarios = ampyent_app.scenarios
    return render_template('home.html', scenarios=scenarios)


@app.route('/scenarios/<scenario_name>/')
def show_scenario(scenario_name):
    selected_scenario = ampyent_app.get_scenario_by_name(scenario_name)

    return render_template('scenario_detail.html', scenario=selected_scenario)


@app.route('/scenarios/new/')
def create_scenario():
    return render_template('scenario_create.html')


@app.route('/scenarios/', methods=['POST'])
def create_scenario_post():
    scenario = Scenario(request.form['name'])
    ampyent_app._scenarios.append(scenario)
    return redirect(url_for('show_scenario', scenario_name=scenario.name))


@app.route('/scenarios/<scenario_name>/scenes/<scene_name>/')
def play_scene(scenario_name, scene_name):
    selected_scenario = ampyent_app.get_scenario_by_name(scenario_name)
    selected_scene = selected_scenario.get_scene_by_name(scene_name)

    ampyent_app.play_scene(selected_scene)

    return redirect(url_for('show_scenario', scenario_name=scenario_name))


@app.route('/scenarios/<scenario_name>/scenes/new/')
def create_scene(scenario_name):
    scenario = ampyent_app.get_scenario_by_name(scenario_name)
    return render_template('scene_create.html', scenario=scenario)


@app.route('/scenarios/<scenario_name>/scenes/', methods=['POST'])
def create_scene_post(scenario_name):
    scene = Scene(request.form['name'])
    selected_scenario = ampyent_app.get_scenario_by_name(scenario_name)
    selected_scenario.scenes.append(scene)

    return redirect(url_for('show_scenario', scenario_name=selected_scenario.name))


@app.context_processor
def inject_current_scene():
    return dict(current_scene=ampyent_app.current_scene)

app.run(debug=True)
