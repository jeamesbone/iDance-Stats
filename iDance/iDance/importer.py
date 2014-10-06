import csv
from datetime import datetime
from django.db.models import Max, Count
from BeautifulSoup import BeautifulSoup

from iDance.models import Player, Score, Song, SystemHigh

def importSongs(fileURL='songs.csv'):
    print 'Parsing CSV'
    
    with open(fileURL, 'rb') as csv_file:
        songs = []
        csv_reader = csv.reader(csv_file)
        for csv_line in csv_reader:
            csv_sid = int(csv_line[0])
            csv_name = csv_line[1]
            csv_diff = [csv_line[2], csv_line[3], csv_line[4], csv_line[5], csv_line[6]]
            try: 
                Song.objects.get(sid=csv_sid)
            except Song.DoesNotExist:
                song = Song()
                song.sid = csv_sid
                song.name = csv_name
                song.setDifficulties(csv_diff)
                print song.difficulties()
                songs += [song]
            
    print 'Saving Songs'
    Song.objects.bulk_create(songs)
    print 'Songs Saved'
    
    return '%d Songs added <br />' % len(songs)

def importData(fileURL='idance.xml'):
    print 'Parsing XML'
    
    data = open(fileURL)
    xml = BeautifulSoup(data)

    print 'XML Parsed'

    print 'Getting Players'
    players = []
    # Save all players to the database
    for playerXML in xml.idancestats.persons.findAll("person"):
        xml_id = playerXML['id']
        try:
            player = Player.objects.get(pid=xml_id)
        except Player.DoesNotExist:            
            player = Player()
            player.pid = xml_id
            player.name = playerXML['name']
            player.icon = int(playerXML['icon'])
            player.deleted = (playerXML['deleted'] == '1')
            #player.password = playerXML['password']  
            players += [player]
    
    Player.objects.bulk_create(players)
    print 'Players Saved'
    log = "%d Players updated <br />" % len(players)
    
    print 'Getting Scores'
    latest = Score.objects.aggregate(latest=Max('dt'))['latest']
        
    scores = []
    for scoreXML in xml.idancestats.log.findAll("score"):
        xml_dt = scoreXML['dt']
        
        if latest and datetime.strptime(xml_dt, "%Y-%m-%dT%H:%M:%S") < latest:
            continue
        
        xml_pid = scoreXML['pid']
        xml_player = Player.objects.get(pid=xml_pid)
        xml_sid = scoreXML['sid']
        xml_song = Song.objects.get(sid=xml_sid)
        try:
            score = Score.objects.get(dt=xml_dt, player=xml_player, song=xml_song)
        except Score.DoesNotExist:
            score = Score()
            score.dt = xml_dt
            score.player = xml_player
            score.song = xml_song
            score.difficulty = int(scoreXML['d'])
            if score.difficulty == 0:      
                continue
            score.score = float(scoreXML['p'])
            score.early = float(scoreXML['e'])
            score.late = float(scoreXML['l'])
            score.steps = int(scoreXML['c'])
            score.oneStar = int(scoreXML['s1'])
            score.twoStar = int(scoreXML['s2'])
            score.threeStar = int(scoreXML['s3'])
            score.rank = score.song.rank(score.difficulty)                       
            scores += [score]

    Score.objects.bulk_create(scores)
    print 'Scores Saved'

    print Score.objects.filter(difficulty=0)

    log += "%d Scores imported <br />" % len(scores)
    
    removeInactivePlayers()
    generateSystemHighs()
    
    return log 
    
def generateSystemHighs():
    print 'Getting System Highs'
    
    SystemHigh.objects.all().delete()
    
    systemHighs = []
    songs = Song.objects.all()
    for song in songs:
        songScores = Score.objects.filter(song=song)
        for difficulty in song.difficulties():
            difficultyScores = songScores.filter(difficulty=difficulty)
            if difficultyScores.count() > 0:
                maxScore = difficultyScores.aggregate(Max('score'))['score__max']
                score = difficultyScores.filter(score=maxScore).order_by('dt')[0]
                systemHighs += [SystemHigh(score=score, song=song, difficulty=difficulty)]
    SystemHigh.objects.bulk_create(systemHighs)
    
    print 'System Highs Saved'


def removeInactivePlayers():
    print 'Removing Inactive Players'
    players = Player.objects.annotate(num_scores=Count('scores')).filter(num_scores__lt=100)
    Score.objects.filter(player__in=players).delete()
    players.delete()
    print 'Inactive Players Removed'
    

    
