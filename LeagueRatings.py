import numpy as np
import nflgame
import mlbgame
import nba_py as nbagame
from operator import itemgetter as ig
from copy import deepcopy as dc
import pandas as pd
import datetime as dt
import yaml
#pf = points for ( total points scored)
#hpf = home points for
#hpa = home points against

#pa = points against ( total points opponents have scored)
#overall_performance (2 points for win, 1 for tie no points for loss.
#features = [pf, pa, ]

#we will have one data set such as this [win/loss, home/away, pf, pa]

class NBA(object):
    def __init__(self, args):
        self.args = args


class MLB(object):
    ''' MLB class to extract information for feature analysis.

        Arguments:
            args: dictionary containing some default arguments.
                    Should at minimum be
                    {'year':''}
    '''

    def __init__(self, args, feature_ids, yaml_path='./mlb_code_mapping.yaml'):
        self.games = ''
        self.teams = ''
        self.records = ''
        self.code_map = {}
        self.args = args
        self.feature_ids = feature_ids
        self.yaml_path = yaml_path
        self._load_yaml()
        if args['year'] != '':
            self.get_games()
            self.remove_preseason_games()
            self.get_teams()
            self.get_records()


    def _load_yaml(self):
        try:
            code_map = open(self.yaml_path, 'r')
            self.code_map = yaml.load(code_map)
        except:
            print "file not found"


    def get_games(self, args=None):
        ''' This will retrieve the games using mlbgame

        arguments:
            args - If you want to send a different set of args in you can
        '''
        if args == None:
            args = self.args
        if args['year'] != '' and args['month'] == '':
            self.games = mlbgame.games(args['year'])
        elif args['year'] != '' and args['month'] != '':
            self.games = mlbgame.games(args['year'], args['month'])
        
        
    def remove_preseason_games(self, args=None ):
        '''This function removes preseason games based on the start of the season
        arguments:
            args - This should contain a start date that is a datetime.datetime object. defaults to None
        '''
        if args == None:
            start = self.args['start']
        games1 = self.games
        games2 = dc(games1)
        print "len of list one is {0} and len of list two is {1}".format(len(games1), len(games2))
        for i in range(0, len(games1)):       
            for j in range(0, len(games1[0])):
                game = games1[i][j]
                if game.date < start:
                    games2.pop(0)
                    break
        self.games = games2


    def get_stats(self, game):
        game_id = game.game_id
        try:
            stats = mlbgame.team_stats(game_id)
        except:
 #           print "CAN'T FIND a game with id of {0}".format(game_id)
            return [0]*18, [0]*18
        home_bat = stats['home_batting']
        away_bat = stats['away_batting']
        home_bat_stats = [home_bat.ab, home_bat.rbi, home_bat.bb, home_bat.avg, home_bat.h - home_bat.d - home_bat.t, home_bat.d, home_bat.t, home_bat.da, home_bat.hr, home_bat.lob, home_bat.obp, home_bat.ops
                          , home_bat.slg, home_bat.so]
        away_bat_stats= [away_bat.ab, away_bat.rbi, away_bat.bb, away_bat.avg, away_bat.h - away_bat.d - away_bat.t, away_bat.d, away_bat.t, away_bat.da, away_bat.hr, away_bat.lob, away_bat.obp, away_bat.ops
                          , away_bat.slg, away_bat.so]

        home_pitch = stats['home_pitching']
        away_pitch = stats['away_pitching']
        home_pitch_stats = [home_pitch.bf, home_pitch.er, home_pitch.era]
        away_pitch_stats = [away_pitch.bf, away_pitch.er, away_pitch.era]

        for stat1, stat2 in zip(home_pitch_stats, away_pitch_stats):
            home_bat_stats.append(stat1)
            away_bat_stats.append(stat2)
            
        return home_bat_stats, away_bat_stats



    def get_records(self, season=None, teams=None, start=None, end=None):
        ''' Takes in the seasons worth of data and creates a records dictionary

        arguments:
            season - This is a list where each entry from 0 to the end is a days worth of games. Defaults to none
            teams  - list of teams. Defaults to none
            start  - start date you want to get games for. Defaults to None
            end    - first day you do not want records for, ie start of postseason
        '''
        def _remove_no_play(records):
            for key in records:
                new_records = []
                for game in records[key]:
                    try:
                        if game[2] == game[3] and game[2] == 0:
                            pass
                        else:
                            new_records.append(game)
                    except:
                        print "This did not work at all for record {0}".format(game)
                        return records
                records[key] = new_records
            return records


        if start == None:
            start = self.args['start']
        if season == None:
            season = self.games
        if teams == None:
            teams = self.teams
        if end == None:
            end = self.args['end']
        
        records = {}
        not_count = {}
        for team in teams:
            records[team] = []
        for games in season:
            for game in games:
                if game.date < start or game.date >= end:
                    break
                home_team = game.home_team
                home_team_hits = game.home_team_hits
                home_team_runs = game.home_team_runs
                away_team = game.away_team
                away_team_hits = game.away_team_hits
                away_team_runs = game.away_team_runs
                if home_team in ['AL All-Stars', 'NL All-Stars']:
                    break

                if home_team_runs > away_team_runs:
                    ht_record = [2, 1, home_team_runs, away_team_runs, home_team_hits, away_team_hits]
                    at_record = [0, 0, away_team_runs, home_team_runs, away_team_hits, home_team_hits]
                else:
                    ht_record = [0, 1, home_team_runs, away_team_runs, home_team_hits, away_team_hits]
                    at_record = [2, 0, away_team_runs, home_team_runs, away_team_hits, home_team_hits]
                    


                home_other, away_other = self.get_stats(game)
                for stat1, stat2 in zip(home_other, away_other):
                    ht_record.append(stat1)
                    at_record.append(stat2)
                for stat1, stat2 in zip(home_other, away_other):
                    ht_record.append(stat2)
                    at_record.append(stat1)
                records[home_team].append(ht_record)
                records[away_team].append(at_record)
        records = _remove_no_play(records)
        self.records = records


    def get_teams(self, games=None):
        ''' gets the teams based on the games that have been played. Currently there is no easy to way to currate a list as there is from nflgame

            Arguments:
                games - games that have been played. If it contains all 30 teams it should be able create the needed list
        '''
        if games == None:
            games = self.games
        teams = []

        for i in range(0, len(games)):
            for game in games[i]:
                if game.home_team in ['NL All-Stars', 'AL All-Stars']:
                    pass
                elif game.away_team in ['NL All-Stars', 'AL All-Stars']:
                    pass
                else:
                    if game.home_team not in teams:
                        teams.append(game.home_team)
                    if game.away_team not in teams:
                        teams.append(game.away_team)
                    if len(teams)>= 30:
                        self.teams = teams



