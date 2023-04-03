from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Groupe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80))
    description = db.Column(db.String(255))
    membres = db.Column(db.String(255))
    autorisations = db.Column(db.String(255))
    confidentialite = db.Column(db.Boolean)

    def __init__(self, name, description, members, permissions, privacy):
        self.name = name
        self.description = description
        self.members = members
        self.permissions = permissions
        self.privacy = privacy
