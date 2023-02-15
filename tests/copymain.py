from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from os.path import isfile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)


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

videos = {}

class Video(Resource):
    def get(self, video_id):
        if video_id not in videos:
            abort(404, message='This video does not exist')
        return videos[video_id]

    def put(self, video_id):
        args = video_put_args.parse_args()
        response = ""
        if video_id in videos:
            response = f'Video {video_id} was updated correctly'
        else:
            response = f'Video {video_id} was created correctly'
        videos[video_id] = args
        return {'info': response, 'data': videos[video_id]}, 201

    def delete(self, video_id):
        if video_id not in videos:
            abort(404, message='This video does not exist')
        del videos[video_id]
        return f'Video {video_id} was deleted correctly', 200


api.add_resource(Video, '/video/<int:video_id>')
