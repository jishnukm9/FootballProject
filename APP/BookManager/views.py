
from flask import Blueprint,render_template,jsonify,redirect,url_for
import requests
import json
import pymongo
from flask import request
from mongoengine.queryset.visitor import Q
# import jsonify
# import ServerApi
from flask import Flask
from flask_pymongo import pymongo

from dotenv import load_dotenv
import os

def configure():
    load_dotenv()


BookManager = Blueprint("BookManager",__name__)

# from APP import db



from enum import unique
from mongoengine import connect
from mongoengine import Document, StringField, URLField,ObjectIdField
import json
import ast

username = 'jishnukm'

configure()
# uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + '/?authSource=' + authSource + '&authMechanism=' + authMechanism
uri='mongodb+srv://'+username+':'+os.getenv('password')+'@cluster0.vy8agxv.mongodb.net/?retryWrites=true&w=majority'
connect(db='football',host=uri)

class topscorers(Document):
	top = ObjectIdField()
	season = StringField()
	league = StringField()

class standings(Document):
	response = ObjectIdField()
	season = StringField()
	league = StringField()


class teams(Document):
    team=StringField()
    response=StringField()

class coaches(Document):
    coach=StringField()
    response=StringField()




# client = pymongo.MongoClient("mongodb+srv://jishnukm:<password>@cluster0.vy8agxv.mongodb.net/?retryWrites=true&w=majority")



@BookManager.route('/',methods=['GET','POST'])
def home():

    return render_template("new.html")


@BookManager.route('/teams',methods=['GET','POST'])
def func_teams():

    try:
        team=request.form['team'].lower()
    except:
        pass

    
    try:

        
        if team:
            obj=''
            obj=teams.objects(team=team)
        
        list_resp=[]
        for i in obj:
            dic={}
            dic['team']=i.team
            dic['response']=i.response

            list_resp.append(dic)

        print("\n fetching listof resp",list_resp)
   
        
        if list_resp==[]:
            try:
                if team:
                    url = "https://api-football-beta.p.rapidapi.com/teams"

                    querystring = {"search":team}

                    headers = {
                        "X-RapidAPI-Key": "920f279d8cmshc653063e61c176ep10d8fbjsn52435b179d34",
                        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
                    }

                    response = requests.request("GET", url, headers=headers, params=querystring)

                    team_j=response.json()['response']


                    print("\n response from api",team_j)



                    sav=teams(team=team,response=str(team_j))
                    sav.save()

                    print(sav)




                    obj=teams.objects(team=team)
            
                    list_resp=[]
                    for i in obj:
                        dic={}
                        dic['team']=i.team
                        dic['response']=i.response

                    list_resp.append(dic)

                
                    print("\n respo after api ..and db fetching",list_resp)

                else:
                    list_resp=[]
            except:
                list_resp=[]


    except:
        list_resp=[]



    print(list_resp)

    

    if list_resp != []:
        team_name=[]
        logo=[]
        stadium=[]
        capacity=[]
        country=[]
        founded=[]
        stad_image=[]
        city=[]
        print("\n type...........",type(list_resp[0]['response']))


        list_of_response=ast.literal_eval(list_resp[0]['response'])


        for i in list_of_response:
            team_name.append(i['team']['name'])
            logo.append(i['team']['logo'])
            country.append(i['team']['country'])
            founded.append(i['team']['founded'])
            stadium.append(i['venue']['name'])
            capacity.append(i['venue']['capacity'])
            stad_image.append(i['venue']['image'])
            city.append(i['venue']['city'])



        data_dict={
            'team_name':team_name,
            'logo':logo,
            'stadium':stadium,
            'capacity':capacity,
            'country':country,
            'founded':founded,
            'stad_image':stad_image,
            'city':city
        }


        print("\n data dict.....",data_dict)
    else:
        data_dict="-"


    try:
        length=len(team_name)
    except:
        length=0

    
    return render_template('team.html',data_dict=data_dict,length=length)


@BookManager.route('/home',methods=['GET','POST'])
def func_home():
    book_list=[]

    try:
        league = request.form['dr1']
        season = request.form['dr2']
    except:
    
        league="39"
        season="2021"

    if not league or not season:
        league="-"
        season="-"
        return render_template("index.html",season=season,league=league)
    
    print(league)
    print(season)
    obj=topscorers.objects(Q(season=season) & Q(league=league))
    print("\n obj length",len(obj))
    for i in obj:
        # print(i.season)
        book_list=i.top['response']

    length=len(book_list)

    with open('books.json','w') as f:
        json.dump(book_list,f)



    # db.football.topscorers.insert_one({"name":"jishnu"})
    print("\n book list",book_list)

    if season:
        
        season=season
    else:
        season="-"
    if league:
        if league=='39':
            league="Premier League"
        elif league=='61':
            league='Ligue 1'
        elif league=='135':
            league="Serie A"
        elif league=='78':
            league='Bundesliga'
        elif league=='140':
            league='La Liga'
 
    else:
        league="-"
    
    return render_template("index.html",length=length,book_list=book_list,season=season,league=league)



