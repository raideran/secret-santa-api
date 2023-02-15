from flask_restful import Resource, reqparse, marshal_with, fields, abort, inputs
from flask_jwt_extended import jwt_required
from api.models.event import EventModel
from api.models.user import UserModel


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date': fields.DateTime(dt_format="iso8601"),
    'location': fields.String,
    'amount': fields.Integer,
    'comment': fields.String,
    'user_id': fields.Integer,
    'raffled': fields.Boolean
}


class EventController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, event_id):
        event = EventModel.query.filter_by(id=event_id).first()
        if not event:
            abort(404, message=f'The event id: {event_id} was not found')
        return event, 200

    @marshal_with(resource_fields)
    @jwt_required()
    def delete(self, event_id):
        event = EventModel.query.filter_by(id=event_id).first()
        if not event:
            abort(404, message=f'The event id: {event} was not found')
        event.delete()
        return event, 200

    @marshal_with(resource_fields)
    @jwt_required()
    def put(self, event_id):
        self.parser.add_argument('name', type=str, help='Event name is missing', required=True)
        self.parser.add_argument('date', type=inputs.date, help='Event date is missing', required=True)
        self.parser.add_argument('location', type=str, required=False)
        self.parser.add_argument('amount', type=str, required=False)
        self.parser.add_argument('comment', type=str, required=False)
        args = self.parser.parse_args()
        event = EventModel.query.filter_by(id=event_id).first()
        if not event:
            abort(404, message=f'The event id: {event_id} was not found')
        event.set_all(args)
        event.store()
        return event, 200


class EventsController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self):
        events = EventModel.query.all()
        return events, 200

    @marshal_with(resource_fields)
    @jwt_required()
    def post(self):
        self.parser.add_argument('name', type=str, help='Event name is missing', required=True)
        self.parser.add_argument('date', type=inputs.date, help='Event date is missing', required=True)
        self.parser.add_argument('user_id', type=int, help='Event owner is missing', required=True)
        self.parser.add_argument('location', type=str, required=False)
        self.parser.add_argument('amount', type=str, required=False)
        self.parser.add_argument('comment', type=str, required=False)
        args = self.parser.parse_args()
        event = EventModel()
        event.set_all(args)
        owner_exists = UserModel.query.filter_by(id=event.user_id).first()
        if not owner_exists:
            abort(403, message='The owner of this event does not exist')
        event.store()
        return event, 201





