from flask_restful import Resource, reqparse, abort, fields, marshal, output_json
from api.models.user import UserModel
from flask_jwt_extended import create_access_token

resource_fields = {
    'id': fields.Integer,
}


class Login(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('email', type=str, help='User email is missing', required=True)
        self.parser.add_argument('password', type=str, help='User password is missing', required=True)
        args = self.parser.parse_args()
        user = UserModel.query.filter_by(email=args['email']).first()
        if not user:
            abort(404, message='The user is not registered')
        if not user.verify_password(args['password']):
            abort(401, message='Invalid credentials')
        token = create_access_token(identity=user.id)
        return {'user': marshal(user, resource_fields), 'token': token}



