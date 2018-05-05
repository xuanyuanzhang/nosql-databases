import pymongo
import datetime
from pymongo import MongoClient
from pprint import pprint
from bson.binary import Binary
from final_project import *

client = MongoClient("mongodb://localhost")

print("connected")

if "mobike" in client.database_names():
	client.drop_database('mobike')

print("if database exists, drop database")

# Create a database named "hackernews"
db = client.mobike


def create_user_test():
	create_user(db)
	res = db.user.find()
	for ele in res:
		pprint(ele)

def create_bike_test():
	create_bike(db)
	res = db.bike.find()
	for ele in res:
		pprint(ele)

def create_location_test():
	create_location(db)
	res = db.location.find()
	for ele in res:
		pprint(ele)

def create_occupation_test():
	create_occupation(db)
	res = db.occupation.find()
	for ele in res:
		pprint(ele)

def create_deposit_test():
	create_deposit(db)
	res = db.deposit.find()
	for ele in res:
		pprint(ele)

def create_worker_test():
	create_worker(db)
	res = db.worker.find()
	for ele in res:
		pprint(ele)

def create_repair_test():
	create_repair(db)
	res = db.repair.find()
	for ele in res:
		pprint(ele)

def create_blacklist_test():
	create_blacklist(db)
	res = db.blacklist.find()
	for ele in res:
		pprint(ele)

def sign_up_test():
	print("\nbefore sign up\n")
	res = db.user.find()
	for ele in res:
		pprint(ele)
	action_sign_up(db)
	print("\nafter sign up\n")
	res = db.user.find()
	for ele in res:
		pprint(ele)

def deposit_test():
	print("\nbefore deposit\n")
	res = db.user.find({"username": "david"})
	for ele in res:
		pprint(ele)
	action_deposit(db)
	print("\nafter deposit\n")
	res = db.user.find({"username": "david"})
	for ele in res:
		pprint(ele)

def borrow_test():
	print("\nbefore borrow\n")
	print("##############################")
	res = db.location.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	res = db.bike.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	res = db.occupation.find()
	for ele in res:
		pprint(ele)
	action_borrow(db)
	print("\nafter borrow\n")
	print("##############################")
	res = db.location.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	res = db.bike.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	res = db.occupation.find()
	for ele in res:
		pprint(ele)

def return_test():
	print("\nbefore return\n")
	print("##############################")
	print("location")
	res = db.location.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	print("bike")
	res = db.bike.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	print("occupation")
	res = db.occupation.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	print("user")
	res = db.user.find()
	for ele in res:
		pprint(ele)
	action_return(db)
	print("\nafter return\n")
	print("##############################")
	print("location")
	res = db.location.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	print("bike")
	res = db.bike.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	print("occupation")
	res = db.occupation.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	print("user")
	res = db.user.find()
	for ele in res:
		pprint(ele)

def bike_count_test():
	print("##############################")
	print("bike count:")
	action_bike_count(db)

def bike_fix_test():
	print("\nbefore fix\n")
	print("##############################")
	res = db.repair.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	res = db.worker.find()
	for ele in res:
		pprint(ele)
	action_bike_fix(db)
	print("\nafter fix\n")
	print("##############################")
	res = db.repair.find()
	for ele in res:
		pprint(ele)
	print("##############################")
	res = db.worker.find()
	for ele in res:
		pprint(ele)

def action_find_user_test():
	print("##############################")
	action_find_user(db)

def action_blacklist_test():
	print("##############################")
	res = db.blacklist.find()
	for ele in res:
		pprint(ele)
	action_blacklist(db)
	print("\nafter fix\n")
	print("##############################")
	res = db.blacklist.find()
	for ele in res:
		pprint(ele)

def test_all():
	print("Generate users")
	create_user_test()
	print("\nGenerate articles\n")
	create_bike_test()
	print("\nGenerate comments\n")
	create_location_test()
	print("\nGenerate shows\n")
	create_occupation_test()
	print("\nGenerate ask\n")
	create_deposit_test()
	print("\nGenerate message\n")
	create_worker_test()
	print("\nGenerate job\n")
	create_repair_test()
	print("\nGenerate vote\n")
	create_blacklist_test()

	# create_bike(db)
	# create_user(db)
	# create_location(db)
	# create_occupation(db)
	# create_deposit(db)
	# create_worker(db)
	# create_repair(db)
	# create_blacklist(db)

	sign_up_test()
	deposit_test()
	borrow_test()
	return_test()
	bike_count_test()
	bike_fix_test()
	action_find_user_test()
	action_blacklist_test()


test_all()


