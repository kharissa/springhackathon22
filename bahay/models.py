from bahay import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """ Given user's id, retrieves user from database. """
    return User.query.get(int(user_id))

UserTasks = db.Table('tags',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model, UserMixin):
    """ Represents a user with login information. """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=True)
    points = db.Column(db.Integer, nullable=True, default=0)
    history = db.relationship('History', backref=db.backref('user'), lazy=True) 

    def __repr__(self):
        """ Prints string of User. """
        return f"User('{self.id}', '{self.first_name}')"

class House(db.Model):
    """ Represents a household. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    rooms = db.relationship('Room', backref=db.backref('house'), lazy=True) 
    users = db.relationship('User', backref=db.backref('house'), lazy=True) 

    def __repr__(self):
        """ Prints string of House. """
        return f"House('{self.id}', '{self.name}')"

class Room(db.Model):
    """ Represents a room in a household. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    tasks = db.relationship('Task', backref=db.backref('room'), lazy=True) 

    def __repr__(self):
        """ Prints string of Room. """
        return f"Room('{self.id}', '{self.name}')"

class Task(db.Model):
    """ Represents a cleaning task in a room. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    history = db.relationship('History', backref=db.backref('task'), lazy=True) 

    def __repr__(self):
        """ Prints string of Task. """
        return f"Task('{self.id}', '{self.name}')"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    done_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)