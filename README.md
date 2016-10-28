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

I assign weights to each feature, and then apply those weights to each team's stat and sum them. As of week 7 through the NFL season this is how the ranking shows.

```python
rater.get_team_ranks(do_print=True)
```

rank |team|rating
-----|----|------
1|NE|0.396387607626
2|DAL|0.344677052322
3|MIN|0.311528325874
4|DEN|0.310645058168
5|PHI|0.301167487215
6|OAK|0.283635897615
7|BUF|0.273283468478
8|ATL|0.266490215905
9|SEA|0.245654445684
10|ARI|0.234369335938
11|GB|0.213914001591
12|PIT|0.212225265863
13|KC|0.210619607373
14|DET|0.20235043106
15|WAS|0.201847451607
16|SD|0.197070290522
17|NYG|0.192614314753
18|BAL|0.164524103496
19|IND|0.154067571058
20|TEN|0.151954292969
21|CIN|0.132816685834
22|LA|0.13217311859
23|TB|0.127529006717
24|HOU|0.111993472015
25|MIA|0.109722409003
26|NO|0.0820935156731
27|CAR|0.0569624467174
28|JAC|0.041280216755
29|NYJ|0.0393224770004
30|CHI|-0.00999466253563
31|SF|-0.0306032074746
32|CLE|-0.0766706857225


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
