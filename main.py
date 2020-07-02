import jinja2
import webapp2
import os
import json
import urllib
import urllib2
import logging
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import users
# from dictionary import GallonsWater

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__)))


class Visitor(ndb.Model):
    name =  ndb.StringProperty(required=True)
    email =  ndb.StringProperty(required=True)
    id =  ndb.StringProperty(required=True)
    # Images can only be stored as "BlobProperty"
    image = ndb.BlobProperty()

class UserSearch(ndb.Model):
    term = ndb.StringProperty(required=True)
    count = ndb.IntegerProperty(required=True)

class Location(object):
    name = ""
    Lng = 0
    Lat = 0

    def __init__(self, name, Lng, Lat):
        self.name = name
        self.Lng = Lng
        self.Lat = Lat


def make_location(name, Lng, Lat):
    location = Location(name, Lng, Lat)
    location.name = name
    location.Lng = Lng
    location.Lat = Lat
    print(location.name)
    print(location.Lng)
    print(location.Lat)
    return location



class MainPage(webapp2.RequestHandler):
    def get(self):
        make_location("Brussels", 100, 20)
        search_term = self.request.get('search') #what is being searched
        if search_term: #if search_term does exist
            lterm = search_term.lower()
            # CREATE A KEY
            key = ndb.Key('UserSearch', lterm) #the key functions is activated looking for
            # READ DATABASE
            search = key.get()
            if not search:
                #CREATE IF NOT THERE
                search = UserSearch(
                    key =key, count =0,
                    term = search_term)
            # UPDATE ACCOUNT
                # if there's nothing in the array, it creates a new user and sets the page count to 1
        else: #if search_term doesnt exist
            search_term = "Seattle"




class UserData(ndb.Model):
    id = ndb.StringProperty(required=False)
    fullname = ndb.StringProperty(required=False)
    givenname = ndb.StringProperty(required=False)
    imageurl = ndb.StringProperty(required=False)
    email = ndb.StringProperty(required=False)

class UserFood(ndb.Model):
    email = ndb.StringProperty(required=False)
    food = ndb.StringProperty(required=False)
    place = ndb.StringProperty(required=False)
    calories = ndb.IntegerProperty(required=False)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    userid = ndb.StringProperty(required=False)

class MainPage(webapp2.RequestHandler):
    def get(self):
        loginTemplate = jinja_environment.get_template('index.html')
        self.response.write(loginTemplate.render())

class LoginPage(webapp2.RequestHandler):
    def get(self):
        signinTemplate = jinja_environment.get_template('old templates/Login.html')
        self.response.write(signinTemplate.render())

class UserPage(webapp2.RequestHandler):
    def get(self):
        database = UserFood.query().order()
        print("HELLO LOOK AT THIS")
        print( database)
        food = database.order(-UserFood.created_at).fetch(limit=10)
        total=0
        for i in food:
            if i.calories == None:
                i.calories=0
            total= i.calories + total
        dict = {
            "string" : food,
            "total": total,
            }
        userTemplate = jinja_environment.get_template('html5up-big-picture/user.html')
        self.response.write(userTemplate.render(dict))

    def post(self):
        user_email = self.request.get('email')
        user_food = self.request.get('food')
        user_place = self.request.get('place')
        user_calories = self.request.get('calories')
        user_input = UserFood(food = user_food, place = user_place, calories= int(user_calories), email = user_email)
        user_input.put()
        self.redirect('/user')



class  DataEndpoint(webapp2.RequestHandler):
    def post(self):
        print("post")
        requestObject = json.loads(self.request.body)
        userdata = requestObject.get('data')
        # myuser = user_key
        myuser= UserData()
        print(list(userdata.keys()))
        myuser.id = userdata.get('id')
        myuser.fullname = userdata.get('fullname')
        myuser.givenname = userdata.get('givenname')
        myuser.imageurl = userdata.get('imageurl')
        myuser.email = userdata.get('email')
        myuser.put()



class QueryHandler(webapp2.RequestHandler):
    def get(self):
        query1 = UserFood.query()
        food = query1.fetch()
        print food
        dict = {
            "string" : food
            }
        template = jinja_environment.get_template('Templates/maps2.html')
        self.response.write(template.render(dict))

        # template = jinja_environment.get_template('Templates/maps2.html')
        # self.response.write(template.render(variables))

