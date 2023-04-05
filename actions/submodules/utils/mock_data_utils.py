# ----- Data Structure ----- #

import json

# ----- -------------- ----- #

json_restaurant_list = """
[
   {
      "id":"rid_1232JHKJ",
      "name":"Taco Bell",
      "image_url":"https://b.zmtcdn.com/data/pictures/1/18602861/bd2825ec26c21ebdc945edb7df3b0d99.jpg",
      "home_page_url":"https://www.tacobell.com/",
      "cuisine":"Mexican",
      "ratings":"4.5",
      "telephone":"(123) 456-7890",
      "menu_url":"https://www.tacobell.com/menu",
      "address":"123 Main Street, Anytown, USA",
      "opening_hours":{
         "Mon - Fri":"9:00 AM - 10:00 PM",
         "Sat, Sun":"10:00 AM - 11:00 PM"
      }
   },
   {
      "id":"rid_4567SJKL",
      "name":"Danke",
      "image_url":"https://lh3.googleusercontent.com/p/AF1QipOs5oyEh2eqR1wHmLuL7WPvdkiqPjyJJdHEeCyI=w600-h0",
      "home_page_url":"https://www.danke.com/",
      "cuisine":"Italian",
      "ratings":"4.5",
      "telephone":"(123) 456-7890",
      "menu_url":"https://www.tacobell.com/menu",
      "address":"123 Main Street, Any-town, USA",
      "opening_hours":{
         "Mon - Fri":"9:00 AM - 10:00 PM",
         "Sat, Sun":"10:00 AM - 11:00 PM"
      }
   },
   {
      "id":"rid_1234ABCD",
      "name":"Lụa Restaurant",
      "image_url":"https://www.collinsdictionary.com/images/full/restaurant_135621509.jpg",
      "home_page_url":"https://www.lua.com/",
      "ratings":"4.5",
      "cuisine":"Vietnamese",
      "telephone":"(123) 456-7890",
      "menu_url":"https://www.tacobell.com/menu",
      "address":"123 Main Street, Anytown, USA",
      "opening_hours":{
         "Mon - Fri":"9:00 AM - 10:00 PM",
         "Sat, Sun":"10:00 AM - 11:00 PM"
      }
   },
   {
      "id":"rid_4567HTKL",
      "name":"Thai King",
      "image_url":"https://upload.wikimedia.org/wikipedia/commons/6/62/Barbieri_-_ViaSophia25668.jpg",
      "home_page_url":"https://www.thaiking.com/",
      "ratings":"3.5",
      "cuisine":"Thai",
      "telephone":"(123) 456-7890",
      "menu_url":"https://www.tacobell.com/menu",
      "address":"123 Main Street, Anytown, USA",
      "opening_hours":{
         "Mon - Fri":"9:00 AM - 10:00 PM",
         "Sat, Sun":"10:00 AM - 11:00 PM"
      }
   },
   {
      "name":"Marubi Ramen",
      "image_url":"https://b.zmtcdn.com/data/pictures/4/18902194/e92e2a3d4b5c6e25fd4211d06b9a909e.jpg",
      "home_page_url":"https://www.marubiramen.com/",
      "id":"rid_1234JRJK",
      "ratings":"4.0",
      "cuisine":"Japanese",
      "telephone":"(123) 456-7890",
      "menu_url":"https://www.tacobell.com/menu",
      "address":"123 Main Street, Anytown, USA",
      "opening_hours":{
         "Mon - Fri":"9:00 AM - 10:00 PM",
         "Sat, Sun":"10:00 AM - 11:00 PM"
      }
   },
   {
      "name":"Gong Gan",
      "image_url":"https://b.zmtcdn.com/data/pictures/3/17871363/c53db6ba261c3e2d4db1afc47ec3eeb0.jpg",
      "home_page_url":"https://www.gonggan.com/",
      "id":"rid_4567HJKL",
      "ratings":"3.0",
      "cuisine":"Korean",
      "telephone":"(123) 456-7890",
      "menu_url":"https://www.tacobell.com/menu",
      "address":"123 Main Street, Anytown, USA",
      "opening_hours":{
         "Mon - Fri":"9:00 AM - 10:00 PM",
         "Sat, Sun":"10:00 AM - 11:00 PM"
      }
   }
]"""

rest_list = json.loads(json_restaurant_list)

users = [
    {"id": "uid_0", "name": "Alice", "email": "alice@gmail.com", "password": "1234"},
    {"id": "uid_1", "name": "Bob", "email": "bob@yahoo.com", "password": "5678"},
    {"id": "uid_2", "name": "Carol", "email": "carol@gmail.com", "password": "9876"},
    {"id": "uid_3", "name": "David", "email": "david@gmail.com", "password": "4321"},
    {"id": "uid_4", "name": "Eva", "email": "eva@gmail.com", "password": "2468"},
    {"id": "uid_5", "name": "Kalpa", "email": "kalpa@uom.com", "password": "1234"},
    {"id": "uid_6", "name": "Eva", "email": "eva@gmail.com", "password": "2468"}
]

# add these later
# phone: The phone number of the restaurant
# website: The website of the restaurant
# price_level: A rating of the restaurant's price level, with 1 being the cheapest and 4 being the most expensive

# [
#                 {
#                     "image_url": "https://b.zmtcdn.com/data/pictures/1/18602861/bd2825ec26c21ebdc945edb7df3b0d99.jpg",
#                     "name": "Taftoon Bar & Kitchen",
#                     "ratings": "4.5",
#                 },
#                 {
#                     "image_url": "https://b.zmtcdn.com/data/pictures/4/18357374/661d0edd484343c669da600a272e2256.jpg",
#
#                     "ratings": "4.0",
#                     "name": "Veranda"
#                 },
#                 {
#                     "image_url": "https://b.zmtcdn.com/data/pictures/4/18902194/e92e2a3d4b5c6e25fd4211d06b9a909e.jpg",
#
#                     "ratings": "4.0",
#                     "name": "145 The Mill"
#                 },
#                 {
#                     "image_url": "https://b.zmtcdn.com/data/pictures/3/17871363/c53db6ba261c3e2d4db1afc47ec3eeb0.jpg",
#
#                     "ratings": "4.0",
#                     "name": "The Fatty Bao"
#                 },
#             ]

# Python follows the PEP 8 Style Guide for Python Code, which recommends the following naming conventions for Python
# files:

# Module names should be short and lowercase. If the module name contains multiple words,
# separate them with underscores (e.g., my_module.py).
# Package names should also be short and lowercase, with no underscores (e.g., mypackage).
# Class names should be in CamelCase (capitalized words with no spaces between them). For example, MyClass.
# Function and variable names should be lowercase, with words separated by underscores (e.g., my_function, my_variable).
# Constants should be in all caps, with words separated by underscores (e.g., MY_CONSTANT).

# Note that these conventions are not enforced by the Python interpreter, but they are widely adopted by the Python
# community to improve readability and maintainability of code.
