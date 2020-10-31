# project/server/models.py


import datetime
from time import time
import jwt

from flask import current_app
from flask_login import UserMixin

from project.server import db, bcrypt
from project.server.database import PkModel, TimestampMixin


class User(UserMixin, PkModel):

    __tablename__ = "users"

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    strat_units = db.relationship('Stratigraphy', backref='user', lazy=True)

    def __init__(self, username, email, password, admin=False, **kwargs):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    @property
    def is_admin(self):
        return self.admin

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config.get('SECRET_KEY'), algorithm='HS256').decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config.get('SECRET_KEY'),
            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return "<User {0}>".format(self.username)

class Stratigraphy(PkModel, TimestampMixin):

    __tablename__ = "stratigraphy"

    unit_name = db.Column(db.String(50), nullable=False)
    ASUD_No = db.Column(db.Integer)
    ASUD_definition_card = db.Column(db.Boolean)
    strat_no = db.Column(db.Integer, nullable=False)
    map_symbol = db.Column(db.String(8))
    province = db.Column(db.String(60))
    domain = db.Column(db.String(60))
    unit_description = db.Column(db.String(500))
    unit_summary = db.Column(db.String(2000))
    type_locality = db.Column(db.String(300))
    unit_definition = db.Column(db.String(6000))
    unit_correlation = db.Column(db.String(2000))
    unit_distribution = db.Column(db.String(2000))
    unit_thickness = db.Column(db.String(2000))
    unit_lithology = db.Column(db.String(8000))
    unit_deposition_env = db.Column(db.String(4000))
    unit_contact_relations = db.Column(db.String(4000))
    unit_geochronology = db.Column(db.String(4000))
    unit_geochemistry = db.Column(db.String(4000))
    unit_geophysical_expression = db.Column(db.String(4000))
    references = db.Column(db.String(6000))
    compiler_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    edited_id = db.Column(db.String(80))
    
  
    def __repr__(self):
        return "<unit name {}>".format(self.unit_name)
    