from app.routes import db


Club_Events = db.Table('Club_Events', db.Column('cid', db.Integer, db.ForeignKey('Clubs.id')), db.Column('eid', db.Integer, db.ForeignKey('Events.id', ondelete='CASCADE')))

Club_Notices = db.Table('Club_Notices', db.Column('cid', db.Integer, db.ForeignKey('Clubs.id')), db.Column('nid', db.Integer, db.ForeignKey('Notices.id', ondelete='CASCADE')))

Club_Photos = db.Table('Club_Photos', db.Column('cid', db.Integer, db.ForeignKey('Clubs.id')), db.Column('pid', db.Integer, db.ForeignKey('Photos.id', ondelete='CASCADE')))

Club_Teacher = db.Table('Club_Teacher', db.Column('cid', db.Integer, db.ForeignKey('Clubs.id')), db.Column('tid', db.Integer, db.ForeignKey('Teachers.id', ondelete='CASCADE')))

Club_User = db.Table('Club_User', db.Column('cid', db.Integer, db.ForeignKey('Clubs.id')), db.Column('uid', db.Integer, db.ForeignKey('User.id', ondelete='CASCADE')))


class Clubs(db.Model):
    __tablename__ = "Clubs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    pro_photo = db.Column(db.Text())
    club_room = db.Column(db.Text())
    organiser = db.Column(db.Text())
    events = db.relationship('Events', secondary='Club_Events', back_populates='clubs', cascade='all, delete')
    notices = db.relationship('Notices', secondary='Club_Notices', back_populates='clubs', cascade='all, delete')
    photos = db.relationship('Photos', secondary='Club_Photos', back_populates='clubs', cascade='all, delete')
    teachers = db.relationship('Teachers', secondary='Club_Teacher', back_populates='clubs', cascade='all, delete')
    User = db.relationship('User', secondary='Club_User', back_populates='clubs', cascade='all, delete')

    def __repr__(self):
        return self.name


class Events(db.Model):
    __tablename__ = "Events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    location = db.Column(db.Text())
    date = db.Column(db.Text())
    photo = db.Column(db.Text())
    clubs = db.relationship('Clubs', secondary='Club_Events', back_populates='events')

    def __repr__(self):
        return self.name


class Notices(db.Model):
    __tablename__ = "Notices"
    id = db.Column(db.Integer, primary_key=True)
    notice = db.Column(db.Text())
    date = db.Column(db.Text())
    photo = db.Column(db.Text())
    clubs = db.relationship('Clubs', secondary='Club_Notices', back_populates='notices')

    def __repr__(self):
        return self.name


class Photos(db.Model):
    __tablename__ = "Photos"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Text())
    description = db.Column(db.Text())
    clubs = db.relationship('Clubs', secondary='Club_Photos', back_populates='photos')

    def __repr__(self):
        return self.name


class Teachers(db.Model):
    __tablename__ = "Teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    email = db.Column(db.Text())
    password = db.Column(db.Text())
    picture = db.Column(db.Text())
    clubs = db.relationship('Clubs', secondary='Club_Teacher', back_populates='teachers')


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)
    email = db.Column(db.Text())
    password = db.Column(db.Text())
    picture = db.Column(db.Text())
    clubs = db.relationship('Clubs', secondary='Club_User', back_populates='User')
