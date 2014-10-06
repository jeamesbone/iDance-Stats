from iDance.models import Song, Player, SystemHigh, Rank

def koth_matches(king, players, spread):
    scores = {}
    
    # Get the full list of scores for each player
    kingScores = Score.objects.filter(player=king)
    
    for player in players:
        scores[player] = Score.objects.filter(player=player)
        
    matches = []
    
    # Try and get matches for each song
    for song in Song.objects.all():
        highScoreIds = {}
        highScores = {}
        
        kingSongScores = kingScores.filter(song=song)
        kingHighScoreIds = []
        

        # Get the scores for this song from the player scores
        for player in players:
            songScores[player] = scores[player].filter(song=song)
            highScoreIds[player] = []
            
        for difficulty in song.difficulties():
            kingHighScoreIds += [kingSongScores.filter(difficulty=difficulty).order_by('-score')[0].id]
            for player in players:
                try:
                    highScoreIds[player] += [songScores[player].filter(difficulty=difficulty).order_by('-score')[0].id]
                except IndexError:
                    continue
                    
        kingHighScores = list(kingSongScores.filter(id__in=kingHighScoreIds))
        
        for player in players:       
            highScores[player] = list(songScores[player].filter(id__in=highScoreIds[player]))
        
        songMatches = [[] for i in len(kingHighScores)]
        for i, kscore in enumerate(kingHighScores):
            for j, player in enumerate(players):
                for pscore in highScores[player]:
                    if (kscore.score - pscore.score) < spread:
                        msongMatches[i] += [pscore]
                        break 
                    
                
        
        songMatches = []
            

def rankString(rank):
    if rank == Rank.easy:
        return "Easy"
    elif rank == Rank.normal:
        return "Normal"
    elif rank == Rank.hard:
        return "Hard"
    elif rank == Rank.expert:
        return "Expert"
    elif rank == Rank.master:
        return "Master"