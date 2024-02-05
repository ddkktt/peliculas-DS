
import uuid

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://iteso:iteso@peliculas.874ntci.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

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
        return f'\n{self.title}\n{self.price}\n{self.rentals}\n'
    
    def movie_rented(self):
        '''method that increases counter'''
        self.rentals += 1
        
    @staticmethod
    def get_movies():
        '''method to retrieve movies from mongo db'''
        db = client.test 
        collection = db.movies
        for document in collection.find():
            print(document)

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
        '''adds and links an account to a user'''
        a = Account(name, balance)
        self.accounts.append(a)

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

m.get_movies()

admin = Admin()

admin.check_earnings()

u.accounts[0].rent_movie(m)

