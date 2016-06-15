from app.app import app, db
from app import models
import datetime


db.drop_all()
db.get_engine(app).connect().execute(
    'DROP FUNCTION post_search_vector_update();'
)
db.configure_mappers()
db.create_all()

users = [
    models.User('admin', '1'),
    models.User('andre', '2'),
]

for user in users:
    db.session.add(user)
db.session.commit()

user_1 = models.User.query.filter(models.User.login == 'admin').first()
user_2 = models.User.query.filter(models.User.login == 'andre').first()

posts = [
    models.Post(
        'First Post', 'This is the first post of this blog',
        datetime.datetime.strptime("20091229050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'My Second Post', 'The second post after the first post of this blog',
        datetime.datetime.strptime("20101229050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ' +
        'non finibus turpis. Ut accumsan, risus sit amet posuere.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ' +
        'ornare accumsan viverra. Curabitur consequat vel ante nec ' +
        'sollicitudin. Morbi eu metus sagittis massa tincidunt mollis. Ut ' +
        'aliquam fringilla ipsum, ut condimentum nulla rutrum sed. Nam ' +
        'maximus ligula ante, vitae consequat sem lobortis interdum. ' +
        'Quisque ac nisi a lectus lobortis consequat eu in turpis. Aenean ' +
        'ornare ultrices augue, a hendrerit justo sodales non. Proin tempus ' +
        'velit gravida massa dignissim, vel malesuada lorem mollis. ' +
        'Praesent porta sit amet arcu quis interdum. Cras pellentesque ' +
        'euismod vestibulum.\n\nProin feugiat vitae nisi et vulputate. Nam ' +
        'ullamcorper eu nulla sit amet commodo. Nullam convallis risus vel ' +
        'enim hendrerit consequat.',
        datetime.datetime.strptime("20091230050936", "%Y%m%d%H%M%S"),
        user_2.id
    ),
    models.Post(
        'Lorem Ipsum',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ' +
        'ornare accumsan viverra. Curabitur consequat vel ante nec ' +
        'sollicitudin',
        datetime.datetime.strptime("20111229050936", "%Y%m%d%H%M%S"),
        user_2.id
    ),
    models.Post(
        'Nulla rutrum ut lectus id auctor',
        'Maecenas auctor ipsum nec sapien bibendum, nec varius nisl molestie',
        datetime.datetime.strptime("20151229050936", "%Y%m%d%H%M%S"),
        user_2.id
    ),
    models.Post(
        'Donec facilisis eget sapien non fermentum',
        'Phasellus ut sem eget elit viverra tempor. Donec varius dui eget ' +
        'arcu elementum placerat.',
        datetime.datetime.strptime("20141229050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Sed euismod facilisis consectetur',
        'Etiam et diam nulla. Sed et eros tincidunt felis laoreet porttitor.',
        datetime.datetime.strptime("20131229050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
]

for post in posts:
    db.session.add(post)
db.session.commit()
