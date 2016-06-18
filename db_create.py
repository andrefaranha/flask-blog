from app.app import app, db
from app import models
import datetime


POSTS_CONTENT = [
    """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at est
    utlibero egestas porttitor vitae non leo. Suspendisse nulla ex, viverra vel
    posuere ac, sollicitudin nec est. In pellentesque lectus lacus, eu
    condimentum lorem bibendum a. Suspendisse ultricies dui sit amet mi
    elementum, a porta nibh sagittis. Fusce pharetra ante sit amet tellus
    sagittis, eu tristique sapien maximus. Curabitur quis justo ex. Morbi
    egestas ullamcorper diam nec fringilla. Praesent in egestas magna. Aliquam
    porta nisi risus, pharetra luctus metus consequat eu. Ut dignissim, tortor
    at cursus ullamcorper, lorem ipsum fermentum tellus, ac auctor elit lacus
    sit amet ex. Vestibulum egestas ac erat id suscipit. Aenean sit amet
    faucibus purus.</p>

    <p>Sed nulla felis, pulvinar ullamcorper placerat sit amet, fringilla in
    mi. Etiam posuere est eget diam ornare scelerisque. Nullam porta sem id
    elit consectetur volutpat. Mauris justo odio, aliquam in lacus at, finibus
    dapibus nulla. Vivamus aliquam aliquam nisl eu congue. Vestibulum mauris
    leo, fermentum ac vehicula tempus, placerat eget augue. Aenean eget justo
    pulvinar, viverra velit quis, euismod tortor. Class aptent taciti sociosqu
    ad litora torquent per conubia nostra, per inceptos himenaeos. Sed metus
    est, fringilla non nibh ultrices, eleifend tempus ex. Nullam nisl felis,
    volutpat sit amet faucibus eget, pulvinar ac purus. Quisque vitae lorem et
    sem tincidunt gravida. Aenean tincidunt sodales nunc, quis consequat nisi
    vulputate nec. Nullam condimentum interdum turpis non dictum. Nullam
    porttitor ligula eget lacus ultrices, vitae commodo eros volutpat.
    Suspendisse at posuere nunc, lobortis malesuada risus.</p>

    <p>Proin gravida ipsum iaculis mattis eleifend. Fusce elementum dictum
    malesuada. Curabitur ut nibh luctus, lacinia nulla at, efficitur augue.
    Sed a est ipsum. Suspendisse nec diam eget est semper aliquam sit amet a
    nibh. Integer eu faucibus purus, sed bibendum magna. Donec ut lacus
    condimentum, commodo magna sit amet, pellentesque diam. Curabitur dui urna,
    auctor at felis vel, aliquet congue tortor. Praesent condimentum massa
    enim, at vestibulum ligula laoreet ac. Sed rutrum ante eleifend nibh
    faucibus, et molestie dolor bibendum. Quisque feugiat convallis ornare.
    Nulla in rutrum ipsum, nec pretium nulla. Nulla vestibulum imperdiet odio,
    vel fermentum erat fringilla ac. Aliquam bibendum, tellus ut porta
    sagittis, lacus ex interdum nisl, non convallis eros sapien auctor metus.
    Quisque lacus ligula, facilisis id mi at, vulputate consectetur sem.
    Mauris ac turpis aliquet, tincidunt turpis eu, tempor felis.</p>

    <p>Nam quis auctor nibh. Ut fermentum neque eu molestie facilisis. Duis
    eget egestas sem, sed convallis orci. Donec vel massa ac est vestibulum
    facilisis quis vitae libero. Aliquam erat volutpat. Sed egestas gravida
    massa, nec eleifend nisi tristique vestibulum. Nunc interdum pulvinar
    imperdiet. Aliquam erat volutpat. Curabitur enim purus, euismod vel
    iaculis vel, convallis quis lacus. Vivamus luctus consequat commodo.
    Curabitur neque dolor, pulvinar eu tempus eget, euismod nec metus. Quisque
    felis quam, luctus malesuada odio quis, tristique hendrerit ante. Aliquam
    erat volutpat. In in eros diam.</p>

    <p>Donec sollicitudin magna non nibh viverra, non finibus magna posuere.
    Curabitur pretium ligula lacus, quis cursus arcu ultricies elementum. In
    vitae dui sed magna feugiat facilisis eget a lorem. Mauris turpis dui,
    placerat ac massa sed, mollis commodo lorem. In suscipit nunc in neque
    lobortis, nec aliquam nulla ultricies. Donec dictum mi non tortor finibus
    porta. Morbi gravida, tortor sed consectetur mattis, neque nulla varius
    nisl, posuere tristique enim nisi nec quam. Aliquam in ex nulla. Duis
    gravida ut lacus in laoreet. Fusce non risus aliquet, consequat elit ut,
    pharetra neque. Donec vitae mollis lacus. In fringilla viverra nisi.
    Pellentesque tristique lectus nibh, ac sagittis quam mollis ac. Fusce
    mollis aliquet sapien, et finibus sem vestibulum quis.</p>""",
]