class NFL(object):
    ''' This class gathers NLF record information to later create features
        Arguments:
            args: args needs to atleast resemble the following
                {'year':'',
                'week':''}

            feature_ids:
                op = overall performance ( number of wins)
                hp = home performance  ( number of wins at home)
                ap = away performance  ( number of wins away)
                pf = point for
                pa = points alowed
                hpf = home points for
                hpa = home points allowed
                apf = away points for
                apa = away points allowed
                **for rest of these add h in front for these features at home and a in front for these features away rush as fd becomes hfd for home first downs
                fd = first downs
                ty = total yards
                py = passing yards
                ry = rushing yards
                pnt = number of penalties
                pnty = penalty yards
                to = turnovers
                fda = first downs allowed
                tya = total yards allowed
                pya = passying yards allowed
                rya = rushing yards allowed
                pnta = penalty yards allowed ( ie penalties opposing team got)
                pntya = penalty yards allowed ( or given by opponnent)
                tog = turn over gained
        '''
    
    def __init__(self, args, feature_ids, yaml_path='./nfl_code_mapping.yaml'):
        self.games = ''
        self.teams = ''
        self.records = ''
        self.args = args
        self.feature_ids = feature_ids
        self.codes = []
        self.weeks = args['week']
        self.year = args['year']
        self.yaml_path = yaml_path
        self.code_map = {}
        elf.get_teams()
        self._load_yaml()
        self.get_codes()

        if self.args['year'] != '' and self.args['week'] != '':
            self.get_games()
            self.get_records()


    def get_teams(self):
        ''' Gets the teams in the NFL '''

        self.teams = [t[0] for t in nflgame.teams if t[0] != 'STL']

    def _load_yaml(self):
        try:
            code_map = open(self.yaml_path, 'r')
            self.code_map = yaml.load(code_map)
        except:
            print "file not found"
        
        


    def get_codes(self, feature_ids=None):
        if feature_ids == None:
            feature_ids = self.feature_ids
        codes = []
        for feature in feature_ids:
            try:
                codes.append(self.code_map[feature])
            except:
                print "That code is not one we know"
        self.codes = codes
        

        

    
    def get_records(self, teams=None, games=None):
        ''' gets the records for teams so that we can create our features 
            Arguments:
                teams - list of teams. Defaults to None
                games - list of games
        '''
        if teams == None:
            teams = self.teams
        if games == None:
            games = self.games
        records = {key: [] for key in teams}
        for game in games:
            home_team = game.home
            away_team = game.away
            home_stats = game.stats_home
            away_stats = game.stats_away
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
            ## records in the form of [win/loss, home/away (1/0), pf, pa, fd, ty, py, ry, pnt, pty, to, ]
            home_info = [home_winloss, 1, home_points, away_points, home_stats[0], home_stats[1], home_stats[2], home_stats[3], home_stats[4], home_stats[5], home_stats[6],
                         away_stats[0], away_stats[1], away_stats[2] , away_stats[3], away_stats[4], away_stats[5], away_stats[5]]
            away_info = [away_winloss, 0, away_points, home_points, away_stats[0], away_stats[1], away_stats[2] , away_stats[3], away_stats[4], away_stats[5], away_stats[5],
                         home_stats[0], home_stats[1], home_stats[2], home_stats[3], home_stats[4], home_stats[5], home_stats[6]]
            records[home_team].append(home_info)
            records[away_team].append(away_info)
        self.records = records


    def get_games(self, year = None , ending_week = None, only_week=False):
        ''' This function sets self.games = the games for the year and week given

            arguments:
                year - 4 digit year. Leave blank if you already have specified the year when creating League object (default to '')
                ending_week - can be left emtpy, or a list, or an integer. Leave blank if you want to use the week/weeks specified in the creation of the class (defaults to '')
                only_week - a flag to set true if you only want the data given in the week set as ending_week

        '''
        is_list = isinstance(self.weeks, list)
        if year == None:
            year = self.year
        if ending_week == None and not is_list:
            weeks = range(1, self.weeks + 1)
        elif ending_week == None and is_list:
            weeks = self.weeks
        elif isinstance(ending_week, list):
            weeks = ending_week
        elif only_week:
            if ending_week != None:
                weeks = ending_week
            else:
                weeks = self.week
        else:
            weeks = range(1, ending_week + 1)

        games = nflgame.games(year, week=weeks)
        self.games = games


