from sqlalchemy import Column, Integer, Float, String, DateTime, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, func, Table
from sqlalchemy.orm import relationship, backref
from helloflask.init_db import Base

class Album(Base):
    __tablename__ = 'Album'
    albumid = Column(String, primary_key=True)
    createdt = Column(String)
    title = Column(String)
    company = Column(String)
    genre = Column(String)
    likecnt = Column(Integer)
    rate = Column(Float)
    crawldt = Column(String)
    songs = relationship('Song')

class Song(Base):
    __tablename__ = 'Song'
    songno = Column(String, primary_key=True)
    title = Column(String)
    genre = Column(String)
    likecnt = Column(Integer)
    albumid = Column(String, ForeignKey('Album.albumid'), nullable=False)
    # album = relationship('Album', backref=backref('Album'))
    album = relationship('Album')
    songartists = relationship('SongArtist')

class SongRank(Base):
    __tablename__ = 'SongRank'
    id = Column(Integer, primary_key=True)
    rankdt = Column(String)
    songno = Column(String, ForeignKey('Song.songno'), nullable=False)
    rank = Column(Integer)
    song = relationship('Song')


def get_atype_name(atype):
    if atype == 1:
        return "작사"
    elif atype == 2:
        return "작곡"
    elif atype == 3:
        return "편곡"
    else:
        return "노래"

class SongArtist(Base):
    __tablename__ = 'SongArtist'
    songno = Column(String, ForeignKey('Song.songno'), nullable=False)
    artistid = Column(String, ForeignKey('Artist.artistid'))
    atype = Column(Integer)
    song = relationship('Song')
    artist = relationship('Artist')
    __table_args__ = (PrimaryKeyConstraint('songno', 'artistid', 'atype'), {})

    def atype_name(self):
        return get_atype_name(self.atype)

class Artist(Base):
    __tablename__ = 'Artist'
    artistid = Column(String, primary_key=True)
    name = Column(String)
    atype = Column(Integer)
    songartists = relationship('SongArtist')
    def atype_name(self):
        return get_atype_name(self.atype)


class Myalbum(Base):
    __tablename__ = 'Myalbum'
    def __init__(self, userid, songno):
        self.userid = userid
        self.songno = songno

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    songno = Column(String, ForeignKey('Song.songno'))
    upfile = Column(String)
    song = relationship('Song')

    def json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class MyalbumTable():
    def __init__(self):
        table = Table(self.__tablename__, MetaData(), self.useif, self.song)

class Mycom(Base):
    __tablename__ = 'Mycom'

    def __init__(self, myalbumid, writer, content):
        self.myalbumid = myalbumid
        self.writer = writer
        self.content = content

    id = Column(Integer, primary_key=True)
    myalbumid = Column(Integer)
    writer = Column(Integer, ForeignKey('User.id'))
    user = relationship('User')
    content = Column(String)
    writedate = Column(TIMESTAMP)

    def json(self, loginId):
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        j['writername'] = self.user.nickname
        j['isMine'] = self.writer == loginId
        j['writedate'] = self.writedate
        return j
    #    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SongInfo(Base):
    __tablename__ = 'v_sa_grp'
    id = Column(String, primary_key=True)
    songno = Column(String)
    names = Column(String)
    atype = Column(Integer)

    def atype_name(self):
        return get_atype_name(self.atype)

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    passwd = Column(String)
    nickname = Column(String)

    def __init__(self, email=None, passwd=None, nickname='손님', makeSha=False):
        self.email = email
        if makeSha:
            self.passwd = func.sha2(passwd, 256)
        else:
            self.passwd = passwd
        self.nickname = nickname

    def __repr__(self):
        return 'User %s, %r, %r' % (self.id, self.email, self.nickname)


class Ttt(Base):
    __tablename__ = 'Ttt'

    def __init__(self, myalbum, writer, content):
        self.myalbum = myalbum
        self.writer = writer
        self.content = content

    # id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True)
    myalbum = Column(Integer, ForeignKey('Myalbum.id'))
    writer = Column(Integer, ForeignKey('User.id'))
    content = Column(String)
    # writedate = Column(TIMESTAMP(timezone=True))
    writedate = Column(String)
    user = relationship('User')

    def json(self):
        print("99999999999999999999999999999999999999999",
              self.user.nickname, self.__table__.columns)
        j = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # j = {c: getattr(self, c) for c in ['content', 'writedate']}
        j['writername'] = self.user.nickname
        return j
