import numpy as np
import nflgame
from operator import itemgetter as ig
from copy import deepcopy as dc
import pandas as pd
#pf = points for ( total points scored)
#hpf = home points for
#hpa = home points against

#pa = points against ( total points opponents have scored)
#overall_performance (2 points for win, 1 for tie no points for loss.
#features = [pf, pa, ]

#we will have one data set such as this [win/loss, home/away, pf, pa]


class Rater(object):

    def __init__(self, league, start=True):
        self.league = league.lower()
        self.league_feature_ids = {'nfl':['op', 'hp', 'ap', 'pf', 'pa', 'hpf', 'hpa', 'apf', 'apa']}
        self.weights_list = {'nfl':np.array([1., 2., 3., 2., 2., 1.5, 2., 2., 1.5])}
        self.feature_ids = self.league_feature_ids[self.league]
        self.weights = self.weights_list[self.league]
        self.get_games = ''
        self.games = []
        self.teams = []
        self.records = {}
        self.adjusted_features = {}
        self.features = {}
        self.weighted_features = {}
        self.ranks = []
        self.split = []
        self.feature_table = []
        self.overall_rank=[]
        if start:
            self.get_ratings()
    
                    
    
    def get_overall_performance(self, record):
        ## Records here are given in  the format of [win or loss, home or away]
        ## the form is [2 for win, 0 for loss, 1 for tie, 1 for home and 0 for away]
        overall_performance = 0
        home_performance = 0
        away_performance = 0

        for game in record:
            overall_performance += game[0] * 1.
            if game[1] == 1:
                home_performance += game[0] * 1.
            else:
                away_performance += game[0] * 1.
        return overall_performance, home_performance, away_performance





    def get_points(self, record):
        tot_len = len(record)
        home_len = len([r for r in record if r[1] == 1]) * 1.
        away_len = len([r for r in record if r[1] == 0]) * 1.
        pf  =  sum([r[2] * 1. for r in record]) / tot_len
        hpf =  sum([r[2] * 1. for r in record if r[1] == 1]) / home_len
        hpa =  sum([r[3] * 1. for r in record if r[1] == 1]) * (-1. / home_len)
        pa  =  sum([r[3] * 1. for r in record]) * -1. / tot_len
        apf =  sum([r[2] * 1. for r in record if r[1] == 0]) / away_len
        apa =  sum([r[3] * 1. for r in record if r[1] == 0]) * ( -1. / away_len)
        return pf, hpf, apf, pa, hpa, apa


    def get_nfl_games(self, year, ending_week):
        weeks = range(1, ending_week + 1)
        games = nflgame.games(year, week=weeks)
        self.games = games


    def get_records(self, teams='', games=''):
        if teams == '':
            teams = self.teams
        if games == '':
            games = self.games
        records = {key: [] for key in teams}
        for game in games:
            home_team = game.home
            away_team = game.away
            if home_team == 'JAX':
                home_team = 'JAC'
            if away_team == 'JAX':
                away_team = 'JAC'
            away_points = game.score_away
            home_points = game.score_home
            away_winloss = 0
            home_winloss = 0
            if away_points > home_points:
                away_winloss = 2.
                home_winloss = 0.
            elif away_points < home_points:
                home_winloss = 2.
                away_winloss = 0.
            else:
                home_winloss = 1.
                away_winloss = 1.
            ## records in the form of [win/loss, home/away (1/0), pf, pa]
            home_info = [home_winloss, 1, home_points, away_points]
            away_info = [away_winloss, 0, away_points, home_points]
            records[home_team].append(home_info)
            records[away_team].append(away_info)
        self.records = records


    def get_max(self, features=''):
        if features == '':
            features = dc(self.features)
        sets = np.array([features[key] for key in features])
        maxs = []
        for i in range(0, len(sets[0])):
            maxs.append(max(abs(sets[:,i])))        
        return np.array(maxs)


    def apply_max(self, maxs, features=''):
        if features == '':
            features = dc(self.features)
        for team in features:
            features[team] = features[team]/maxs
        self.adjusted_features = features


    def apply_weights(self, unweighted_features='', weights=''):
        if unweighted_features == '':
            unweighted_features = dc(self.adjusted_features)
        if weights == '':
            weights = self.weights
        for team in unweighted_features:
            unweighted_features[team] =  sum(unweighted_features[team] * weights) 
        self.weighted_features = unweighted_features


    def get_team_ranks(self, summed_features='', do_print=False):
        rankings=[]
        if summed_features == '':
            summed_features = dc(self.weighted_features)
        columns = ['TEAM', 'RATING']
        if do_print:
            print "rank |team|rating"
            print "-----|----|------"
        i = 1
        for team, rating in sorted(summed_features.items(), key=ig(1), reverse=True):
            if do_print:
                print "{2}|{0}|{1}".format(team, rating, i)
            rankings.append([team, rating])
            i += 1
        df = pd.DataFrame(np.array(rankings), columns=columns)
        df.index += 1
        self.overall_rank = df
            


    def get_feature_ranks(self, features='', feature_id=''):
        feature_ranks = []
        f_len = 9
        for i in range(0, f_len):
            rank = []
            print ''
            print '***'
            print feature_id[i]
            print '***'
            for team, rating in sorted(features.items(), key=ig(i), reverse=True):                
                rank.append(team)
                print team, rating
            feature_ranks.append(rank)        
        self.feature_ranks = feature_ranks


    def split_features(self, adjusted_features=''):
        if adjusted_features == '':
            adjusted_features = dc(self.adjusted_features)
        split = []
        for i in range(0,9):
            new_features = {}
            for team in adjusted_features:
                new_features[team] = adjusted_features[team][i]
            split.append(new_features)
        self.split = split


    def get_split_ranks(self, split_feat='', feature_id='', do_print=False):
        if split_feat == '':
            split_feat = dc(self.split)
        if feature_id == '':
            feature_id = dc(self.feature_ids)
        feature_ranks = []
        f_len = len(feature_id)
        i = 0
        for feature in split_feat:
            rank = []
            if do_print:
                print ''
                print '***'
                print feature_id[i]
                print '***'
            for team in sorted(feature.items(), key=ig(1), reverse=True):
                rank.append(team[0])
                if do_print:
                    print team
            i += 1
            feature_ranks.append(rank)
        feature_ranks = np.array(feature_ranks)
        t_ranks = dc(feature_ranks).transpose()
        self.ranks = t_ranks

           
    def get_feature_sets(self, records=''):
        if records == '':
            records = self.records
        features = {key: [] for key in records}
        for team in records:
            record = records[team]
            pf, hpf, apf, pa, hpa, apa = self.get_points(record)
            op, hp, ap =  self.get_overall_performance(record)
            features[team] = [op, hp, ap, pf, pa, hpf, hpa, apf, apa]
        self.features = features


    def print_table(self):
        columns = 'rank|'
        for i in self.feature_ids:
            string = i
            if i != self.feature_ids[-1]:
                string = '{0}|'.format(i)
            columns += string
        below_cols = '---|'
        for i in self.feature_ids:
            string = '---'
            if i != self.feature_ids[-1]:
                string = '---|'
            below_cols += string
        row_len = len(self.ranks[0])
        index = 1
        datas = []
        for i in range(len(self.ranks)):
            string = '{0}|'.format(index)
            for j in range(len(self.ranks[i])):
                team =  self.ranks[i,j]
                if j != row_len - 1:
                    team = '{0}|'.format(self.ranks[i,j])
                string += team
            datas.append(string)
            index += 1

        print columns
        print below_cols
        for row in datas:
            print row


    def set_get_games(self):
        if self.league == 'nfl':
            self.get_games = self.get_nfl_games

        
    def get_teams(self, league= ''):
        if league == '':
            league = dc(self.league)
        if league == 'nfl':
            ## If it still has STL, remove it. Currently it does.
            self.teams = [t[0] for t in nflgame.teams if t[0] != 'STL']

    def get_feature_table(self):
        table = pd.DataFrame(self.ranks, columns=self.feature_ids)
        table.index += 1
        self.feature_table = table


    def get_ratings(self):
        self.set_get_games()
        self.get_games(2016, 7)
        self.get_teams()
        records = self.get_records()
        self.get_feature_sets()
        self.weights = self.weights / sum(self.weights)
        maxs = self.get_max()
        self.apply_max(maxs)
        self.apply_weights()
        self.split_features()
        self.get_team_ranks()
        self.get_split_ranks()
        self.get_feature_table()
        
        
        
                


