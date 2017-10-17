from models import Model
from models.comment import Comment
from models.user import User


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)

    def is_owner(self, id):
        return self.user_id == id

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    def comments(self):
        return Comment.find_all(weibo_id=self.id)