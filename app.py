from flask import Flask, redirect, render_template, request, url_for
from group import Group

app = Flask(__name__)
# Création d'une liste vide pour stocker les groupes
groups = []

@app.route('/')
def home():
    return 'Hello, World!'
# Route pour afficher le formulaire de création de groupe
@app.route('/form_group', methods=['GET'])
def create_group_form():
    return render_template('form_group.html')

# Route pour traiter les données du formulaire de création de groupe
@app.route('/form_group', methods=['POST'])
def create_group():
    name = request.form['name']
    description = request.form['description']
    members = request.form['members']
    permissions = request.form['permissions']
    privacy = request.form['privacy']
    group = Group(name, description, members, permissions, privacy)
    groups.append(group)
    return redirect(url_for('list_groups'))

# Route pour afficher la liste des groupes
@app.route('/list_groups')
def group_list():
    return render_template('group_list.html', groups=groups)


if __name__ == '__main__':
    app.run()

