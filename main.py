from api import create_app, db
from api.models.user import UserModel
from api.models.event import EventModel
from flask_migrate import Migrate
from os import getenv

app = create_app(getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, UserModel=UserModel, EventModel=EventModel)

