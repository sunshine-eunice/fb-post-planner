import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
import jinja2
import webapp2
import logging
from google.appengine.api import urlfetch
import json
from datetime import datetime,timedelta

import sched
import time
import threading





FACEBOOK_APP_ID = "693517617401481"
FACEBOOK_APP_SECRET = "04e6462015211d41135602f9d392ebce"
GRAPH_API_URL ="https://graph.facebook.com/v2.1"



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)

class Posts(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)
    message = ndb.StringProperty(required=True)
    date_to_post = ndb.DateTimeProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty(default="TBP")


def post_to_object(post):
    data = {
            "method": "post",
            "message": post.message,
            "access_token" : post.access_token
        }
    return data

def post_to_facebook(data,id):
    form_data = urllib.urlencode(data)
    url = GRAPH_API_URL+"/"+id+"/feed"
    result = urlfetch.fetch(url=url,payload=form_data,method=urlfetch.POST)
    content = json.loads(result.content)
    return content

def short_to_long_lived(access_token,self):
    url = "https://graph.facebook.com/oauth/access_token"
    data = {
        "grant_type" : "fb_exchange_token",
        "fb_exchange_token": access_token,
        "client_id" : FACEBOOK_APP_ID,
        "client_secret" : FACEBOOK_APP_SECRET,
        
    }
    form_data = urllib.urlencode(data)
    result = urlfetch.fetch(url=url,payload=form_data,method=urlfetch.POST)
    return result.content

def decode_response(str):
    access_token = str.split("&")[0].split("=")[1]
    return {
        "access_token" : access_token,
    }
def write_template(self,template,template_values=None):
    header = JINJA_ENVIRONMENT.get_template('templates/header.html')
    template = JINJA_ENVIRONMENT.get_template('templates/'+template)
    if template_values:
        self.response.write(header.render()+template.render(template_values))
    else:
        self.response.write(header.render()+template.render())
class MainHandler(webapp2.RequestHandler):
    def get(self):
        write_template(self,"main.html")
    def post(self):
        post = Posts()
        post.user_id = self.request.get("fbID")   
        post.message = self.request.get("message")
        post.date_to_post = datetime.strptime(self.request.get("date_to_post"),'%m/%d/%Y %I:%M %p')
        access_token = self.request.get("access_token")
        request = short_to_long_lived(access_token,self)
        request = decode_response(request)
        post.access_token = request["access_token"]
        post.put()
        self.response.write('<script>alert("Post has been Scheduled.");window.location.assign("/list/'+post.user_id+'")</script>')

class ListPostHandler(webapp2.RequestHandler):
    def get(self,id):
        to_be_post = ndb.gql("Select * from Posts "+
            "Where user_id = :1 and status = 'TBP' ",id).bind()
        posted = ndb.gql("Select * from Posts "+
            "Where user_id = :1 and status = 'Posted' ",id).bind()
        template_values={
            "posts":to_be_post,
            "posted": posted
        }
        write_template(self,"list.html",template_values)

class PostToFBHandler(webapp2.RequestHandler):
    def post(self):
        data = {
                    "method": "post",
                    "message": self.request.get("message"),
                    "access_token": self.request.get("access_token")
                };
        post = Posts()
        post.message = self.request.get("message")
        post.access_token = self.request.get("access_token")
        post.user_id = self.request.get("fbID")
        post.date_to_post = datetime.now()+ timedelta(hours=8) 
        content = post_to_facebook(data,self.request.get("fbID"))
        if(content.get("id")):
           self.response.write('<script>alert("Message posted to facebook.");window.location.assign("/")</script>')
        elif content["error"]["error_user_title"]:
            self.response.write('<script>alert("'+content["error"]["error_user_title"]+'");window.location.assign("/")</script>')
        else:
            self.response.write('<script>alert("An error occured.");window.location.assign("/")</script>')

class EditPostHandler(webapp2.RequestHandler):
    def get(self,id):
        post = Posts.get_by_id(long(id))
        date = post.date_to_post.strftime("%m/%d/%Y %I:%M %p")
        template_values = {
            "post" : post,
            "date" : date
        }
        write_template(self,"edit.html",template_values)
    def post(self,id):
        post = Posts.get_by_id(long(id))
        post.message = self.request.get("message")
        post.date_to_post = datetime.strptime(self.request.get("date_to_post"),'%m/%d/%Y %I:%M %p')
        post.put()
        self.response.write("<script> alert('Edit Successful.');window.location.assign('/list/"+post.user_id+"')</script>")

class DeleteHandler(webapp2.RequestHandler):
    def get(self,id):
        post = Posts.get_by_id(long(id))
        post.key.delete()
        self.response.write("<script> alert('Edit Successful.');window.location.assign('/list/"+post.user_id+"')</script>")

class PostAllScheduledPosts(webapp2.RequestHandler):
    def get(self):
        p = Posts()
        p.date_to_post = datetime.now()
        posts = Posts.query(ndb.AND(Posts.date_to_post <= datetime.now()+timedelta(hours=8),
            Posts.status=="TBP")).fetch()
        for post in posts:
            data = post_to_object(post)
            post_to_facebook(data,post.user_id)
            post.status="Posted"
            post.put()
        

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/list/(.*)',ListPostHandler),
    ('/edit/(.*)',EditPostHandler),
    ('/delete/(.*)',DeleteHandler),
    ('/post-now',PostToFBHandler),
    ('/task/post',PostAllScheduledPosts)
], debug=True)