db.drop_all()
db.get_engine(app).connect().execute(
    'DROP FUNCTION IF EXISTS post_search_vector_update();'
)
db.configure_mappers()
db.create_all()

users = [
    models.User('admin', '1', 'Administrator'),
    models.User('hal', '2', 'Hal Jordan'),
]

for user in users:
    db.session.add(user)
db.session.commit()

user_1 = models.User.query.filter(models.User.login == 'admin').first()
user_2 = models.User.query.filter(models.User.login == 'hal').first()

posts = [
    models.Post(
        'First Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20091229050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'My Second Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20101228050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ' +
        'non finibus turpis. Ut accumsan, risus sit amet posuere.',
        POSTS_CONTENT[0],
        datetime.datetime.strptime("20091230050936", "%Y%m%d%H%M%S"),
        user_2.id
    ),
    models.Post(
        'Lorem Ipsum', POSTS_CONTENT[0],
        datetime.datetime.strptime("20111227050936", "%Y%m%d%H%M%S"),
        user_2.id
    ),
    models.Post(
        'Nulla rutrum ut lectus id auctor', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151226050936", "%Y%m%d%H%M%S"),
        user_2.id
    ),
    models.Post(
        'Donec facilisis eget sapien non fermentum', POSTS_CONTENT[0],
        datetime.datetime.strptime("20141225050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Sed euismod facilisis consectetur', POSTS_CONTENT[0],
        datetime.datetime.strptime("20131229050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Third Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151008050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Fourth Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151007050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Fifth Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151006050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Sixth Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151005050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Seventh Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151004050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Eighth Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151003050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Ninth Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151002050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
    models.Post(
        'Tenth Post', POSTS_CONTENT[0],
        datetime.datetime.strptime("20151001050936", "%Y%m%d%H%M%S"),
        user_1.id
    ),
]

for post in posts:
    db.session.add(post)
db.session.commit()


tags = [
    models.Tag('tag_a'),
    models.Tag('tag_b'),
    models.Tag('tag_c'),
    models.Tag('d'),
    models.Tag('e'),
    models.Tag('f'),
    models.Tag('g'),
    models.Tag('h'),
    models.Tag('i'),
    models.Tag('j'),
    models.Tag('k'),
    models.Tag('l'),
    models.Tag('m'),
    models.Tag('n'),
    models.Tag('o'),
    models.Tag('p'),
    models.Tag('q'),
    models.Tag('r'),
    models.Tag('s'),
    models.Tag('t'),
    models.Tag('u'),
    models.Tag('v'),
    models.Tag('w'),
    models.Tag('x'),
    models.Tag('y'),
    models.Tag('z'),
    models.Tag('ab'),
    models.Tag('ac'),
    models.Tag('ad'),
    models.Tag('ae'),
    models.Tag('af'),
    models.Tag('ag'),
    models.Tag('ah'),
    models.Tag('ai'),
    models.Tag('aj'),
    models.Tag('ak'),
    models.Tag('al'),
    models.Tag('am'),
    models.Tag('an'),
    models.Tag('ao'),
    models.Tag('ap'),
    models.Tag('aq'),
    models.Tag('ar'),
    models.Tag('as'),
    models.Tag('at'),
    models.Tag('au'),
    models.Tag('av'),
    models.Tag('aw'),
    models.Tag('ax'),
    models.Tag('ay'),
    models.Tag('az'),
]

for tag in tags:
    db.session.add(tag)
db.session.commit()

posts = models.Post.query.all()
for post in posts:
    post.tags.append(models.Tag.query.get(1))
    post.tags.append(models.Tag.query.get(2))
db.session.commit()
