from flask import Flask, render_template
from .database import db, User

app = Flask(__name__)


@app.route('/users')
def users():
    users = db.session.query(User)
    return render_template("users.html", users=users)

if __name__ == '__main__':
    app.run()