@BookManager.route('/standings',methods=['GET','POST'])
def func_standings():
    book_list=[]

    try:
        league = request.form['dr1']
        season = request.form['dr2']
    except:
    
        league="39"
        season="2021"
        pass


    
    
    # print(league)
    # print(season)
    obj=standings.objects(Q(season=season) & Q(league=league))
    print("\n obj length",len(obj))
    for i in obj:
        # print(i.season)
        book_list=i.response

    

    # with open('books.json','w') as f:
    #     json.dump(book_list,f)
    print("\n book list type",type(book_list))
    # book_list=ast.literal_eval(book_list)

    try:
        length=len(book_list['response'][0]['league']['standings'][0])
        book_list=book_list['response'][0]['league']['standings'][0]
    except:
        length=0
        book_list=[]

    # db.football.topscorers.insert_one({"name":"jishnu"})
    
    if season:
        
        season=season
    else:
        season="-"
    if league:
        if league=='39':
            league="Premier League"
        elif league=='61':
            league='Ligue 1'
        elif league=='135':
            league="Serie A"
        elif league=='78':
            league='Bundesliga'
        elif league=='140':
            league='La Liga'
 
    else:
        league="-"



    print(season)
    print(league)
    return render_template("standings.html",length=length,book_list=book_list,season=season,league=league)



@BookManager.route('/home_new/<season>/<league>',methods=['GET','POST'])
def func_home_new(season,league):
    book_list=[]

    print("\n 'start .../home_new/<season>/<league>'")
    
    # url = "https://api-football-beta.p.rapidapi.com/players/topscorers"

    # querystring = {"season":"2021","league":"39"}

    # headers = {
    #     "X-RapidAPI-Key": "920f279d8cmshc653063e61c176ep10d8fbjsn52435b179d34",
    #     "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # book_list=response.json()["response"]
    # try:
    #     league = request.form['ui_league']
    #     season = request.form['ui_season']
    # except:
    
    # league="39"
    # season="2021"
    
    
    obj=topscorers.objects(Q(season=season) & Q(league=league))

    for i in obj:
        print(i.season)
        print(i.league)
        book_list=i.top['response']

    length=len(book_list)
    print(book_list)
    with open('books.json','w') as f:
        json.dump(book_list,f)



    # db.football.topscorers.insert_one({"name":"jishnu"})

    print("\n 'end .../home_new/<season>/<league>'")
    return render_template("new.html",length=length,book_list=book_list)
    # return url_for("func_top",length=length,book_list=book_list)



@BookManager.route('/topscorers',methods=['GET','POST'])
def func_get_top():


    league = request.form['league_']
    season = request.form['season_']

    print("/topscorers", league)
    print("/topscorers",season)
    # book_list=[]
    # obj=topscorers.objects(Q(season=season) & Q(league=league))

    # for i in obj:
    #     print(i.season,"f")
    #     print(i.league,"f")
    #     book_list=i.top['response']

    # print(book_list)
    # player_name=book_list[i]['player']['name']
    # team=book_list[i]['statistics'][0]['team']['name']
    # return jsonify({"status":"success", "book_list":book_list})
    return redirect('/home_new/'+season+"/"+league)
    # return url_for('func_home_new',season=season,league=league)









@BookManager.route('/coaches',methods=['GET','POST'])
def func_coaches():

    try:
        coach=request.form['coach'].lower()
        print("\n coach input",coach)
    except:
        pass

    
    try:

        
        if coach:
            obj=''
            obj=coaches.objects(coach=coach)
        
        list_resp=[]
        for i in obj:
            dic={}
            dic['coach']=i.coach
            dic['response']=i.response

            list_resp.append(dic)

        print("\n fetching listof resp",list_resp)
   
        
        if list_resp==[]:
            try:
                if coach:
                    url = "https://api-football-beta.p.rapidapi.com/coachs"

                    querystring = {"search":coach}

                    headers = {
                        "X-RapidAPI-Key": "920f279d8cmshc653063e61c176ep10d8fbjsn52435b179d34",
                        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
                    }

                    response = requests.request("GET", url, headers=headers, params=querystring)

                    team_j=response.json()['response']


                    print("\n response from api",team_j)


                    if team_j==[]:
                        pass
                    else:
                        sav=coaches(coach=coach,response=str(team_j))
                        sav.save()

                    print(sav)




                    obj=coaches.objects(coach=coach)
            
                    list_resp=[]
                    for i in obj:
                        dic={}
                        dic['coach']=i.coach
                        dic['response']=i.response

                    list_resp.append(dic)

                
                    print("\n respo after api ..and db fetching",list_resp)

                else:
                    list_resp=[]
            except:
                list_resp=[]


    except:
        list_resp=[]



    print(list_resp)

    

    if list_resp != []:
 
        logo=[]
        age=[]
        firstname=[]
        lastname=[]
        birthdate=[]
        nation=[]
        place=[]
        team=[]
        logo_team=[]
        print("\n type...........",type(list_resp[0]['response']))


        list_of_response=ast.literal_eval(list_resp[0]['response'])


        for i in list_of_response:
            logo.append(i['photo'])
            firstname.append(i['firstname'])
            lastname.append(i['lastname'])
            age.append(i['age'])
            birthdate.append(i['birth']['date'])
            nation.append(i['birth']['country'])
            place.append(i['birth']['place'])
            team.append(i['team']['name'])
            logo_team.append(i['team']['logo'])



        data_dict={
            'image':logo,
   
            'age':age,
            'firstname':firstname,
            'lastname':lastname,
            'birthdate':birthdate,
            'nation':nation,
            'place':place,
            'team':team,
            'logo_team':logo_team
        }


        print("\n data dict.....",data_dict)
    else:
        data_dict="-"


    try:
        length=len(age)
    except:
        length=0

    
    return render_template('coach.html',data_dict=data_dict,length=length)
