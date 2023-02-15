from . import api
from .controllers import (Root, UserController, UsersController,
                          Login, EventsController, EventController)


api.add_resource(Root, '/', '/home')
api.add_resource(UserController, '/users/<int:user_id>')
api.add_resource(UsersController, '/users')
api.add_resource(Login, '/login')
api.add_resource(EventsController, '/events')
api.add_resource(EventController, '/events/<int:event_id>')
