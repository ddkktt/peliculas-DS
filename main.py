import uuid


class Movie():
    '''class for movies'''
    def __init__(self,title:str, price: int, description: str) -> None:
        '''initializes a movie'''
        self.title:str = title
        self.price:int = price
        self.description:str = description
        self.rentals:int = 0
    



    


class User():
    '''class for a user'''
    def __init__(self, username:str, password:str, email:str) -> None:
        self.username:str = username
        self.userID:str = uuid.uuid4()
        self.password:str = password
        self.email:str = email
        self.accounts:[Account] = []

    def add_account(self,name:str,balance:int) -> None:
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
    
    def rent_movies(self, movie:Movie):
        '''method to rent a movie'''
        if(self.balance>movie.price):
            self.balance -= movie.price
            movie.rentals += 1
            self.rented_movies.append(movie)
        




class Movie():
    '''class for movies'''



u = User("david",'iteso', 'dtks')

u.add_account('netflix', 5)

print(u.accounts[0])
