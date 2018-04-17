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

# 4. find number of movies made in China
china_movies = db.movie_collection.aggregate([
        {"$match": {"countries": ["China"], "rated": "Pending rating"}},
        {"$group": {"_id": {"countries": ["China"], "rated": "Pending rating"}, "count": {"$sum": 1}}}
])

# 5. test lookup and return at least two results

