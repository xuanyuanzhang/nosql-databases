##################################################################
# xz2580
# Xuanyuan Zhang
# NoSQL final project
##################################################################
# Put the use case you chose here. Then justify your database choice:
#
# Answer: 
# A public bike sharing website could be set up using mongodb database 
# Mongodb is the most powerful database among all four options from my
# point of view. It is good for storing large scale database with 
# complicated relations among tables. 
##################################################################
# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
# 
# Answer:
# Information on that specific server could not be displayed.
# A few replicas are created inside the server.  
##################################################################
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
# 
# Answer: 
# We should never lose user data in our app. We can have to manually set up 
# more replicas for this module. 
##################################################################

# Documentation.
# This app is called Mobike, which is a bike sharing app.
# To test on the application, simply run test.py under the directory.


import pymongo
import datetime
from pymongo import MongoClient
from pprint import pprint
from bson.binary import Binary

# Three users:
# Alex, Ben, Cathy

# fifteen objects:
# 4 bikes.
# 4 locations.
# 5 occupations.
# 2 deposits.
# 1 worker.
# 2 bike repair records.

# Table 1: bike.
def create_bike(db):
	db.bike.insert_many([
		{"ID": 1, "status": "unoccupied", "location": "Columbia University"},
		{"ID": 2, "status": "unoccupied", "location": "Central Park West"},
		{"ID": 3, "status": "unoccupied", "location": "Union Square"},
		{"ID": 4, "status": "unoccupied", "location": "Central Park West"},
		{"ID": 5, "status": "unoccupied", "location": "Columbus Circle"},
	])

# Table 2: user. 
def create_user(db):
	db.user.insert_many([
		{"username": "Alex","password": "password","deposit": 0},
		{"username": "Ben","password": "password","deposit": 0},
		{"username": "Cathy","password": "password","deposit": 0}
	])

# Table 3: location.
def create_location(db):
	db.location.insert_many([
		{"location": "Columbia University","bike number": 1},
		{"location": "Central Park West","bike number": 2},
		{"location": "Union Square","bike number": 1},
		{"location": "Columbus Circle","bike number": 1},
	])

# Table 4: occupation.
def create_occupation(db):
	date = datetime.datetime.now().strftime("%Y%m%d")
	db.occupation.insert_many([
		{"ID": 1, "bikeID": 3, "username": "Alex", "date": date, "cost": 3.0},
		{"ID": 2, "bikeID": 2, "username": "Ben", "date": date, "cost": 5.0},
		{"ID": 3, "bikeID": 1, "username": "Alex", "date": date, "cost": 1.5},
		{"ID": 4, "bikeID": 4, "username": "Cathy", "date": date, "cost": 1.0},
		{"ID": 5, "bikeID": 1, "username": "Cathy", "date": date, "cost": 2.5},
	])

# Table 5: deposit history.
def create_deposit(db):
	date = datetime.datetime.now().strftime("%Y%m%d")
	db.deposit.insert_many([
		{"username": "Ben", "date": date, "payment": 100.0},
		{"username": "Cathy", "date": date, "payment": 200.0},
	])

# Table 6: message.
def create_worker(db):
	db.worker.insert_one(
		{"name": "Jeff", "level": 3, "earning": 20},
	)

# Table 7: repair.
def create_repair(db):
	date = datetime.datetime.now().strftime("%Y%m%d")
	db.repair.insert_many([
		{"bikeID": 1, "name": "Jeff", "date": date},
		{"bikeID": 3, "name": "Jeff", "date": date}
	])

# Table 8: blacklist.
def create_blacklist(db):
	date = datetime.datetime.now().strftime("%Y%m%d")
	db.blacklist.insert_one(
		{"username": "Ben", "release": 30}
	)

# David is a student who lives 30 minutes walk away from Columbia.
# He wants to register for Mobike to come to school easier.

# First of all, David creates his account.
# Action 1: A user signs up for an account
def action_sign_up(db, username="david", password="ilikemobike"):
	db.user.insert_one(
		{
			"username": username,
			"password": password,
			"deposit": 0
		},
	)

# Then, David needs to make a deposit into his account in order to use the bike
# Action 2: A user makes a deposit to his account, creating a deposit history
def action_deposit(db, username="david", deposit=100.0):
	date = datetime.datetime.now().strftime("%Y%m%d")
	db.deposit.insert_one(
		{
			"username": username, "date": date, "payment": deposit,
		}
	)
	db.user.update_one(
		{"username": username},
		{'$inc': {"deposit": deposit}}
	)

# In the morning, David borrows a bike from Columbus Circle.
# Action 3: A user borrows a bike from certain station.
def action_borrow(db, username="david", ID=6, bikeID=3, location="Columbus Circle"):
	date = datetime.datetime.now().strftime("%Y%m%d")
	# first, set bike's state to occupied.
	db.bike.update(
		{"ID": bikeID},
		{
			'$set': {
		       "status": "occupied",
		       "location": "",
		     }
		}
	)
	# second, Columbus Circle will therefore have one less bike.
	db.location.update(
		{"location": location},
		{
			'$inc': {"bike number": -1},
		}
	)
	# third, the record will be stored in occupation. For now, cost is 0.
	db.occupation.insert_one(
		{"ID": ID, "bikeID": bikeID, "username": username, "date": date, "cost": 0.0}
	)

# After David arrives at Columbia University, he returns the bike.
# Action 4: A user returns the bike
def action_return(db, username="david", ID=6, bikeID=3, location="Columbia University", cost=4.0):
	# first, set bike's state to unoccupied.
	db.bike.update(
		{"ID": bikeID},
		{
			'$set': {
		       "status": "unoccupied",
		       "location": "Columbia University",
		     }
		}
	)
	# second, Columbia University will therefore have one more bike.
	db.location.update(
		{"location": location},
		{
			'$inc': {"bike number": 1},
		}
	)
	# third, the record in occupation will be updated based on the cost. 
	db.occupation.update(
		{"ID": ID},
		{
			'$set': {
				"cost": cost,
			}
		}
	)
	# fourth, money will be decreased from user account.
	db.user.update(
		{"username": username},
		{
			'$inc': {"deposit": -(int(cost))}
		}
	)

# Worker Jeff wants to check the number of bikes at a certain station.
# Action 5: Find out the number of bikes at a certain station.
def action_bike_count(db, location="Columbia University"):
	res = db.location.find({"location": location}, {"bike number": 1, "_id": 0})
	for ele in res:
		pprint(ele)

# Worker Jeff find a broken bike at Columbia University and repairs it.
# Action 6: Fix a bike and earn some money.
def action_bike_fix(db, worker="Jeff", bikeID=2, earning=30.0):
	date = datetime.datetime.now().strftime("%Y%m%d")
	db.repair.insert_one(
		{"bikeID": bikeID, "workername": "Jeff", "date": date}
	)
	db.worker.update(
		{"name": worker},
		{
			'$inc': {"earning": earning},
		}
	)

# Worker Jeff wants to trace who borrowed the bike today and try to contact the user.
# Action 7: Find who used a specific bike today.
def action_find_user(db, bikeID=3):
	date = datetime.datetime.now().strftime("%Y%m%d")
	res = db.occupation.find(
		{"bikeID": bikeID},
		{"username": 1, "_id": 0}
	)
	for ele in res:
		pprint(ele)

# Jeff finds out that David is the only user who is suspicious on breaking the bike and 
# decides to put him on the blacklist
# Action 8: Put some user onto the blacklist.
def action_blacklist(db, username="david", cost=30):
	db.blacklist.insert_one(
		{"username": username, "release": cost}
	)
