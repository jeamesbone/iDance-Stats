import itertools
import math

from datetime import datetime

from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from iDance import importer
from iDance.models import Player, Score, Song, SystemHigh

def importData(request):    
    log = importer.importSongs()
    log += importer.importData()
    return HttpResponse(log)
    
def songs(request):
    return Http404 

def playerScores(request):
    playerName = request.GET.get('player')
    if playerName:
        player = Player.objects.filter(name__iexact=playerName).last()
        #score_list = Score.objects.filter(player=player).values('song', 'player', 'difficulty').annotate(max_score=Max('score')).values('id')
        score_list = Score.objects.filter(player=player)
    else:
        score_list = Score.objects.all()
        
    songName = request.GET.get('song')
    songs = []
    
    if songName:
        songs = Song.objects.filter(name__icontains=songName)
        score_list = score_list.filter(song=songs)
    else:
        songs = Song.objects.all()
        
    if request.GET.get('high'):
        high_list = []
        for song in songs:
            song_score_list = score_list.filter(song=song)
            for difficulty in [i['difficulty'] for i in song_score_list.values('difficulty').distinct()]:
                high_list += [song_score_list.filter(difficulty=difficulty).order_by('-score')[0].id]
        score_list = score_list.filter(id__in=high_list).order_by('-difficulty')
    else:
        score_list = score_list.order_by('-dt', '-score')
        
    minDifficulty = request.GET.get('minDiff')
    if minDifficulty:
        score_list = score_list.filter(difficulty__gt=int(minDifficulty))
        
    maxDifficulty = request.GET.get('maxDiff')
    if maxDifficulty:
        score_list = score_list.filter(difficulty__lt=int(maxDifficulty))
        
    minScore = request.GET.get('minScore')
    if minScore:
        score_list = score_list.filter(score__gt=minScore)

    maxScore = request.GET.get('maxScore')
    if maxScore:
        score_list = score_list.filter(score__lt=maxScore)
    
    # Pagination
    paginator = Paginator(score_list, 50)
    page=request.GET.get('page')
    try:
        scores = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        scores = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        scores = paginator.page(paginator.num_pages)
        
    return render(request, 'scores.html', {"scores": scores})

def systemHighs(request):
    playerName = request.GET.get('player')
    if playerName:
        player = Player.objects.filter(name__iexact=playerName).last()
        #score_list = Score.objects.filter(player=player).values('song', 'player', 'difficulty').annotate(max_score=Max('score')).values('id')
        score_list = SystemHigh.objects.filter(score__player=player)
    else:
        score_list = SystemHigh.objects.all()
        
    songName = request.GET.get('song')
    songs = []
    
    if songName:
        songs = Song.objects.filter(name__icontains=songName)
        score_list = score_list.filter(song=songs)
    else:
        songs = Song.objects.all()
        
    minDifficulty = request.GET.get('minDiff')
    if minDifficulty:
        score_list = score_list.filter(difficulty__gt=int(minDifficulty))
        
    maxDifficulty = request.GET.get('maxDiff')
    if maxDifficulty:
        score_list = score_list.filter(difficulty__lt=int(maxDifficulty))
        
    minScore = request.GET.get('minScore')
    if minScore:
        score_list = score_list.filter(score__gt=minScore)

    maxScore = request.GET.get('maxScore')
    if maxScore:
        score_list = score_list.filter(score__lt=maxScore)    
    
    score_list = score_list.order_by('song__name', '-difficulty')
    
    # Pagination
    paginator = Paginator(score_list, 50)
    page=request.GET.get('page')
    try:
        scores = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        scores = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        scores = paginator.page(paginator.num_pages)
        
    return render(request, 'systemHighs.html', {"scores": [high.score for high in scores]})

def scores(request):    
    songName = request.GET.get('song')
    songs = []
    
    playerName = request.GET.get('player')
    if playerName:
        player = Player.objects.filter(name__iexact=playerName).last()
        #score_list = Score.objects.filter(player=player).values('song', 'player', 'difficulty').annotate(max_score=Max('score')).values('id')
        score_list = Score.objects.filter(player=player)
    else:
        score_list = Score.objects.all()
    
    if songName:
        songs = Song.objects.filter(name__icontains=songName)
        score_list = score_list.filter(song=songs)
    else:
        songs = Song.objects.all()
        
    minDifficulty = request.GET.get('minDiff')
    if minDifficulty:
        score_list = score_list.filter(difficulty__gt=int(minDifficulty))
        
    maxDifficulty = request.GET.get('maxDiff')
    if maxDifficulty:
        score_list = score_list.filter(difficulty__lt=int(maxDifficulty))
        
    minScore = request.GET.get('minScore')
    if minScore:
        score_list = score_list.filter(score__gt=minScore)

    maxScore = request.GET.get('maxScore')
    if maxScore:
        score_list = score_list.filter(score__lt=maxScore)    
    
    if request.GET.get('high'):
        high_list = []
        for song in songs:
            song_score_list = score_list.filter(song=song)
            for difficulty in [i['difficulty'] for i in song_score_list.values('difficulty').distinct()]:
                high_list += [song_score_list.filter(difficulty=difficulty).order_by('-score')[0].id]
        score_list = score_list.filter(id__in=high_list).order_by('-score')
    else:
        score_list = score_list.order_by('-dt', '-score')
        
    # Pagination
    paginator = Paginator(score_list, 999)
    page=request.GET.get('page')
    try:
        scores = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        scores = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        scores = paginator.page(paginator.num_pages)
        
    return render(request, 'scores.html', {"scores": scores})
    
def match(request):
    player1Name = request.GET.get('p1')
    player2Name = request.GET.get('p2')
    
    if not (player1Name and player2Name):
        return render(request, 'match.html') 
    
    spreadParam = request.GET.get('spread')
    if spreadParam:
        spread = float(spreadParam) / 100
    else:
        spread = 0.005
    
    player1 = Player.objects.filter(name__iexact=player1Name).last()
    score_list1 = Score.objects.filter(player=player1)
    
    player2 = Player.objects.filter(name__iexact=player2Name).last()
    score_list2 = Score.objects.filter(player=player2)
    
    matches = []
    
    for song in Song.objects.all():
        high_list1 = []
        high_list2 = []
        song_score_list1 = score_list1.filter(song=song)
        song_score_list2 = score_list2.filter(song=song)
        for difficulty in [i['difficulty'] for i in song_score_list1.values('difficulty').distinct()]:
            try:
                high_list1 += [song_score_list1.filter(difficulty=difficulty).order_by('-score')[0].id]
                high_list2 += [song_score_list2.filter(difficulty=difficulty).order_by('-score')[0].id]
            except IndexError:
                continue
        high_score_list1 = score_list1.filter(id__in=high_list1)
        high_score_list2 = score_list2.filter(id__in=high_list2)
        for score1 in high_score_list1:
            for score2 in high_score_list2:
                if abs(score1.score - score2.score) < spread:
                    matches += [(score1, score2)]
        #print matches
    return render(request, 'match.html', {"scores": matches}) 