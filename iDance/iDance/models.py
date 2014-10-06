import datetime
from django.db import models

class Rank(object):
    easy = 0
    normal = 1
    hard = 2
    expert = 3
    master = 4

class Song(models.Model):
    sid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    easy = models.IntegerField(null=True)
    normal = models.IntegerField(null=True)
    hard = models.IntegerField(null=True)
    expert = models.IntegerField(null=True)
    master = models.IntegerField(null=True)
    
    def __unicode__(self):
        return self.name
        
    def difficulties(self):
        return [self.easy, self.normal, self.hard, self.expert, self.master]
    
    def difficulty(self, rank):
        return self.difficulties[rank]
        
    def setDifficulties(self, difficulties):
        self.easy = difficulties[Rank.easy]
        self.normal = difficulties[Rank.normal]
        self.hard = difficulties[Rank.hard]
        self.expert = difficulties[Rank.expert]
        self.master = difficulties[Rank.master]
    
    def rank(self, difficulty):
        return self.difficulties().index(difficulty)

    
class Player(models.Model):
    #<person id="07G00000" name="SYSTEM" country="??" icon="0" pw="BF8F09292D1A1F9E94C616E310BF2824" deleted="0" />
    
    pid = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.IntegerField(blank=True)
    password = models.CharField(blank=True, max_length=100)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
    
class Score(models.Model):
    dt = models.DateTimeField(default=datetime.datetime.now)
    player = models.ForeignKey(Player, related_name="scores")
    song = models.ForeignKey(Song, related_name="scores")
    difficulty = models.IntegerField()
    score = models.FloatField()
    early = models.FloatField()
    late = models.FloatField()
    steps = models.IntegerField()
    oneStar = models.IntegerField()
    twoStar = models.IntegerField()
    threeStar = models.IntegerField()
    rank = models.IntegerField()    
    
    def __unicode__(self):
        return self.player.name + " - " + str(self.song) + " - " + str(self.score * 100) + "% - " + str(self.dt)

class SystemHigh(models.Model):
    song = models.ForeignKey(Song)
    difficulty = models.IntegerField()
    score = models.ForeignKey(Score)
    
    def __unicode__(self):
        return str(self.song) + " - " + str(self.difficulty) + " - " + str(self.score.player) + " - " + str(self.score.score * 100) + "%"