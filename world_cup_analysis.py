import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import string

# set up
url_june = 'https://www.skysports.com/fifa-world-cup-scores-fixtures/2026-06-01'
url_july = 'https://www.skysports.com/fifa-world-cup-scores-fixtures/2026-07-01'
page_june = requests.get(url_june)
page_july = requests.get(url_july)
soup_june = bs(page_june.text, 'html.parser')
soup_july = bs(page_july.text, 'html.parser')

# extract a list of scores
scoresx_june = soup_june.find_all('span', class_ = 'ui-sport-match-score__score')
scoresx_july = soup_july.find_all('span', class_ = 'ui-sport-match-score__score')
scores_june = []
scores_july = []

for i in range(len(scoresx_june)):
    check = scoresx_june[i].text.strip()
    if check.isdigit():
        scores_june.append(check)
        
for i in range(len(scoresx_july)):
    check = scoresx_july[i].text.strip()
    if check.isdigit():
        scores_july.append(check)
        
# extract a list of teams
teamsx_june = soup_june.find_all('span', class_ = 'ui-sport-match-score__team')
teamsx_july = soup_july.find_all('span', class_ = 'ui-sport-match-score__team')
teams_june = []
teams_july = []

# because website shows upcoming games that don't have a score yet
for i in range(len(scores_june)):
    check = teamsx_june[i].text.strip()
    teams_june.append(str(check))
    
for i in range(len(scores_july)):
    check = teamsx_july[i].text.strip()
    teams_july.append(str(check))

# check game status
statusx_june = soup_june.find_all('span', class_ = 'ui-sport-match-score__status')
statusx_july = soup_july.find_all('span', class_ = 'ui-sport-match-score__status')
status_june = []
status_july = []

for i in range(len(scores_june)):
    check = statusx_june[i].text.strip()
    if check == '':
        pass
    else:
        check = check.translate(str.maketrans('', '', string.punctuation))
        status_june.append(check)
for i in range(len(scores_july)):
    check = statusx_july[i].text.strip()
    if check == '':
        pass
    else:
        check = check.translate(str.maketrans('', '', string.punctuation))
        status_july.append(check)
    

# combine june and july
scores = scores_june
teams = teams_june
status = status_june

for i in range(len(scores_july)):
    scores.append(scores_july[i])
for i in range(len(teams_july)):
    teams.append(teams_july[i])
for i in range(len(status_july)):
    status.append(status_july[i])

# extract historic odds (new website)

#url2 = 'https://www.oddsportal.com/football/world/world-championship-2026/results/#/page/2/'
#page2 = requests.get(url2)
#soup2 = bs(page2.text, 'html.parser')
#odds = soup2.find_all('p', class_ = 'height-content !text-black-main next-m:min-w-[100%] flex-center min-h-full min-w-[50px] hover:!bg-gray-medium default-odds-bg-bgcolor border gradient-green-added-border')
#print(odds[0].text.strip())

odds = [3.5, 2.2, 2.6, 2.4, 6.5, 2.9, 3.6, 2.8, 25, 2.6, 2.1, 2.55, 13, 3.33, 3.5, 2.5, 3.55, 6.5, 3.2, 3.8, 5, 2.9, 2.25, 4.5, 2.55, 16/5, 5.5, 2.3, 17/5, 14/5, 10.5, 49/20, 3.1, 15/4, 8.5, 18/5, 12/1, 15/4, 4, 3, 3.5, 13, 2.5, 3.5, 8, 7, 19/5, 3.1, 21/5, 2.1, 21/4, 19/4, 3, 11/4, 29/4, 3.33, 2.6, 11, 29/20, 3, 5, 2.6, 2.5, 11/4, 9/5, 8, 47/20, 8, 3, 3, 23/20, 8, 2.5, 13/5, 4.3, 9/4, 12/5, 26/5, 183/100, 17/4, 13/5, 433/100, 17/4, 14/5, 23/10, 19/10, 17/2, 17/5, 12/5, 23/4, 29/10, 43/20, 13/5, 12/5, 4/1, 2/1, 3/1, 3/1, 59/20, 49/20, 23/10, 19/10, 333/100, 43/20]
    
# create x axis co-ordinates
team_pairs = []
for i in range(int(len(teams)/2)):
    team_pair = (teams[2*i], 'vs', teams[2*i+1])
    team_pair = str(team_pair)
    team_pair = team_pair.translate(str.maketrans('', '', string.punctuation))
    team_pairs.append(team_pair)

# work out if there was a draw and change money accordingly, creating y axis co-ordinates
money = 100
ymoney = []

for i in range(int(len(scores)/2)):
    if scores[2*i] == scores[2*i+1]:
        money = money + 100*odds[i]
    elif status[i] == 'AET\nExtra Time Full Time':
        money = money + 100*odds[i]
    else:
        money = money - 100
        
    ymoney.append(int(money))

# create start point
team_pairs.insert(0, 'START')
ymoney.insert(0, 100)
    
# create graph
font1 = {'family':'serif','color':'black','size':15}
font2 = {'family':'serif','color':'black','size':10}
font3 = {'family':'serif','color':'green','size':8}

#plt.figure(figsize=(12, 5))
plt.plot(team_pairs, ymoney, ms=8, marker='o', mfc = 'white', linewidth = 2.5)
plt.xticks(fontsize=6, rotation=90, ha='center')
plt.tight_layout()

plt.title('Performance of a £100 Flat Betting Strategy in the 2026 Football World Cup', fontdict = font1)
plt.xlabel('Match', fontdict = font2)
plt.ylabel('Cumulative Profit (£)', fontdict = font2)

plt.grid(axis = 'y')
plt.axhline(y=0, linestyle=':', color='black')
plt.axhline(y=(max(ymoney)), linestyle=':', color='green')
plt.axhline(y=(min(ymoney)), linestyle=':', color='red')
plt.text(x='START', y=max(ymoney)+27, s='MAX', fontdict = font3)
plt.text(x='START', y=min(ymoney)-100, s='MIN', fontdict = font3, color='red')

#plt.show()

# second graph
team_pairs.remove('START')
money2= 100
ymoney2 = []
team_pairs2 = []

for i in range(len(odds)):
    if odds[i] > 2.45:
        if scores[2*i] == scores[2*i+1]:
            money2 = money2 + 100*odds[i]
        elif status[i] == 'AET\nExtra Time Full Time':
            money2 = money2 + 100*odds[i]
        else:
            money2 = money2 - 100
        
        ymoney2.append(int(money2))
        team_pairs2.append(team_pairs[i])

team_pairs2.insert(0, 'START')
ymoney2.insert(0, 100)

plt.plot(team_pairs2, ymoney2, ms=8, marker='o', mfc = 'white', linewidth = 2.5)

plt.axhline(y=0, linestyle=':', color='black')
plt.axhline(y=(max(ymoney2)), linestyle=':', color='green')
plt.axhline(y=(min(ymoney2)), linestyle=':', color='red')
plt.text(x='START', y=max(ymoney2)+27, s='MAX', fontdict = font3)
#plt.text(x='START', y=min(ymoney2)-100, s='MIN', fontdict = font3, color='red')

plt.gcf().set_size_inches(16, 7)
plt.tight_layout()
plt.savefig("results.png", dpi=300, bbox_inches="tight")

plt.show()