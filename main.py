
import uuid

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://iteso:iteso@peliculas.874ntci.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    database_names = client.list_database_names()
    print("List of databases:", database_names)
except Exception as e:
    print(e)



class Movie():
    '''class for movies'''
    def __init__(self,title:str, price: int, description: str, picture:str) -> None:
        '''initializes a movie'''
        self.title:str = title
        self.price:int = price
        self.description:str = description
        self.rentals:int = 0
        self.picture:str = picture #url
    def __str__(self) -> str:
        return f'\n{self.title}\n{self.price}\n{self.rentals}\n'
    
    @staticmethod
    def get_movies():
        '''method to retrieve movies from mongo db'''
        db = client.test 
        collection = db.movies

        for document in collection.find():
            print(document)
    
class User():
    '''class for a user'''
    def __init__(self, username:str, password:str, email:str) -> None:
        self.username:str = username
        self.userID:str = uuid.uuid4()
        self.password:str = password
        self.email:str = email
        self.accounts:[Account] = []

    def add_account(self,name:str,balance:int):
        '''adds and links an account to a user'''
        a = Account(name, balance)
        self.accounts.append(a)
    
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
            movie.rentals += 1
            self.rented_movies.append(movie)
        


u = User("david",'iteso', 'dtks')

a = u.add_account('netflix', 5)

m = Movie("toy story",3,'movie about toy story', 'google.com')

m.get_movies()

u.accounts[0].rent_movie(m)

