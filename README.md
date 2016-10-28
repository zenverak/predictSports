# predictSports


The goal of this is to eventually predict outcomes of games. However, for now it also will rate teams in a league based on certain features.


For the future I would like to add the following features

* more sports leagues.
  * currently this only works with the NFL. However if I can find some API's similar to nflGame then I can get all of the data I need
* neural netowrk capability so that it will be able to predict
* ability to save the pandas representation of my ratings to csv
* lint the code and add comments and argument descriptions


If you run this right now, it will create an object called r which is the Rater class. I will probably be changing some of this around to be more accureate to the classes purpose once I get more work done.


#RATER

a simple rater can look like this

```python
from LeagueRatings import Rater
rater = Rater('nfl')
```

with just that code you will then have the ability to get the overall rankings with default features and weights, if you would like to modify the weights before the code runs, you can do the following.

```python
rater = Rater(start=False)
rater.weights = new_weights #some list of weights
rater.get_ratings()
```


Right now the main functionality here is to rate the various teams in a league. Currently I am using 9 features

* op = overall performance. Basically total wins
* hp = home performance. Number of wins at home
* ap = away performance. Number of win on the road
* pf = points for. Total points scored
* pa = points allowed. Total points allowed
* hpf = home points for. Total points scored at home
* hpa = home points allowed. Total points allowed at home
* apf = away points for. Total points scored on the road
* apa = away points allowed. Total number of points allowed on the road

I assign weights to each feature, and then apply those weights to each team's stat and sum them. 

for the data below the normalized weights are as shown. They are in the same order as the features are listed above.

```python
rater.weights = array([ 0.16666667,  0.05555556,  0.16666667,  0.11111111,  0.11111111,
        0.08333333,  0.11111111,  0.11111111,  0.08333333])
```

As of week 7 through the NFL season this is how the ranking shows.

```python
rater.get_team_ranks(do_print=True)
```

rank |team|rating
-----|----|------
1|NE|0.443810518313
2|DAL|0.390343142008
3|OAK|0.346582051451
4|MIN|0.345147122584
5|DEN|0.344312925307
6|PHI|0.316843367555
7|ATL|0.311870389095
8|BUF|0.304397349859
9|SEA|0.273673643146
10|ARI|0.251441409868
11|WAS|0.236930000592
12|GB|0.234437297799
13|PIT|0.232842380723
14|KC|0.231325925482
15|NYG|0.228209815785
16|DET|0.223516147853
17|SD|0.213899718826
18|BAL|0.197050542191
19|TEN|0.185179054471
20|TB|0.175999617455
21|IND|0.173286039333
22|LA|0.166496834224
23|CIN|0.153215758843
24|HOU|0.124290130978
25|MIA|0.117515608503
26|NO|0.100680912951
27|JAC|0.0621350195279
28|NYJ|0.060286043093
29|CAR|0.0584274959738
30|CHI|-0.00480977387625
31|SF|-0.0242733996519
32|CLE|-0.0724112031824
>>> 



You can also see the output of where each team ranks on each feature
```python
r.print_table()
```

rank|op|hp|ap|pf|pa|hpf|hpa|apf|apa
---|---|---|---|---|---|---|---|---|---
1|NE|HOU|OAK|ATL|MIN|BUF|PHI|ATL|SEA
2|MIN|MIN|ATL|SD|SEA|NO|ARI|CAR|DEN
3|DEN|MIA|DAL|NO|PHI|ATL|MIN|OAK|BUF
4|OAK|DET|NE|IND|NE|SD|NE|SD|MIN
5|DAL|DEN|TB|CAR|ARI|IND|LA|NE|NE
6|SEA|NE|MIN|BUF|DEN|PIT|BAL|DAL|DAL
7|ATL|SEA|DEN|DAL|DAL|KC|DAL|DET|NYG
8|DET|PIT|BAL|OAK|BUF|PHI|KC|IND|WAS
9|NYG|GB|NYG|PHI|BAL|MIA|HOU|ARI|TEN
10|PIT|KC|TEN|NE|NYG|DAL|SEA|PHI|GB
11|HOU|PHI|WAS|DET|GB|SEA|PIT|DEN|MIA
12|GB|ARI|BUF|PIT|KC|GB|CIN|NO|PHI
13|WAS|CIN|LA|DEN|PIT|DEN|DEN|TB|OAK
14|KC|NYG|SEA|GB|HOU|WAS|CHI|TEN|BAL
15|PHI|DAL|DET|WAS|LA|MIN|SD|BAL|TB
16|BUF|WAS|CIN|ARI|MIA|OAK|GB|WAS|KC
17|ARI|BUF|NYJ|KC|TEN|HOU|DET|GB|ATL
18|MIA|IND|NO|MIN|CIN|CAR|NYG|LA|NO
19|CIN|SD|PIT|TB|WAS|CIN|CAR|SF|LA
20|BAL|CAR|GB|MIA|CHI|NYG|NYJ|BUF|PIT
21|TEN|ATL|JAC|TEN|DET|NE|SF|CLE|JAC
22|TB|NYJ|KC|SF|OAK|DET|MIA|MIN|ARI
23|LA|BAL|PHI|CIN|NYJ|ARI|BUF|PIT|CIN
24|IND|OAK|IND|JAC|SD|JAC|TEN|CIN|CHI
25|SD|TEN|ARI|BAL|TB|NYJ|WAS|KC|HOU
26|NYJ|NO|SD|NYG|JAC|SF|JAC|CHI|NYJ
27|NO|CHI|MIA|CLE|ATL|TEN|IND|NYG|DET
28|JAC|JAC|CAR|SEA|IND|TB|CLE|JAC|IND
29|CAR|LA|CHI|LA|CAR|BAL|OAK|NYJ|CLE
30|CHI|SF|CLE|NYJ|CLE|CLE|TB|MIA|SD
31|SF|TB|HOU|HOU|SF|CHI|ATL|SEA|CAR
32|CLE|CLE|SF|CHI|NO|LA|NO|HOU|SF