class Leagues(object):
    """ gets the data from the set specificied when calling the league object.


        aguments:
        league - league such as nfl, mlb, ncaaf, ncaab, nhl. It currently only works for nfl and mlb.
        year - year you want data from (default is blank)
        weeks - Weeks you want data from. This can be a list or integer.
        start - This can be used to define the start of the season for mlb seasons
        """


    def __init__(self, args, feature_ids, yaml_path=None):
        self.league_name = args['league'].lower()
        self.feature_ids = feature_ids
        self.yaml_path = yaml_path
        self.league = {}
        self.args = args
        self.get_league()


    def get_league(self):
        if self.league_name == 'nfl':
            if self.yaml_path == None:
                self.league = NFL(self.args, self.feature_ids)
            else:
                self.league = NFL(self.args, self.feature_ids, self.yaml_path)
        elif self.league_name =='mlb':
            if self.yaml_path == None:
                self.league = MLB(self.args, self.feature_ids)
            else:
                self.league = MLB(self.args, self.feature_ids, self.yaml_path)


class Rater(object):
    ''' function that takes in a league object and rates the varius teams in that league based on the features specified'''

    def __init__(self, league, start=True):
        self.league = league.league_name
        self.codes = league.league.codes#[[0, 'o', 'p','s'], [0, 'h', 'p','s'], [0, 'a', 'p','s'], [2, 'o','p','pg'],[2, 'h', 'p', 'pg'], [2, 'a', 'p', 'pg'], [3, 'o', 'n', 'pg'], [3, 'h', 'n', 'pg'], [3, 'a', 'n', 'pg']]
        self.weights_list = {'nfl':np.array([1., 2., 3., 2., 2., 1.5, 2., 2., 1.5]),
                             'mlb':np.array([1., 2., 3., 2., 2., 1.5, 2., 2., 1.5])}
        self.feature_ids = league.feature_ids
        self.weights = self.weights_list[self.league]
        self.games = league.league.games
        self.teams = league.league.teams
        self.records = league.league.records
        self.adjusted_features = {}
        self.features = {}
        self.weighted_features = {}
        self.ranks = []
        self.split = []
        self.feature_table = []
        self.overall_rank=[]
        if start:
            self.get_ratings()



    def calculate_per_game_features(self, record,  code, record_len, home_len, away_len):
        typ = code[1]
        index = code[0]
        where = None
        if code[2] == 'p':
            pm = 1.0
        else:
            pm = -1.0
        if typ == 'o':
            div = record_len * pm
        elif typ == 'h':
            div = home_len * pm
            where = 1
        elif typ == 'a':
            div = away_len * pm
            where = 0
        if where == None:
            return sum([r[index] * 1. for r in record]) / div
        else:
            return sum([r[index] * 1. for r in record if r[1] == where]) / div


    def calculate_season_features(self, record, code):
        typ = code[1]
        index = code[0]
        where = None
        if code[2] == 'p':
            pm = 1.0
        else:
            pm = -1.0
        if typ == 'h':
            where = 1
        elif typ == 'a':
            where = 0
        if where == None:
            return sum([r[index] * pm for r in record])
        else:
            return sum([r[index] * pm for r in record if r[1] == where])
        
        


    def calculate_features(self, record=None, codes=None):
        '''Will get all of the points summed up and averages

            arguments:
                record - the records for a team. Defaults to None
                codes  - codes used to determine how we calcluate a certain feature.

            returns:
                all point related features calculated
                
        '''
        if record == None:
            record = self.records
        if codes == None:
            codes = self.codes
        tot_len = len(record) * 1.

        if tot_len == 0.0:
            tot_len = 1.0
        home_len = len([r for r in record if r[1] == 1]) * 1.
        if home_len == 0.0:
            home_len = 1.
        away_len = len([r for r in record if r[1] == 0]) * 1.
        if away_len == 0.0:
            away_len = 1.
        features = []
        for i in range(0, len(self.feature_ids)):
            if codes[i][3] == 'pg':
                features.append(self.calculate_per_game_features(record, codes[i], tot_len, home_len, away_len))
            else:
                features.append(self.calculate_season_features(record, codes[i]))
        return np.array(features)


    def get_max(self, features=None):
        ''' this will get the max value for each feature for all teams

        arguments:
            features - The features we will get the max of
        return:
            returns all of the maxes in an np.array()
            '''
        if features == None:
            features = dc(self.features)
        sets = np.array([features[key] for key in features])
        maxs = []
        for i in range(0, len(sets[0])):
            maxs.append(max(abs(sets[:,i])))        
        return np.array(maxs)


    def apply_max(self, maxs, features=None):
        ''' Applies the maximums found in get_max

            Arguments:
                maxs - the maximums found in get_max
                features - features dictionary with teams that we will apply maxs to. Defaults to None
        '''
        if features == None:
            features = dc(self.features)
        for team in features:
            features[team] = features[team]/maxs
        self.adjusted_features = features


    def apply_weights(self, unweighted_features=None, weights=None):
        ''' applies the weights and sum the values to get a score for each team
            Arguments:
                unweighted_features - features that have been adjusted for maxs, but not weighted. Defaults to None
                weights - weights to give importance to each feature
                
        '''
        if unweighted_features == None:
            unweighted_features = dc(self.adjusted_features)
        if weights == None:
            weights = self.weights
        for team in unweighted_features:
            unweighted_features[team] =  sum(unweighted_features[team] * weights) 
        self.weighted_features = unweighted_features


    def get_team_ranks(self, summed_features=None, do_print=False):
        '''Creates the team rankings and also can print a table. Saves the output in a pandas dataframe

            Arguments:
                summed_features - the output of apply_weights. Defaults to None
        '''
        rankings=[]
        if summed_features == None:
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
        if do_print:
            return
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


    def split_features(self, adjusted_features=None):
        '''splits the features up so that we can rate each team on each feature

            Arguments:
                adjust_features - features that have been adjusted by maxes. Weights don't matter here because they won't change who was higher or lower. Defaults to None
        '''
        if adjusted_features == None:
            adjusted_features = dc(self.adjusted_features)
        split = []
        for i in range(0,9):
            new_features = {}
            for team in adjusted_features:
                new_features[team] = adjusted_features[team][i]
            split.append(new_features)
        self.split = split


        


    def get_split_ranks(self, split_feat=None, feature_id=None, do_print=False):
        '''Creates the rankings for each team based on the splits. Stores the result in a pandas data frame in self.ranks
            Arguments:
                split_feat - This is the result from split_features
                feature_id - the features that we are using. This will give us a column name for the table
        '''
        if split_feat == None:
            split_feat = dc(self.split)
        if feature_id == None:
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

           
    def get_feature_sets(self, records=None):
        ''' this combines the output from get_overall_performance and get_points to create a feature set for each team
            Arguments:
                records - the records that we be fed into get_points and get_overall_performance. Defaults to None
            '''
        if records == None:
            records = self.records
        features = {key: [] for key in records}
        for team in records:
            record = records[team]            
            features[team] = self.calculate_features(record)
        self.features = features


    def print_table(self):
        '''prints self.ranks '''
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


    def get_feature_table(self):
        ''' takes self.ranks and creates dataframe to store in a table '''
        table = pd.DataFrame(self.ranks, columns=self.feature_ids)
        table.index += 1
        self.feature_table = table


    def get_ratings(self):
        ''' function goes through the process of getting all of the ratings done'''
        self.get_feature_sets()
        self.weights = self.weights / sum(self.weights)
        maxs = self.get_max()
        self.apply_max(maxs)
        self.apply_weights()
        self.split_features()
        self.get_team_ranks()
        self.get_split_ranks()
        self.get_feature_table()


    def get_teams_ind_ratings(self, team):
        ''' function used find where a team ranks on each feature
            arguments:
                team - team to search for
            returns:
                ratings for that team
        '''
        ratings = []
        for feature in self.feature_ids:
            ratings.append(self.feature_table[self.feature_table[feature] == team].index[0])
        return ratings
        
        
        
                


if __name__ == '__main__':
    args1 = {'league':'mlb',
            'year':2016,
            'week':8,
            'month':''}
    args2 = {'league':'nfl',
             'year':2016,
             'week':8}
    #l = Leagues(args)
    start = dt.datetime(2016, 4, 3)
    end = dt.datetime(2016, 10, 2)
    args1['start'] = start
    args1['end'] = end
    fid = ['op', 'hp', 'ap']
    mlb = Leagues(args1, fid)
    #nfl = Leagues(args2, fid)
    #mlb_rate = Rater(mlb)
    #nfl_rate = Rater(nfl)
