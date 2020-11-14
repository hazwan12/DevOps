from datetime import datetime, timezone
from dateutil import tz
from devops import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

def local_time(time):
    utc = time
    utc = utc.replace(tzinfo=tz.tzutc())
    return utc.astimezone(tz.tzlocal())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    bugs = db.relationship('Bug', primaryjoin="User.id==Bug.user_id", backref="author")
    assigned_to = db.relationship('Bug', primaryjoin="User.id==Bug.developer_id", backref="assigned_to")
    reviewed_by = db.relationship('Bug', primaryjoin="User.id==Bug.reviewer_id", backref="reviewed_by")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=local_time(datetime.utcnow()))
    product = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    whatHappen = db.Column(db.Text, nullable=False)
    howHappen = db.Column(db.Text, nullable=False)
    shouldHappen = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    developer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    user = db.relationship("User", foreign_keys=[user_id])
    developer = db.relationship("User", foreign_keys=[developer_id])
    reviewer = db.relationship("User", foreign_keys=[reviewer_id])

    comments = db.relationship('Comment', primaryjoin="Bug.id==Comment.bug_id", backref="Comment")

    def __repr__(self):
        return f"Bug('{self.summary}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    bug_id = db.Column(db.Integer, db.ForeignKey('bug.id'), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=local_time(datetime.utcnow()))

    bug = db.relationship("Bug", foreign_keys=[bug_id])
    
    def __repr__(self):
        return f"Comment('{self.comment}', '{self.username}', ''{self.date_posted})"