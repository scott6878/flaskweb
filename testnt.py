from collections import namedtuple

Song = namedtuple('Song', 'songno title likecnt')

print(Song, Song._fields)

s1 = Song(123, '만남', 100)
s2 = Song(songno=222, likecnt=200, title='강남스타일')
s2 = s2._replace(likecnt=201)
s3 = Song._make([333, 'Radio ga ga', 300])
s4 = Song( 444, 'Rady ga ga', 400 )

d1 = s1._asdict()
print(d1)

for s in [s1, s2, s3, s4]:
    print("s====>", s, s.title, getattr(s, 'title'))
