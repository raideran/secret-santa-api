from .. import db


class Base:

    def set_all(self, args):
        for key, value in args.items():
            setattr(self, key, value)

    def store(self):
        db.session.add(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
