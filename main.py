import datetime
from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm


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


@app.route('/login')
def login():
    return 'Вы зарегистрированы'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_session.global_init('db/mars_explorer.db')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
