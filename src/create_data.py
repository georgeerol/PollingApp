from app import db, app

db.app = app
db.init_app(app)
db.create_all()
from models import Options, Topics, Polls

topic = Topics(title='Which side is going to win the EPL this season')
arsenal = Options(name='Arsenal')
spurs = Options(name='Spurs')
poll = Polls(topic=topic, option=arsenal)
poll1 = Polls(topic=topic, option=spurs)
db.session.add(topic)
db.session.commit()
city = Options(name='Manchester city')
liverpool = Options(name='Liverpool FC')
liverpool = Polls(option=liverpool)
city = Polls(option=city)
new_topic = Topics(title='Whos better liverpool or city', options=[liverpool, city])
db.session.add(new_topic)
db.session.commit()
