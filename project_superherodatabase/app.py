from flask import Flask, url_for,request,redirect,render_template,session
from os import environ
import datetime,sqlite3
from model import *
import sys

from config import *
import string


# run this when you run app.py => heroku does not run main function.
app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'



# DATABASE SETUP CODE
               			
def initsession(email):
	
	try:
		print "in session"
		session['logged_in'] = True
		session['user'] = email

	except Exception as inst:
		print inst,"Exception"
		

def closesession():
	try:
		session.pop('logged_in',None)
		session.pop('user',None)
		db_session.remove()
	except Exception as e:
		print e,"close session"
	# close the database session too
	

def checkforuser(email,pwd = None, login = False,register = False):
	
	if login:
		result = db_session.query(User).filter_by(email = email,password = pwd)
		print result.count(),"count here"
		if result.count() == 1:
			initsession(email)
			return {'error':False}		
		else:
			
			msg = 'invalid username or password'
			return {'error':True,'msg':msg}


	if register:
		result = db_session.query(User).filter_by(email = email)
		if result.count() > 0:
			msg = 'this user name already exists'
			
			return {'error':True,'msg':msg}

		else:
			#print email+pwd
			u = User(email,pwd)
			db_session.add(u)
			initsession(email)
			

			return {'error':False}

# register functions

@app.route('/register', methods = ['GET'])
def register():
	return render_template('register.html')

@app.route('/registerverify', methods = ['POST'])
def registerverify():
	
	email = request.form['email']
	pwd = request.form['password']

	result = checkforuser(email,pwd,False,True)
	#print result

	if result['error']:
		return render_template('register.html', message = result)
	else:

		#return render_template('register.html', message = result)
		print "logged in"
		return render_template('homepage.html')
		
		
#login functions		

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/verify', methods = ['POST'])
def verify():
	email = request.form['email']
	pwd = request.form['password']
	result = checkforuser(email,pwd,True,False)

	#print result


	if result['error']:
		return render_template('login.html',message = result)
	else:
		return render_template('homepage.html')
	
		
# logout functions
@app.route('/logout')
def logout():
	closesession()
	return render_template('homepage.html')	


# homepages
@app.route('/')
def default_url():
	return render_template('homepage.html')

@app.route('/home')
def home():
	return render_template('homepage.html')


#show association
@app.route('/allcharacters', methods = ['GET'])
@app.route('/allcharacters/<searchtext>', methods = ['GET'])

def allcharacters(searchtext = ""):
	#session.has_key('user')
	
	if searchtext != "":
		searchtext = searchtext+"%"
		#print searchtext

	else:
		searchtext = "%"  # this is blank query

	charrec = db_session.query(Characters).filter(Characters.CharacterAlias.like(searchtext)).all()
		

	charsbyalphabet = {}
	for letter in string.uppercase[:26]:
		charsbyalphabet[letter] = []

		
	for character in charrec:
		charsbyalphabet[character.CharacterAlias[0].upper()].append((character.CharacterAlias,character.CharacterImage,character.CharacterID))

		#print charsbyalphabet
		
	di = charsbyalphabet

	sortedlist = [(k,di[k]) for k in sorted(di.keys())]

	return render_template('allcharacters.html', charsbyalphabet= sortedlist)
	


@app.route('/creators', methods = ['GET'])


def allcreators():
	

	creatorrec = db_session.query(Creator).filter().all()
		

	creatorbyalphabet = {}
	for letter in string.uppercase[:26]:
		creatorbyalphabet[letter] = []

		
	for creator in creatorrec:
		
		chars = db_session.query(Characters).filter(Characters.CREATORS_CreatorID == creator.CreatorID).all()
		#
		creatorbyalphabet[creator.CreatorLastName[0].upper()].append((creator.CreatorLastName,creator.CreatorFirstName,chars))

		#print charsbyalphabet
	

	di = creatorbyalphabet

	sortedlist = [(k,di[k]) for k in sorted(di.keys())]
	#print sortedlist

	return render_template('creators.html', creatorbyalphabet= sortedlist)

@app.route('/universe', methods = ['GET'])


def alluniverse():
	
	universerec = db_session.query(Universe).filter().all()
		

	universebyalphabet = {}
	for letter in string.uppercase[:26]:
		universebyalphabet[letter] = []

		
	for universe in universerec:
		
		chars = db_session.query(Characters).filter(Characters.UNIVERSE_UniverseID == universe.UniverseID).all()
		#
		universebyalphabet[universe.UniverseName[0].upper()].append((universe.UniverseName,chars))

		#print charsbyalphabet
	

	di = universebyalphabet

	sortedlist = [(k,di[k]) for k in sorted(di.keys())]
	#print sortedlist

	return render_template('universe.html', universebyalphabet= sortedlist)
	
	

