
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from config import bcrypt, db
class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    
    missions = db.relationship("Mission", back_populates="planet", cascade="all, delete-orphan")
    scientists = association_proxy('missions', 'scientist')
    
    # Add serialization rules
    serialize_rules = ("-missions",)

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    
    missions = db.relationship("Mission", back_populates="scientist", cascade="all, delete-orphan")
    planets = association_proxy('missions', 'planet')

    # Add serialization rules
    serialize_rules = ("-missions",)

    # Add validation

    @validates('name', 'field_of_study')
    def validates_presence(self, key, value):
        if not value:
            raise ValueError(f"Scientists must have a {key}.")
        return value

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    # Add relationships
    
    planet = db.relationship("Planet", back_populates="missions")
    scientist = db.relationship("Scientist", back_populates="missions")

    # Add serialization rules
    serialize_rules = ("-scientist","-planet")

    # Add validation
    
    @validates('name', 'scientist_id', 'planet_id')
    def validates_presence(self, key, value):
        if not value:
            raise ValueError(f"Missions must have a {key}.")
        return value


# add any models you may need.

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
     
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    
    serialize_rules= ("-_password_hash",)
     
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))