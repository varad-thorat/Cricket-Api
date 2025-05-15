
import requests
from bs4 import BeautifulSoup
import re
import json


link = "https://www.cricbuzz.com/cricket-match/live-scores"
source = requests.get(link).text
page = BeautifulSoup(source, "lxml")

container = page.find("div", class_="cb-col cb-col-100 cb-bg-white")
matches = container.find_all("div", class_="cb-mtch-lst cb-col cb-col-100 cb-tms-itm")
# Match = match_details.find_all("a", class_="text-hvr-underline text-bold")
match = []

for card in matches:
    title = card.find("a",class_="text-hvr-underline text-bold")
    # print(title)
    if title:
        match.append(title.text.strip())
    else:
        match.append("")

match_no = []
for card in matches:
    title = card.find("span",class_="text-gray")
    # print(title)
    if title:
        match_no.append(re.sub(r'\&nbsp;\S*', '', title.text.strip()))
    else:
        match_no.append("")

date_stadium = []
for card in matches:
    title = card.find("div",class_="text-gray")
    # clean_title = re.sub()
    if title:
        date_stadium.append(re.sub(r'\xa0\S*', '', title.text.strip()))
    else:
        date_stadium.append("")

live = []
for card in matches:
    title = card.find("a", attrs={"title": "Live Score"})
    if title:
        text = title.text.strip()
        href = title["href"]
        live.append({"text": text, "url":href})
    else:
        live.append({"text": "Live Score", "url":""})
# print(live)

scorecard=[]
for card in matches:
    title = card.find("a", attrs={"title": "Scorecard"})
    if title:
        text = title.text.strip()
        href = title["href"]
        scorecard.append({"text": text, "url":href})
    else:
        scorecard.append({"text": "Scorecard", "url":""})
# print(scorecard)

FullCommentary=[]
for card in matches:
    title = card.find("a", attrs={"title": "Full Commentary"})
    if title:
        text = title.text.strip()
        href = title["href"]
        FullCommentary.append({"text": text, "url":href})
    else:
        FullCommentary.append({"text": "Full Commentary", "url":""})
    
# print(FullCommentary)
# # print(match)
# # print(match_no)
# # print(date_stadium)


teams = []

for card in matches:
    #match_status logic
    match_status = card.find("div", class_="cb-text-live") or card.find("div", class_="cb-text-complete") or card.find("span",class_="cb-text-preview")
    match_status = match_status.text.strip() if match_status else ""
    # print(match_status)

    all_cb_ovr_flo = card.find_all("div",class_="cb-ovr-flo")
    # print(len(all_cb_ovr_flo))

    try:
        team1 = all_cb_ovr_flo[1].text.strip() 
    except IndexError:
        team1 = ""

    try:
        team2 = all_cb_ovr_flo[3].text.strip() 
    except IndexError:
        team2 = ""
    
    try:
        score1 = all_cb_ovr_flo[2].text.strip() 
    except IndexError:
        score1 = ""
    
    try:
        score2 = all_cb_ovr_flo[4].text.strip() 
    except IndexError:
        score2 = ""

    team = {
        "team1": team1,
        "team2": team2,
        "score1": score1,
        "score2": score2,
        "match_status": match_status
    }

    teams.append(team)

# print(teams)

result = []

for i in range(len(match)):
    result.append({
        "match": match[i] if i < len(match) else "",
        "status": match_no[i] if i < len(match_no) else "",
        "date_stadium": date_stadium[i] if i < len(date_stadium) else "",
        "live_score": live[i]['url'] if i < len(live) else "",
        "scorecard": scorecard[i]['url'] if i < len(scorecard) else "",
        "commentary": FullCommentary[i]['url'] if i < len(FullCommentary) else "",
        "teams": teams[i]
    })

with open("matches.json", "w") as f:
    json.dump(result, f, indent=2)

print(result)

