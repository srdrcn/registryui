import cgi
import json

import flask
import requests
from flask import (Flask, jsonify, redirect, render_template, request, session, url_for,abort)
from flask_api import FlaskAPI
from requests.auth import HTTPBasicAuth
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import HTTPException


app = Flask(__name__, template_folder='Templates') 
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
        kwargs = {          
        
       
        
        'url':url
        
        }
           
        response = requests.get(url+'/v2/_catalog',
    auth=HTTPBasicAuth(username,password),verify=False)
        j = response.json()

    
        return render_template('home.html',images=j['repositories'],frontend_url=url)
        
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
      





if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)
        
  




