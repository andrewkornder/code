#!/usr/bin/python
# amazon_account.py
__author__ = "Andrew Kornder"
__version__ = '1.0'


class AmazonAccount:
    def __init__(self, name: str, email_address: str, password: str, gift_balance=0):
        """
        constructor for the object
        
        :param name: a name for the account
        :param email_address: a valid email for the account
        :param gift_balance: an amount of money
        :return: None
        """
        
        self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})
        self.purchases = []
        
    def add_gift_amount(self, amount: float):
        """
        increase balance of account
        
        :param amount: a float representing money
        :return: None
        """        
        self.gift_balance += amount
        
    def change_email(self):
        """change the email connected to the account"""
        
        email = input('enter your email here: ')
        while input('confirm your email address: ') != email:
            print('wrong email. try again')
        self.email_address = email    
        
    def show_info(self):
        """prints attributes to console"""
        
        print(f'{self.name} / {self.email_address}\npassword: {self.password}:\nbalance: ${self.gift_balance}')
        print('purchases:\n' + '\n\t'.join(self.purchases))
    
    def purchase_item(self, item):
        """
        buys an item if there is enough money in the account
        
        :param item: an AmazonItem object
        :return: None
        """
        
        if item.price < self.gift_balance:
            self.purchases.append(item.name)
            self.gift_balance -= item.price
            item.categories.remove(item)


class AmazonItem:
    categories = {i: [] for i in ['fun', 'furniture', 'other']}
    
    def __init__(self, name: str, price: int, category: str = 'other'):
        """
        constructor for the object
        
        :param name: a name for the item
        :param price: price of the item
        :param category: a category describing the item
        :return: None
        """
        
        self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})
        self.categories[category].append(self.name)

    def raise_price(self, new_amount):
        """
        simple way to raise price of an item
        
        :param new_amount: a float or int to set the price to
        """
        
        self.price = new_amount
        
    def show_category(self, category):
        """
        shows all item names in a given category
        
        :param category: the name of a category to display items from
        :return: None
        """
        
        if category in self.categories:
            print('\n'.join(self.categories[category]))
            