from app import db
from extensions import db
from sqlalchemy.orm import relationship


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    versions = db.relationship('Version', backref='model', lazy=True)
    type = db.Column(db.String(50), nullable=False)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    data_type = db.Column(db.String(50), nullable=False)
    versions = db.relationship('Version', backref='dataset', lazy=True)

class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    version_number = db.Column(db.String(50), nullable=False)
    performance_metrics = db.Column(db.Text, nullable=True)

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False) # IPv4 address format
    model_versions = db.relationship('ModelDeployment', backref='server', lazy=True)

class ModelDeployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    version_id = db.Column(db.Integer, db.ForeignKey('version.id'), nullable=False)
    deployment_time = db.Column(db.Integer, nullable=False)


# At the end of the seed_data function, add:
#print("Database seeding completed successfully.")

# Or after each commit, add:
#print("Added model to the database.")
#print("Added dataset to the database.")
# And so on for each committed entity.