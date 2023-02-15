from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy
from os.path import isfile
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Video(name={self.name}, views={self.views}, likes={self.likes})'


if not isfile('database.db'):
    db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video is missing', required=True)
video_put_args.add_argument('likes', type=int, help='Number of likes is missing', required=True)
video_put_args.add_argument('views', type=int, help='Number views if the video is missing', required=True)


# Marshal approach
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer,
}


# Marshmallow approach
class VideoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'likes', 'views')


video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        return result

    def put(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], likes=args['likes'], views=args['views'])
        exists = VideoModel.query.filter_by(id=video_id).first()
        if exists:
            response = f'Video {video_id} was updated correctly'
        else:
            response = f'Video {video_id} was created correctly'
        db.session.add(video)
        db.session.commit()
        return {'info': response, 'data': marshal(video, resource_fields)}, 201

    def delete(self, video_id):
        if video_id not in videos:
            abort(404, message='This video does not exist')
        del videos[video_id]
        return f'Video {video_id} was deleted correctly', 200


class Videos(Resource):
    @marshal_with(resource_fields)
    def get(self):
        results = VideoModel.query.all()
        return results


class VideoM(Resource):
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        return video_schema.jsonify(result)


class VideosM(Resource):
    def get(self):
        results = VideoModel.query.all()
        return jsonify(videos_schema.dump(results))


api.add_resource(Video, '/video/<int:video_id>')
api.add_resource(Videos, '/videos')
api.add_resource(VideoM, '/videom/<int:video_id>')
api.add_resource(VideosM, '/videosm')
