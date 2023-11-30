from app import app, db
from models import User, Note
import os

#set environmental variables for developers 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['WTF_CSRF_CHECK_DEFAULT'] = 'False'


@app.shell_context_processor 
def make_shell_context(): # define a shell 
    return {'db': db, 'User': User, 'Note': Note}
