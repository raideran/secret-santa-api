from flask_restful import Resource, reqparse, marshal_with, fields, abort
from api.models.user import UserModel
from ..utlis.data_validators import email_validator
from ..utlis.decorators import permission_required
from flask_jwt_extended import jwt_required, get_jwt_identity


resource_schema = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'admin': fields.Boolean
}


class UserController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required()
    @marshal_with(resource_schema)
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message=f'The user id: {user_id} was not found')
        return user, 200

    @marshal_with(resource_schema)
    @jwt_required()
    @permission_required()
    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message=f'The user id: {user_id} was not found')
        if user.id == get_jwt_identity():
            abort(403, message=f'A user cannot delete himself')
        user.delete()
        return user, 200

    @marshal_with(resource_schema)
    @jwt_required()
    def put(self, user_id):
        self.parser.add_argument('password', type=str, help='User password is missing', required=True)
        self.parser.add_argument('name', type=str, help='User name is missing', required=True)
        self.parser.add_argument('admin', type=bool, help='Admin value is missing', required=False)
        args = self.parser.parse_args()
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message=f'The user id: {user_id} was not found')
        user.set_all(args)
        user.store()
        return user, 200


class UsersController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required()
    @marshal_with(resource_schema)
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @marshal_with(resource_schema)
    def post(self):
        self.parser.add_argument('email', type=str, help='User email is missing', required=True)
        self.parser.add_argument('password', type=str, help='User password is missing', required=True)
        self.parser.add_argument('name', type=str, help='User name is missing', required=True)
        self.parser.add_argument('admin', type=bool, help='Admin value is missing', required=False)
        args = self.parser.parse_args()
        if not email_validator(args['email']):
            abort(400, message='Incorrect email address format')
        unique_email = UserModel.query.filter_by(email=args['email']).first()
        if unique_email:
            abort(409, message='Email address already exists')
        user = UserModel()
        user.set_all(args)
        user.store()
        return user, 201