class Water(webapp2.RequestHandler):
    def get(self):
        inputTemplate = jinja_environment.get_template('html5up-big-picture/user.html')
        self.response.write(inputTemplate.render())

    def post(self):
        meattemplate = jinja_environment.get_template('html5up-big-picture/meat.html')
        liquidtemplate = jinja_environment.get_template('html5up-big-picture/liquids.html')
        othertemplate = jinja_environment.get_template('html5up-big-picture/other.html')
        veggietemplate = jinja_environment.get_template('html5up-big-picture/vegetables.html')
        user_input = self.request.get('user_food_category')
        results = {
            "type": user_input
            }
        if user_input == "meats":
            self.response.write(meattemplate.render())
            self.redirect('/meat')
        elif user_input == "liquids":
            self.response.write(liquidtemplate.render())
            self.redirect('/liquid')
        elif user_input == "other":
            self.response.write(othertemplate.render())
            self.redirect('/other')
        elif user_input == "vegetables":
            self.response.write(veggietemplate.render())
            self.redirect('/veggies')

class Wateroz(webapp2.RequestHandler):
    def get(self):
        lTemplate = jinja_environment.get_template('html5up-big-picture/liquids.html')
        self.response.write(lTemplate.render())
    def post(self):
        template = jinja_environment.get_template('html5up-big-picture/info.html')
        user_drink = self.request.get('user_drinktype')
        user_amount = self.request.get('amount')
        user_amount = float(user_amount)
        amount = (user_amount/128.0)
        if user_drink == "tea":
            amount1 = float(amount*1026.0)
            amount2 = float(amount*296.0)
            amount3 = float(amount*872)
            amount = float(amount*108.0)
            user1 = "Coffee"
            user2 = "Beer"
            user3 = "Wine"
        if user_drink == "coffee":
            amount1 = float(amount*108.0)
            amount2 = float(amount*296.0)
            amount3 = float(amount*872)
            amount = float(amount*1026.0)
            user1 = "Tea"
            user2 = "Beer"
            user3 = "Wine"
        if user_drink == "beer":
            amount1 = float(amount*108.0)
            amount2 = float(amount*1026.0)
            amount3 = float(amount*872.0)
            amount = float(amount*296.0)
            user1 = "Tea"
            user2 = "Coffee"
            user3 = "Wine"
        if user_drink == "wine":
            amount1 = float(amount*108.0)
            amount2 = float(amount*1026.0)
            amount3 = float(amount*296.0)
            amount = float(amount*872.0)
            user1 = "Tea"
            user2 = "Coffee"
            user3 = "Beer"
        results = {
            "drink": user_drink,
            "amount": user_amount,
            "ounces": amount,
            "ounce1": amount1,
            "ounce2": amount2,
            "ounce3": amount3,
            "drink1": user1,
            "drink2": user2,
            "drink3": user3,
            }
        self.response.write(template.render(results))

class WaterMeat(webapp2.RequestHandler):
    def get(self):
        lTemplate = jinja_environment.get_template('html5up-big-picture/meat.html')
        self.response.write(lTemplate.render())
    def post(self):
        template = jinja_environment.get_template('html5up-big-picture/infomeat.html')
        user_drink = self.request.get('user_drinktype')
        user_amount = self.request.get('amount')
        user_amount = float(user_amount)
        amount = user_amount
        if user_drink == "chicken":
            amount1 = float(amount*1847.0)
            amount2 = float(amount*718.0)
            amount3 = float(amount*302.0)
            amount = float(amount*518.0)
            user1 = "Beef"
            user2 = "Pork"
            user3 = "Tofu"
        elif user_drink == "beef":
            amount1 = float(amount*518.0)
            amount2 = float(amount*718.0)
            amount3 = float(amount*302.0)
            amount = float(amount*1847.0)
            user1 = "Chicken"
            user2 = "Pork"
            user3 = "Tofu"
        elif user_drink == "pork":
            amount1 = float(amount*518.0)
            amount2 = float(amount*1847.0)
            amount3 = float(amount*302.0)
            amount = float(amount*718.0)
            user1 = "Chicken"
            user2 = "Beef"
            user3 = "Tofu"
        else:
            amount1 = float(amount*518.0)
            amount2 = float(amount*1847.0)
            amount3 = float(amount*718.0)
            amount = float(amount*302.0)
            user1 = "Chicken"
            user2 = "Beef"
            user3 = "Pork"
        results = {
            "drink": user_drink,
            "amount": user_amount,
            "ounces": amount,
            "ounce1": amount1,
            "ounce2": amount2,
            "ounce3": amount3,
            "drink1": user1,
            "drink2": user2,
            "drink3": user3,
            }
        self.response.write(template.render(results))

