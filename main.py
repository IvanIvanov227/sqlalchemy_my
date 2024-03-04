import datetime
from flask import Flask, render_template
from data import db_session
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678оченьнадежныйпароль'


def create_jobs(db_sess):
    job = Jobs(
        team_leader=1,
        job='какая-то работа 2.0',
        work_size=1,
        collaborators='2, 5',
        start_date=datetime.datetime.now(),
        is_finished=True
    )
    db_sess.add(job)
    db_sess.commit()


@app.route('/')
def index():
    db_session.global_init('db/mars_explorer.db')
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template('jobs.html', jobs=jobs)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
