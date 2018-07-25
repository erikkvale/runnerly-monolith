from celery import Celery
from stravalib import Client
from .database import db, User, Run


BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None

@celery.task
def fetch_all_runs():
    global _APP
    # lazy init
    if _APP is None:
        from .app import create_app
        app = create_app()
        db.init_app(app)
    else:
        app = _APP

    runs_fetched = {}
    with app.app_context():
        q = db.session.query(User)
        for user in q:
            if user.strava_token is None:
                continue
            print('Fetching Strava for %s' % user.email)
            runs_fetched[user.id] = fetch_all_run
