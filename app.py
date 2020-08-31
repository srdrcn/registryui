import cgi
import json

import flask
import requests
from flask import (Flask, jsonify, redirect, render_template, request, session, url_for,abort)
from flask_api import FlaskAPI
from requests.auth import HTTPBasicAuth
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import HTTPException


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key='s'
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/',methods = ['GET'])
def show_index():
      
        
        return render_template('index.html')

@app.route('/repositories', methods = ['POST'])
def get_data_from_html():
        
        url= request.form['url']
        username= request.form['username']
        password= request.form['password']
        frontend_url=url
        

        session["url"] = url
        session["username"] = username
        session["password"] = password
           
        response = requests.get(url+'/v2/_catalog',
    auth=HTTPBasicAuth(username,password),verify=False)
        j = response.json()

    
        return render_template('home.html',images=j['repositories'])
        
@app.route('/image/<path:image>')
def image(image):
        
        
        username = session.get("username")
        password = session.get("password")
        url=session.get("url")
        
        response1 = requests.get(url+'/v2/'+image+'/tags/list',auth=HTTPBasicAuth(username,password),
        verify=False)
        
      
        
        data=response1.json()
        
        kwargs = {          
        
        'image': image,
        'tags': data['tags'] if data['tags'] else [],
        'url':url
        
        }
        
        return render_template('image.html',**kwargs)     

@app.route('/image/<path:image>/tag/<tag>')
  
def taggest(image, tag):
    username = session.get("username")
    password = session.get("password")
    url=session.get("url")
    
    response1 = requests.get(url+'/v2/'+image+'/manifests/'+tag,auth=HTTPBasicAuth(username,password),
        verify=False,headers={'Accept':'application/vnd.docker.distribution.manifest.v2+json'})

    a = response1.headers['Docker-Content-Digest'] 
    j = response1.json()
    
    response2 = requests.delete(url+'/v2/'+image+'/manifests/'+ a,auth=HTTPBasicAuth(username,password),
        verify=False)
    
   
    
    print(a)
 
    kwargs = {
      #  'image': image,
       # 'tag': tag,
        #'layers': len(j[:200]),
        #'digest':a[0:200],
      #  'url':url
        
    }   
    return redirect('/image''/'+image)
    #return  render_template('image.html')
    #return render_template('tag.html', **kwargs)

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", e=e), 500
      






        
  
app.run()  




#url = "https://10.10.0.243:5000/v2"
#username = 'admin'
#password = 'PassworD123'

#session = requests.Session()
# these are sent along for all requests

# not strictly needed, but the documentation recommends it.
#session.headers['Accept'] = "application/json; charset=UTF-8"

# log in first, to get the tokens
#response = session.post(
#    url + '/_catalog',
#    json={'identifier': username, 'password': password},
#    headers={'VERSION': '2'},
#    verify=False
#)