@app.route('/allteams', methods = ['GET'])
@app.route('/allteams/<searchtext>', methods = ['GET'])

def allteams(searchtext = ""):
	
	

	#query = 'select * from TEAM'
	#teamrec = db_session.execute(query)
	
	teamrec = db_session.query(Teams).all()
		

	teamsbyalphabet = {}
	for letter in string.uppercase[:26]:
		teamsbyalphabet[letter] = []

		
	for team in teamrec:
		team = team.__dict__

		#team = dict(team.items()) # convert team into a dictionary
		teamsbyalphabet[team['TeamName'][0].upper()].append((team['TeamName'],team['TeamID']))

		#print charsbyalphabet
		
	di = teamsbyalphabet

	sortedlist = [(k,di[k]) for k in sorted(di.keys())]

	return render_template('teams.html', teamsbyalphabet= sortedlist)



@app.route('/team/<teamid>', methods = ['GET'])
def team(teamid):
	


	#query = 'select * from TEAM where TeamID = '+'\''+teamid+'\'' 

	
	#print query,"team",teamid
	#teamrecs = db_session.execute(query)
	teamrecs = db_session.query(Teams).filter(Teams.TeamID == teamid).first()
	teamrec = ""

	teammembers = db_session.query(Characters,TeamHasChars).filter(TeamHasChars.TeamID == teamid).filter(TeamHasChars.CharcterID == Characters.CharacterID).all()

	memberrec = []	


	for member in teammembers:
		fname = member.Characters.CharacterFName
		lname = member.Characters.CharacterLName
		fullname = ""
		if fname!="NULL":
			fullname += str(fname)
		if lname!="NULL":
			fullname += str(lname)

		memberrec.append((member.Characters.CharacterID,member.Characters.CharacterAlias,fullname,member.Characters.CharacterImage))

	#only one team record
	teamrec = teamrecs.__dict__

	
	return render_template('team.html', teamrec = teamrec, memberrec = memberrec)


@app.route('/character/<charid>', methods = ['GET'])
def character(charid):
	
	char = db_session.query(Characters).filter(Characters.CharacterID == charid).first()
	

	if char.CharacterAlignment == 'Hero':
		rivals = db_session.query(HeroHasVillians,Characters).filter(HeroHasVillians.HeroID == charid).filter(HeroHasVillians.VillainID == Characters.CharacterID).all()
	else:
		rivals = db_session.query(HeroHasVillians,Characters).filter(HeroHasVillians.VillainID == charid).filter(HeroHasVillians.HeroID == Characters.CharacterID).all()
	
	
	equipment = db_session.query(CharHasEquip,Equipment).filter(CharHasEquip.CharacterID == charid).filter(CharHasEquip.EquipmentID == Equipment.EquipmentID).all()
	ability = db_session.query(CharHasAbility,Ability).filter(CharHasAbility.CharacterID == charid).filter(CharHasAbility.AbilityID == Ability.AbilityID).all()
	teams = db_session.query(TeamHasChars,Teams).filter(TeamHasChars.CharcterID == charid).filter(TeamHasChars.TeamID == Teams.TeamID).all()
	creator = db_session.query()

	return render_template('character.html', char = char, rivals = rivals, equipment = equipment, ability = ability, teams = teams)	

			
@app.route('/forum', methods = ['GET','POST'])
@app.route('/forum/<discussionid>', methods = ['GET'])

def forum(discussionid = None):

	if request.method == 'POST':
		request.form['discussion']
		return render_template('forum.html',forum = "")
		

	if discussionid == None and request.method == 'GET':

		discussions = db_session.query(Discussion).filter().all()
		return render_template('forum.html',discussions = discussions)
	

	if request.method == 'GET' and discussionid != None:	
		discussion = db_session.query(Discussion).filter(Discussion.DiscussionID == discussionid).first()
		comments = db_session.query(Comments).filter(Comments.DiscussionID == discussionid).all()
		

		return render_template('forumdetail.html',discussion = discussion,comments = comments)


@app.route('/nf')
def nf():
	return render_template('notfound.html')




if __name__ == '__main__':
	
	#configureserver()
	app.run(port = int('5000'))
	#app.run(port=int(environ['FLASK_PORT']))
	
	
	
	


	
 