if __name__ == '__main__':
##    games = get_games(2016, 7)
##    teams = [t[0] for t in nflgame.teams if t[0] != 'STL']
##    feature_id_short = ['op', 'hp', 'ap', 'pf', 'pa', 'hpf', 'hpa', 'apf', 'apa']
##    feature_ids = ['overall performance based on wins', 'hp', 'ap', 'points for', 'points allowed', 'home points for', 'home points allowed', 'away points for', 'away points allowed']
##    records =  get_records(teams, games)
##    features = get_feature_sets(records)
##    maxs = get_max(features)
##    adjusted_features = apply_max(maxs, dc(features))
##    weights = np.array([3., 1., 3., 2., 2., 1.5, 2., 2., 1.5])
##    #weights = np.array([2., 1., 3., 2., 2., 1.5, 2., 2., 1.5])
##    weights = weights / sum(weights)
##    weighted_features = apply_weights(dc(adjusted_features), weights)
##    split_up_features = split_features(adjusted_features)
##    get_team_ranks(weighted_features)
##    #feature_ranks = get_feature_ranks(adjusted_features, feature_ids )
##    transposed_ranks, ranks = get_split_ranks(split_up_features, feature_ids)
##    table = pd.DataFrame(transposed_ranks, columns=feature_id_short)
##    table.index += 1
##    print_table(transposed_ranks, feature_id_short)
    r = Rater('nfl')

    
    
## [op, hp, ap, pf, pa, hpf, hpa, apf, apa]  
##hpf = [r[2] for r in record if r[1] == 1]
##print hpf




##r1 = [0, 1, 24, 34]
##r2 = [2, 0, 35, 28]
##r3 = [2, 0, 45, 32]
##r4 = [2, 1, 48, 33]
##r5 = [2, 0, 23, 16]
##r6 = [0, 0, 24, 26]
##r7 = [0, 1, 30, 33]
##
##record = [r1, r2, r3, r4, r5, r6, r7]