class WaterVeggies(webapp2.RequestHandler):
    def get(self):
        lTemplate = jinja_environment.get_template('html5up-big-picture/vegetables.html')
        self.response.write(lTemplate.render())
    def post(self):
        template = jinja_environment.get_template('html5up-big-picture/infoveggies.html')
        user_drink = self.request.get('user_vegetable')
        user_amount = self.request.get('amount')
        user_amount = float(user_amount)
        amount = user_amount
        if user_drink == "corn":
            amount1 = float(amount*141.0)
            amount2 = float(amount*26.0)
            amount3 = float(amount*43.0)
            amount4 = float(amount*98.0)
            amount5 = float(amount*42.0)
            amount6 = float(amount*28.0)
            amount = float(amount*146.0)
            user1 = "Avocado"
            user2 = "Tomato"
            user3 = "Eggplant"
            user4 = "Artichokes"
            user5 = "Cucumbers"
            user6 = "Lettuce"
        elif user_drink == "avocado":
            amount1 = float(amount*146.0)
            amount2 = float(amount*26.0)
            amount3 = float(amount*43.0)
            amount4 = float(amount*98.0)
            amount5 = float(amount*42.0)
            amount6 = float(amount*28.0)
            amount = float(amount*141.0)
            user1 = "Corn"
            user2 = "Tomato"
            user3 = "Eggplant"
            user4 = "Artichokes"
            user5 = "Cucumbers"
            user6 = "Lettuce"
        elif user_drink == "tomato":
            amount1 = float(amount*146.0)
            amount2 = float(amount*141.0)
            amount3 = float(amount*43.0)
            amount4 = float(amount*98.0)
            amount5 = float(amount*42.0)
            amount6 = float(amount*28.0)
            amount = float(amount*26.0)
            user1 = "Corn"
            user2 = "Avocado"
            user3 = "Eggplant"
            user4 = "Artichokes"
            user5 = "Cucumbers"
            user6 = "Lettuce"
        elif user_drink == "eggplant":
            amount1 = float(amount*146.0)
            amount2 = float(amount*141.0)
            amount3 = float(amount*26.0)
            amount4 = float(amount*98.0)
            amount5 = float(amount*42.0)
            amount6 = float(amount*28.0)
            amount = float(amount*43.0)
            user1 = "Corn"
            user2 = "Avocado"
            user3 = "Tomato"
            user4 = "Artichokes"
            user5 = "Cucumbers"
            user6 = "Lettuce"
        elif user_drink == "artichokes":
            amount1 = float(amount*146.0)
            amount2 = float(amount*141.0)
            amount3 = float(amount*26.0)
            amount4 = float(amount*43.0)
            amount5 = float(amount*42.0)
            amount6 = float(amount*28.0)
            amount = float(amount*98.0)
            user1 = "Corn"
            user2 = "Avocado"
            user3 = "Tomato"
            user4 = "Eggplant"
            user5 = "Cucumbers"
            user6 = "Lettuce"
        elif user_drink == "cucumbers":
            amount1 = float(amount*146.0)
            amount2 = float(amount*141.0)
            amount3 = float(amount*26.0)
            amount4 = float(amount*43.0)
            amount5 = float(amount*98.0)
            amount6 = float(amount*28.0)
            amount = float(amount*42.0)
            user1 = "Corn"
            user2 = "Avocado"
            user3 = "Tomato"
            user4 = "Eggplant"
            user5 = "Artichokes"
            user6 = "Lettuce"
        # else user_drink == "lettuce":
        else:
            amount1 = float(amount*146.0)
            amount2 = float(amount*141.0)
            amount3 = float(amount*26.0)
            amount4 = float(amount*43.0)
            amount5 = float(amount*98.0)
            amount6 = float(amount*42.0)
            amount = float(amount*28.0)
            user1 = "Corn"
            user2 = "Avocado"
            user3 = "Tomato"
            user4 = "Eggplant"
            user5 = "Artichokes"
            user6 = "Cucumbers"
        results = {
            "drink": user_drink,
            "amount": user_amount,
            "ounces": amount,
            "ounce1": amount1,
            "ounce2": amount2,
            "ounce3": amount3,
            "ounce4": amount4,
            "ounce5": amount5,
            "ounce6": amount6,
            "drink1": user1,
            "drink2": user2,
            "drink3": user3,
            "drink4": user4,
            "drink5": user5,
            "drink6": user6,
            }
        self.response.write(template.render(results))

