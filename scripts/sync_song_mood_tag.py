from music.models import Song

with open('result.txt', 'r', encoding='utf-8') as fi:
    data = fi.readlines()

for item in data:
    name, tag = item.split(';')
    song = Song.objects.filter(name=name.strip()).first()
    if song:
        song.mood = tag.strip()
        song.save()
        continue
    print('Error!! ', name, tag)
