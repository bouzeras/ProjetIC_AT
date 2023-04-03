from flask import Flask, render_template, request, redirect, url_for
from models import Groupe, db
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class Groupe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80))
    description = db.Column(db.String(255))
    membres = db.Column(db.String(255))
    autorisations = db.Column(db.String(255))
    confidentialite = db.Column(db.Boolean)

    def __init__(self, nom, description, membres, autorisations, confidentialite):
        self.nom = nom
        self.description = description
        self.membres = membres
        self.autorisations = autorisations
        self.confidentialite = confidentialite

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80))
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupe.id'), nullable=True)

    def __init__(self, nom, groupe_id=None):
        self.nom = nom
        self.groupe_id = groupe_id

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
    nom = request.form['nom']
    description = request.form['description']
    membres = int(request.form['membres'])
    last_group_config = request.form['last_group_config']

    # create group with empty members and generate an invitation link
    group = Groupe(nom, description, "", "", False)
    db.session.add(group)
    db.session.commit()
    invitation_link = url_for('join_group', groupe_id=group.id, _external=True)

    # generate group configuration based on user input and last group configuration
    if membres == 1:
        return redirect(url_for('home'))

    if last_group_config == 'LAST_MIN':
        group_size = membres // 2
        last_group_size = membres - group_size
    elif last_group_config == 'LAST_MAX':
        group_size = membres - 1
        last_group_size = 1
    else:
        group_size = membres // 2
        last_group_size = membres - group_size

    # add users to group
    for i in range(membres):
        if i == membres - 1 and last_group_size == 1:
            user = Utilisateur('Utilisateur ' + str(i + 1), group.id)
        elif i % group_size == 0:
            if i + group_size >= membres and last_group_size > 0:
                user = Utilisateur('Utilisateur ' + str(i + 1), group.id)
                last_group_size -= 1
            else:
                user = Utilisateur('Utilisateur ' + str(i + 1), group.id)
        else:
            user = Utilisateur('Utilisateur ' + str(i + 1))
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('group_list'))

# Route pour afficher la liste des groupes
@app.route('/group_list', methods=['GET'])
def group_list():
    groups = Groupe.query.all()
    return render_template('group_list.html', groups=groups)

    
# Route pour rejoindre un groupe aléatoire
@app.route('/join_random_group')
def join_random_group():
    groups = Groupe.query.filter_by(confidentialite=False).all()
    if len(groups) > 0:
        random_group = random.choice(groups)
        members = random_group.membres.split('-')
        if len(members) == 1:
            # Si le groupe n'a qu'un seul membre, on ne peut pas rejoindre
            return redirect(url_for('group_list'))
        elif len(members) == 2:
            # Si le groupe a deux membres, on rejoint le groupe et le groupe est supprimé
            db.session.delete(random_group)
            db.session.commit()
            return redirect(url_for('group_list'))
        else:
            # Si le groupe a plus de deux membres, on retire le premier membre de la liste des membres
            # et on met à jour la base de données
            new_members = '-'.join(members[1:])
            random_group.membres = new_members
            db.session.commit()
            return redirect(url_for('group_list'))
    else:
        return redirect(url_for('group_list'))
if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run()
