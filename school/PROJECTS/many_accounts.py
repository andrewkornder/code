from amazon_account import AmazonAccount, AmazonItem
from random import choice, sample, randint
from string import *

def gen_password():
    return ''.join(sample(ascii_letters, 6)) + choice(ascii_uppercase) + choice(punctuation)

fn = open('first_names.txt').read().split('\n')
ln = open('last_names.txt').read().split('\n')

accounts = [AmazonAccount(f'{choice(fn)} {choice(ln)}', f'email{i}@emailservice.com', 
                          gen_password(), randint(0, 1000)) for i in range(100)]

choice(accounts).show_info()