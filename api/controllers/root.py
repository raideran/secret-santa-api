from flask_restful import Resource


class Root(Resource):
    def get(self):
        return {'welcome': 'Welcome to Secret Santa API please go to the link for further information',
                'link': 'http//www.japscr.com'}
