import uuid
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://vergarapablo2001:swlWGNpLvejBiM3i@cluster0.s2d4dwo.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.POPCine 
collection = db.Movies

class Movie():
    '''class for movies'''
    def __init__(self, name:str, price: int, description: str, image:str, rentals:int= 0, category:str= None) -> None:
        '''initializes a movie'''
        self.name:str = name
        self.price:int = price
        self.description:str = description
        self.rentals:int = 0
        self.image:str = image #url
        self.rentals:int = rentals
        self.category:str = category

    def __str__(self) -> str:
        '''method to display info aobut movie'''
        return f'\ntitle: {self.name}\nprice: {self.price}\nrentals: {self.rentals}\n'
    
    def movie_rented(self, movie_id):
        '''method that increases counter'''
        self.rentals += 1
        rentals = {'rentals': self.rentals}
        self.update_movie(movie_id, rentals)

    @staticmethod
    def get_movies():
        '''method to retrieve movies from mongo db'''
        movies = []
        try:
            for document in collection.find():
                movies.append(document)
            return movies
        except:
            return 'An error ocurred while retrieving movies'
        
    @staticmethod
    def get_movie_by_id(movie_id:str):
        '''method to retrieve movie given an id as a string, returns the movie as a movie object'''
        try:
            movie_id = ObjectId(movie_id)
        except:
            return None  

        query = { '_id' : movie_id }
        movie_data = collection.find_one(query)

        if movie_data:
            return movie_data
        else:
            return 'Movie not found'
        
    @staticmethod
    def update_movie(movie_id, update_data):
        '''Updates movie on db'''
        try:
            movie_id = ObjectId(movie_id)
        except:
            return False 
        
        query = { '_id' : movie_id }
        data_to_update = {}
        for key, value in update_data.__dict__.items():
            data_to_update['$set'] = data_to_update.get('$set', {})
            data_to_update['$set'][key] = value

        try:
            collection.update_one(query, data_to_update)
            return 'Movie updated successfully'
        except:
            return 'An error occured while updating the movie'

    @staticmethod
    def create_movie(movie_instance):
        '''Creates a movie on db'''
        movie_data = {
            'name': movie_instance.name,
            'price': movie_instance.price,
            'description': movie_instance.description,
            'image': movie_instance.image,
            'rentals': movie_instance.rentals,
            'category': movie_instance.category,
        }

        try:
            collection.insert_one(movie_data)
            return 'Movie created successfully'
        except:
            return 'An error occured while creating the movie'
        
    @staticmethod
    def delete_movie(movie_id):
        '''Deletes movie from db'''
        try:
            movie_id = ObjectId(movie_id)
        except:
            return False 
        
        query = { '_id' : movie_id }

        try:
            collection.find_one_and_delete(query)
            return 'Movie deleted successfully'
        except: 
            return 'An error occured while deleting the movie'
        
        
class User():
    '''class for a user'''
    def __init__(self, username:str, password:str, email:str) -> None:
        self.username:str = username
        self.userID:str = uuid.uuid4()
        self.password:str = password
        self.email:str = email
        self.accounts:[Account] = []
        self.rented_movies:[Movie] = []
 
    def add_account(self,name:str,balance:int):
        '''adds and links an account to a user and returns the new account'''
        a = Account(name, balance)
        self.accounts.append(a)
        return a

    def get_accounts(self):
        '''returns a users accounts'''
        return self.accounts
    
    def rent_movie(self, movie:Movie):
        '''Adds the movie to the rented list '''
        self.rented_movies.append(movie)

    def delete_user(self):
        '''Deletes an account'''
        self.userID = ""
        return 'Acount deleted'
    
class Account():
    '''class for account'''
    def __init__(self, name:str, balance:int = 0) -> None:
        '''initializes an account'''
        self.name:str = name
        self.balance:int = balance
        self.rented_movies:[Movie] = []

    def __str__(self) -> str:
        '''print out a users name, balance and rented movies'''
        return f'name: {self.name}, balance {self.balance}, movies {self.rented_movies}'
    
    def rent_movie(self, movie:Movie, user:User):
        '''method to rent a movie'''
        if(self.balance>movie.price):
            self.balance -= movie.price
            movie.movie_rented()
            self.rented_movies.append(movie)
            user.rent_movie(movie)
    
    def increase_balance(self, amount:int):
        '''method to modify balance by providing amount'''
        self.balance += amount
        
    def get_balance(self):
        '''returns the balance of an account'''
        return self.balance
        
class Admin(Account):
    '''class that can check analytics of movies'''
    def __init__(self, name:str, admin_name:str) -> None:
        super().__init__(name)
        self.admin_name = admin_name

    def check_earnings(self):
        total_earnings = 0
        '''method to retrieve movies from mongo db'''
        try:
            for document in collection.find():
                rentals = document.get('rentals')
                price = document.get('price')
                if(rentals):
                    total_earnings = total_earnings + (rentals * price)

            return total_earnings   
        except: 
            return 'An error ocurred'

#user = User("david",'iteso', 'dtks')
#account = user.add_account('netflix', 5)

admin = Admin('david', 'cosa')
print(admin.check_earnings())

#admin.check_earnings()

#u.accounts[0].rent_movie(m)
    

'''How to test movie'''
#movie = Movie("toy story", 3,'movie about toy story', 'google.com')
#movie2 = Movie('wawawa', 0, 'a', 'a')

#Movie.create_movie(movie)
#Movie.update_movie('65c2c5bac96b37c065e2bdaf', movie2)
#print(Movie.delete_movie('65c2c0550e4f4c49174bc104'))
#print(Movie.get_movies()) # len(Movie.get_movies())
#print(Movie.get_movie_by_id('65c0216ac064f945b2ba9c90'))