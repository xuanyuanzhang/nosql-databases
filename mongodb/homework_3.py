import pymongo
from pprint import pprint

conn = pymongo.MongoClient()
db = conn.movies
cl = db.movie_collection

# 1. change "NOT RATED" to "Pending rating"
db.movie_collection.update_many(
	{ u'rated': u'NOT RATED'},
	{ "$set": { u'rated': u'Pending rating'} }
)

# 2. insert a new movie
db.movie_collection.insert_one({
	"title": "The Shape of Water",
	"year": 2017,
	"countries": ["USA"],
	"genres": ["Adventure", "Drama", "Fantasy", "Horror", "Romance", "Thriller"],
	"directors": ["Guillermo del Toro"],
	"imdb": {
	"id":5580390,
	"rating": 7.5,
	"votes": 196543,
	}
});

# 3. find total number of movies in drama
drama_movies = db.movie_collection.aggregate([
	{"$match": {"genres": "Drama"}},
	{"$group": {"_id": "Drama", "count": {"$sum": 1}}}
])
print("movies in drama")
for ele in drama_movies:
	pprint(ele)

# 4. find number of movies made in China
# this is kinda tricky.
# What I get here are the movies only produced by China.
# without "[]", we will get all movies including China
# as one of the countries.
# It is not specified clearly what is expected.
china_movies = db.movie_collection.aggregate([
        {"$match": {"countries": ["China"], "rated": "Pending rating"}},
        {"$group": {"_id": {"countries": ["China"], "rated": "Pending rating"}, "count": {"$sum": 1}}}
])
print("movies in china")
for ele in china_movies:
	pprint(ele)

# 5. test lookup and return at least two results
db.team.insert([
	{"group": "RNG", "members": ["Xiaohu", "MLXG", "UZI", "Ming", "ZziTai"]},
	{"group": "WE", "members": ["Xiye", "Mystic", "Condi", "957", "Magic"]},
	{"group": "EDG", "members": ["Clearlove7", "Meiko", "Mouse", "Scout", "Audi"]}
])

db.rank2.insert([
	{"group": "WE", "rank": 7},
	{"group": "IG", "rank": 1},
	{"group": "EDG", "rank": 2},
	{"group": "RNG", "rank": 3}
])

league_cursor = db.team.aggregate([
	{"$lookup": {"from": "rank2", "localField": "group", "foreignField": "group", "as": "rank"}}
])

for ele in league_cursor:
	pprint(ele)
