from orm import Database
import os

db = Database('db.sqlite')


class Post(db.Model):

    text = str  # other datatypes: int, float

    def __init__(self, text):
        self.text = text


try:
    post = Post('Hello World').save()
    assert(post.id == 1)
    post.text = 'Hello Mundo'
    post.update()
    db.commit()
    post = Post.manager().get(id=1)
    assert(post.text == 'Hello Mundo')
    post.delete()
    db.commit()
    db.close()
finally:
    os.remove('db.sqlite')
