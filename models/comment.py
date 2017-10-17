import time

from models import Model
from models.user import User



class Comment(Model):
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))
        self.created_time = form.get('created_time')
        self.updated_time = form.get('updated_time')

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    def is_owner(self, id):
        return self.user_id == id

    @classmethod
    def update(cls, id, form):
        c = cls.find(id)
        valid_names = [
            'content',
        ]
        for key in form:
            if key in valid_names:
                setattr(c, key, form[key])
        c.save()
