import subprocess
import sys
import pandas as pd
import json 
import requests
import config
from config import *

class gistapi:
    def __init__(self):
        self.user = USERNAME
        self.token = API_TOKEN
        self.password = PASSWORD

    def auth(self):
        login = requests.get('https://api.github.com/search/repositories?q=github+api', auth=(self.user,self.token))
        self.headers = {'Authorization': 'token ' + self.token}
        print(login.json())
        print("login success")
        
    def listgist(self):
        file_name = []
        print("list gist")
        r = self.gist = requests.get('https://api.github.com/gists' , headers=self.headers)
        print(self.gist.json())
        r_text = json.loads(r.text)
        limit = len(r.json())
        if (r.status_code == 200 ):
            for g,no in zip(r_text, range(0,limit)):
                for key,value in r.json()[no]['files'].items():
                    file_name.append(value['filename'])
            print("200: gistall")
            print(file_name)
            return file_name
            

        raise Exception('Username not found')
    
    def list(self, offset):
        '''
        will display only the required no. of filenames but in order.
        Result can be stored in an array for easy fetching of gistNames
        for future purposes.
        eg. a = Gist().mygists().listall()
            print a[0] #to fetch first gistName
        '''
        file_name = []
        r = requests.get(
            '%s'%BASE_URL+'/gists',
            headers=self.headers
            )
        if (r.status_code == 200 ):
            r_text = json.loads(r.text)
            limit = offset if (offset <= len(r.json()) ) else len(r.json())

            for g,no in zip(r_text, range(0,limit)):
                for key,value in r.json()[no]['files'].items():
            
                    file_name.append(value['filename'])
            print("200:gist offset")
            print(file_name)
            return file_name
            
        raise Exception('Username not found')
    
    def getMyID(self,gist_name):
        '''
        Getting gistID of a gist in order to make the workflow
        easy and uninterrupted.
        '''
        r = requests.get(
            '%s'%BASE_URL+'/gists',
            headers=self.headers
            )
        if (r.status_code == 200):
            r_text = json.loads(r.text)
            limit = len(r.json())

            for g,no in zip(r_text, range(0,limit)):
                for ka,va in r.json()[no]['files'].items():
                    if str(va['filename']) == str(gist_name):
                        print("My id is ", r.json()[no]['id'])
                        return r.json()[no]['id']
        return 0
    
    
    def create(self, **args):
        if 'description' in args:
            self.description = args['description']
        else:
            self.description = ''

        if 'name' in args:
            self.gist_name = args['name']
        else:
            self.gist_name = ''

        if 'public' in args:
            self.public = args['public']
        else:
            self.public = 1

        if 'content' in args:
            self.content = args['content']
        else:
            raise Exception('Gist content can\'t be empty')

        url = '/gists'

        data = {"description": self.description,
                  "public": self.public,
                  "files": {
                    self.gist_name: {
                      "content": self.content
                    }
                  }
          }

        r = requests.post(
            '%s%s' % (BASE_URL, url),
            data=json.dumps(data),
            headers= self.headers
        )
        if (r.status_code == 201):
            response = {
            'Gist-Link': '%s/%s/%s' %(GIST_URL,self.user,r.json()['id']),
            'Clone-Link': '%s/%s.git' %(GIST_URL,r.json()['id']),
            'Embed-Script': '<script src="%s/%s/%s.js"</script>' %(GIST_URL,self.user,r.json()['id']),
            'id': r.json()['id'],
            'created_at': r.json()['created_at'],

            }
            self.gist_id = r.json()['id']
            print("Create Gist successful!: ", r)
            return response
        
        raise Exception('Gist not created: server response was [%s] %s' % (r.status_code, r.text))
    
    def read(self):
        
        r = requests.get(
            '%s'%BASE_URL+'/gists/'+'%s'%self.gist_id,
            headers=self.headers
            )
        if (r.status_code == 200 ):
            print("Read Gist Successful!: ", r)
            
        else:
            raise Exception('gist id not found')
        
    def update(self):
        
        updateddata = {
            "description": "Hello World Examples",
            "files": {
                "hello_world_python.txt": {
                    "content": "Run `python hello_world.py` to print Hello World",
                    "filename": "hello_world.md"
                },
                "new_file.txt": {
                    "content": "This is a new placeholder file."
                }
            }
        }
        
        r = requests.patch(
            '%s'%BASE_URL+'/gists/'+'%s'%self.gist_id,
            headers=self.headers,
            data = json.dumps(updateddata)
            )
        if (r.status_code == 200 ):
            print("Update Gist Successful!: ", r)
            
        else:
            raise Exception('gist id not found')
        
    def delete(self):
        
        r = requests.delete(
            '%s'%BASE_URL+'/gists/'+'%s'%self.gist_id,
            headers=self.headers
            )
        if (r.status_code == 204 ):
            print("Delete Gist Successful!: ", r)
            
        else:
            raise Exception('gist id not found')
     