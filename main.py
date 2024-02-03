import uuid


class Account():
    '''class for account'''
    def __init__(self, name:str, balance:int) -> None:
        self.name = name
        self.balance = balance
        self.rented_movies = []
    def __str__(self) -> str:
        return f'name: {self.name}, balance {self.balance}, movies {self.rented_movies}'
    def rent_movies():
        pass
    


class User():
    '''class for a user'''
    def __init__(self,username:str, password:str, email:str) -> None:
        self.username:str = username
        self.userID:str = uuid.uuid4()
        self.password:str = password
        self.email:str = email
        self.accounts:[Account] = []
    def add_account(self,name:str,balance:int):
        a = Account(name, balance)
        self.accounts.append(a)
    
        




class Movie():
    '''class for movies'''



u = User("david",'iteso', 'dtks')

u.add_account('netflix', 5)

print(u.accounts[0])