class WaterOther(webapp2.RequestHandler):
    def get(self):
        lTemplate = jinja_environment.get_template('html5up-big-picture/other.html')
        self.response.write(lTemplate.render())
    def post(self):
        template = jinja_environment.get_template('html5up-big-picture/infoother.html')
        user_drink = self.request.get('user_othertype')
        user_amount = self.request.get('amount')
        user_amount = float(user_amount)
        amount = user_amount
        if user_drink == "soybeans":
            amount1 = float(amount*222.0)
            amount2 = float(amount*299.0)
            amount3 = float(amount*193.0)
            amount4 = float(amount*34.0)
            amount5 = float(amount*290.0)
            amount6 = float(amount*35.0)
            amount7 = float(amount*1860.0)
            amount8 = float(amount*199.0)
            amount = float(amount*257.0)
            user1 = "Pasta"
            user2 = "Rice"
            user3 = "Bread"
            user4 = "Potatoes"
            user5 = "Oats"
            user6 = "Peppermint"
            user7 = "Cinnamon"
            user8 = "Ginger"
            user_drink == "soybeans"
        elif user_drink == "Pasta":
            amount1 = float(amount*257.0)
            amount2 = float(amount*299.0)
            amount3 = float(amount*193.0)
            amount4 = float(amount*34.0)
            amount5 = float(amount*290.0)
            amount6 = float(amount*35.0)
            amount7 = float(amount*1860.0)
            amount8 = float(amount*199.0)
            amount = float(amount*222.0)
            user1 = "Soybeans"
            user2 = "Rice"
            user3 = "Bread"
            user4 = "Potatoes"
            user5 = "Oats"
            user6 = "Peppermint"
            user7 = "Cinnamon"
            user8 = "Ginger"
            user_drink == "Pasta"
        elif user_drink == "rice":
            amount1 = float(amount*257.0)
            amount2 = float(amount*222.0)
            amount3 = float(amount*193.0)
            amount4 = float(amount*34.0)
            amount5 = float(amount*290.0)
            amount6 = float(amount*35.0)
            amount7 = float(amount*1860.0)
            amount8 = float(amount*199.0)
            amount = float(amount*299.0)
            user1 = "Soybeans"
            user2 = "Pasta"
            user3 = "Bread"
            user4 = "Potatoes"
            user5 = "Oats"
            user6 = "Peppermint"
            user7 = "Cinnamon"
            user8 = "Ginger"
            user_drink == "Rice"
        elif user_drink == "bread":
            amount1 = float(amount*257.0)
            amount2 = float(amount*222.0)
            amount3 = float(amount*299.0)
            amount4 = float(amount*34.0)
            amount5 = float(amount*290.0)
            amount6 = float(amount*35.0)
            amount7 = float(amount*1860.0)
            amount8 = float(amount*199.0)
            amount = float(amount*193.0)
            user1 = "Soybeans"
            user2 = "Pasta"
            user3 = "Rice"
            user4 = "Potatoes"
            user5 = "Oats"
            user6 = "Peppermint"
            user7 = "Cinnamon"
            user8 = "Ginger"
            user_drink == "Bread"
        elif user_drink == "potatoes":
            amount1 = float(amount*257.0)
            amount2 = float(amount*222.0)
            amount3 = float(amount*299.0)
            amount4 = float(amount*193.0)
            amount5 = float(amount*290.0)
            amount6 = float(amount*35.0)
            amount7 = float(amount*1860.0)
            amount8 = float(amount*199.0)
            amount = float(amount*34.0)
            user1 = "Soybeans"
            user2 = "Pasta"
            user3 = "Rice"
            user4 = "Bread"
            user5 = "Oats"
            user6 = "Peppermint"
            user7 = "Cinnamon"
            user8 = "Ginger"
            user_drink == "Potatoes"
        elif user_drink == "oats":
            amount1 = float(amount*257.0)
            amount2 = float(amount*222.0)
            amount3 = float(amount*299.0)
            amount4 = float(amount*193.0)
            amount5 = float(amount*34.0)
            amount6 = float(amount*35.0)
            amount7 = float(amount*1860.0)
            amount8 = float(amount*199.0)
            amount = float(amount*290.0)
            user1 = "Soybeans"
            user2 = "Pasta"
            user3 = "Rice"
            user4 = "Bread"
            user5 = "Potatoes"
            user6 = "Peppermint"
            user7 = "Cinnamon"
            user8 = "Ginger"
            user_drink == "Oats"
        elif user_drink == "peppermint":
            amount1 = float(amount*257.0)
            amount2 = float(amount*222.0)
            amount3 = float(amount*299.0)
            amount4 = float(amount*193.0)
            amount5 = float(amount*34.0)
            amount6 = float(amount*290.0)
            amount7 = float(amount*1860.0)
            amount8 = float(amount*199.0)
            amount = float(amount*35.0)
            user1 = "Soybeans"
            user2 = "Pasta"
            user3 = "Rice"
            user4 = "Bread"
            user5 = "Potatoes"
            user6 = "Oats"
            user7 = "Cinnamon"
            user8 = "Ginger"
            user_drink == "Peppermint"
        elif user_drink == "cinnamon":
            amount1 = float(amount*257.0)
            amount2 = float(amount*222.0)
            amount3 = float(amount*299.0)
            amount4 = float(amount*193.0)
            amount5 = float(amount*34.0)
            amount6 = float(amount*290.0)
            amount7 = float(amount*35.0)
            amount8 = float(amount*199.0)
            amount = float(amount*1860.0)
            user1 = "Soybeans"
            user2 = "Pasta"
            user3 = "Rice"
            user4 = "Bread"
            user5 = "Potatoes"
            user6 = "Oats"
            user7 = "Peppermint"
            user8 = "Ginger"
            user_drink == "Cinnamon"
        else:
            amount1 = float(amount*257.0)
            amount2 = float(amount*222.0)
            amount3 = float(amount*299.0)
            amount4 = float(amount*193.0)
            amount5 = float(amount*34.0)
            amount6 = float(amount*290.0)
            amount7 = float(amount*35.0)
            amount8 = float(amount*1860.0)
            amount = float(amount*199.0)
            user1 = "Soybeans"
            user2 = "Pasta"
            user3 = "Rice"
            user4 = "Bread"
            user5 = "Potatoes"
            user6 = "Oats"
            user7 = "Peppermint"
            user8 = "Cinnamon"
            user_drink == "Ginger"

        results = {
            "drink": user_drink,
            "amount": user_amount,
            "ounces": amount,
            "ounce1": amount1,
            "ounce2": amount2,
            "ounce3": amount3,
            "ounce4": amount4,
            "ounce5": amount5,
            "ounce6": amount6,
            "drink1": user1,
            "drink2": user2,
            "drink3": user3,
            "drink4": user4,
            "drink5": user5,
            "drink6": user6,
            }
        self.response.write(template.render(results))

app = webapp2.WSGIApplication([
      ('/', MainPage),
      ('/login', LoginPage),
      ('/user', UserPage),
      ('/data', DataEndpoint),
      ('/query',QueryHandler),
      ('/water', Water ),
      ('/liquid', Wateroz),
      ('/meat', WaterMeat),
      ('/veggies', WaterVeggies),
      ('/other', WaterOther)
])
