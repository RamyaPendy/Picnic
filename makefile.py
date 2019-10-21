from simpletest import gistapi
from config import *

ghGist = gistapi()

#User Authentication
ghGist.auth()

#List all gist
ghGist.listgist()

#Display required number of filenames
ghGist.list(2)

#Get my id
ghGist.getMyID("test")

#Create gist
ghGist.create(name='_GISTNAME', description='_ANY_DESCRIPTION', public='true', content='_CONTENT_GOES_HERE')

#Read created gist by id
ghGist.read()

#Update created gist by id
ghGist.update()

#Delete the gist created by id
ghGist.delete()