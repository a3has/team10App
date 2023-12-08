from app import app, db
from models import User, Note
import os

# eases the warning on redirects on https and allows the use of http
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# scope changed often and takes ages to update from google cloud so i turned that warning off
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
# ignores csrf attack warning, google is very picky about this
os.environ['WTF_CSRF_CHECK_DEFAULT'] = 'False'


@app.shell_context_processor
def make_shell_context():  # define a shell
    return {'db': db, 'User': User, 'Note': Note}
