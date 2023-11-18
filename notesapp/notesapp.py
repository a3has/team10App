from app import app, db
from models import User, NotePost
# app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Note': NotePost}
