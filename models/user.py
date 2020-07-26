from peewee import Model, PrimaryKeyField, CharField

from utils import db


class User(Model):
    id = PrimaryKeyField()
    state = CharField(default='')

    def set_state(self, state: str):
        self.state = state
        self.save()

    def reset_state(self):
        self.state = ''
        self.save()
        
    class Meta:
        database = db
        db_table = 'users'
