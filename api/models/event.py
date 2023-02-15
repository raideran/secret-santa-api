from .base import Base, db


class EventModel(Base, db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255))
    amount = db.Column(db.Integer, default=0)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    raffled = db.Column(db.Boolean, default=False)

