
import uuid
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://iteso:iteso@peliculas.874ntci.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.test 
collection = db.movies

class Movie():
    '''class for movies'''
    def __init__(self,title:str, price: int, description: str, picture:str, category:str= None) -> None:
        '''initializes a movie'''
        self.title:str = title
        self.price:int = price
        self.description:str = description
        self.rentals:int = 0
        self.picture:str = picture #url
        self.category:str = category
    def __str__(self) -> str:
        '''method to display info aobut movie'''
        return f'\ntitle: {self.title}\nprice: {self.price}\nrentals: {self.rentals}\n'
    
    def movie_rented(self, movie_id):
        '''method that increases counter'''
        self.rentals += 1
        rentals = {'rentals': self.rentals}
        self.update_movie(movie_id, rentals)

    @staticmethod
    def get_movies():
        '''method to retrieve movies from mongo db'''
        for document in collection.find():
            print(document)
    @staticmethod
    def get_movie_by_id(movie_id:str):
        '''method to retrieve movie given an id as a string, returns the movie as a movie object'''
        try:
            movie_id = ObjectId(movie_id)
        except:
            return None  

        query = {"_id": movie_id}
        movie_data = collection.find_one(query)

        if movie_data:
            movie = Movie(
                title=movie_data.get("title"),
                description=movie_data.get("description"),
                picture=movie_data.get("picture"),
                price=movie_data.get("price"),
                #rented=movie_data.get("rented"),
            )
            return movie
        else:
            return None
        
    @staticmethod
    def update_movie(movie_id, update_data):
        try:
            movie_id = ObjectId(movie_id)
        except:
            return False 

        result = collection.update_one({"_id": movie_id}, {"$set": update_data})

        if result.modified_count > 0:
            return True  
        else:
            return False


class Admin():
    '''class that can check analytics of movies'''
    def __init__(self) -> None:
        pass
    
    def check_earnings(self):
        total_earnings = 0
        '''method to retrieve movies from mongo db'''
        db = client.test 
        collection = db.movies
        for document in collection.find():
            rentals = document.get('rentals')
            price = document.get('price')
            if(rentals):
                total_earnings = total_earnings + (rentals * price)

        return total_earnings



class User():
    '''class for a user'''
    def __init__(self, username:str, password:str, email:str) -> None:
        self.username:str = username
        self.userID:str = uuid.uuid4()
        self.password:str = password
        self.email:str = email
        self.accounts:[Account] = []

    def add_account(self,name:str,balance:int):
        '''adds and links an account to a user and returns the new account'''
        a = Account(name, balance)
        self.accounts.append(a)
        return a

    def get_accounts(self):
        '''returns a users accounts'''
        return self.accounts
    
    
class Account(User):
    '''class for account'''
    def __init__(self, name:str, balance:int) -> None:
        '''initializes an account'''
        self.name:str = name
        self.balance:int = balance
        self.rented_movies:[Movie] = []

    def __str__(self) -> str:
        '''print out a users name, balance and rented movies'''
        return f'name: {self.name}, balance {self.balance}, movies {self.rented_movies}'
    
    def rent_movie(self, movie:Movie):
        '''method to rent a movie'''
        if(self.balance>movie.price):
            self.balance -= movie.price
            movie.movie_rented()
            self.rented_movies.append(movie)
    
    def increase_balance(self, amount:int):
        '''method to modify balance by providing amount'''
        self.balance += amount
    def get_balance(self):
        '''returns the balance of an account'''
        return self.balance
        


u = User("david",'iteso', 'dtks')

a = u.add_account('netflix', 5)

m = Movie("toy story",3,'movie about toy story', 'google.com')

print(m)

m.get_movies()

print(m.get_movie_by_id('65bd950e95570faf8b423a17'))

admin = Admin()

admin.check_earnings()

u.accounts[0].rent_movie(m)

