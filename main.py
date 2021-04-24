import http.client
import json

from flask import Flask
from flask import redirect
from flask import request
from flask import abort
from flask import render_template

from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from forms.toures_form import toures_form
from forms.user import RegisterForm
from forms.LoginForm import LoginForm
from forms.news import NewsForm
from forms.search_articles_form import SearchArticlesForm

from data.news import News
from data.users import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("main_page.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/table_EPL', methods=['GET', 'POST'])
def show_table_EPL():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
    connection.request('GET', '/v2/competitions/PL/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    table = response['standings'][0]['table']
    return render_template("show_table.html", table=table, name=response['competition']['name'])


@app.route("/matches_toures_EPL", methods=['GET', 'POST'])
def show_toures_EPL():
    form = toures_form()
    if form.validate_on_submit():
        if int(form.tour.data) in range(1, 39):
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
            connection.request('GET', f"/v2/competitions/PL/matches?matchday={form.tour.data}", None, headers)
            response = json.loads(connection.getresponse().read().decode())
            matches = response['matches']
            for i in range(len(matches)):
                matches[i]['utcDate'] = str(matches[i]['utcDate'])
            for i in range(len(matches)):
                matches[i]['utcDate'] = matches[i]['utcDate'][8:10] + '.' + matches[i]['utcDate'][5:7] + '.' + \
                                        matches[i]['utcDate'][:4] + ' ' + matches[i]['utcDate'][11:16]
            if int(form.tour.data) <= matches[0]['season']['currentMatchday']:
                show_score = True
            else:
                show_score = False
            print(show_score)
            return render_template("show_matches.html", matches=matches, name=response['competition']['name'],
                                   tour=form.tour.data, score=show_score)
        else:
            return render_template('toures_form.html',
                                   message="Нет тура с таким номером",
                                   form=form)
    return render_template('toures_form.html', title='Поиск статей', form=form)


@app.route("/matches_toures_PD", methods=['GET', 'POST'])
def show_toures_PD():
    form = toures_form()
    if form.validate_on_submit():
        if int(form.tour.data) in range(1, 39):
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
            connection.request('GET', f"/v2/competitions/PD/matches?matchday={form.tour.data}", None, headers)
            response = json.loads(connection.getresponse().read().decode())
            matches = response['matches']
            for i in range(len(matches)):
                matches[i]['utcDate'] = str(matches[i]['utcDate'])
            for i in range(len(matches)):
                matches[i]['utcDate'] = matches[i]['utcDate'][8:10] + '.' + matches[i]['utcDate'][5:7] + '.' + \
                                        matches[i]['utcDate'][:4] + ' ' + matches[i]['utcDate'][11:16]
            if int(form.tour.data) <= matches[0]['season']['currentMatchday']:
                show_score = True
            else:
                show_score = False
            print(show_score)
            return render_template("show_matches.html", matches=matches, name=response['competition']['name'],
                                   tour=form.tour.data, score=show_score)
        else:
            return render_template('toures_form.html',
                                   message="Нет тура с таким номером",
                                   form=form)
    return render_template('toures_form.html', title='Поиск статей', form=form)


@app.route("/matches_toures_BL1", methods=['GET', 'POST'])
def show_toures_BL1():
    form = toures_form()
    if form.validate_on_submit():
        if int(form.tour.data) in range(1, 35):
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
            connection.request('GET', f"/v2/competitions/BL1/matches?matchday={form.tour.data}", None, headers)
            response = json.loads(connection.getresponse().read().decode())
            matches = response['matches']
            for i in range(len(matches)):
                matches[i]['utcDate'] = str(matches[i]['utcDate'])
            for i in range(len(matches)):
                matches[i]['utcDate'] = matches[i]['utcDate'][8:10] + '.' + matches[i]['utcDate'][5:7] + '.' + \
                                        matches[i]['utcDate'][:4] + ' ' + matches[i]['utcDate'][11:16]
            if int(form.tour.data) <= matches[0]['season']['currentMatchday']:
                show_score = True
            else:
                show_score = False
            print(show_score)
            return render_template("show_matches.html", matches=matches, name=response['competition']['name'],
                                   tour=form.tour.data, score=show_score)
        else:
            return render_template('toures_form.html',
                                   message="Нет тура с таким номером",
                                   form=form)
    return render_template('toures_form.html', title='Поиск статей', form=form)


@app.route("/matches_toures_SA", methods=['GET', 'POST'])
def show_toures_SA():
    form = toures_form()
    if form.validate_on_submit():
        if int(form.tour.data) in range(1, 39):
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
            connection.request('GET', f"/v2/competitions/SA/matches?matchday={form.tour.data}", None, headers)
            response = json.loads(connection.getresponse().read().decode())
            matches = response['matches']
            for i in range(len(matches)):
                matches[i]['utcDate'] = str(matches[i]['utcDate'])
            for i in range(len(matches)):
                matches[i]['utcDate'] = matches[i]['utcDate'][8:10] + '.' + matches[i]['utcDate'][5:7] + '.' + \
                                        matches[i]['utcDate'][:4] + ' ' + matches[i]['utcDate'][11:16]
            if int(form.tour.data) <= matches[0]['season']['currentMatchday']:
                show_score = True
            else:
                show_score = False
            print(show_score)
            return render_template("show_matches.html", matches=matches, name=response['competition']['name'],
                                   tour=form.tour.data, score=show_score)
        else:
            return render_template('toures_form.html',
                                   message="Нет тура с таким номером",
                                   form=form)
    return render_template('toures_form.html', title='Поиск статей', form=form)


@app.route("/matches_toures_FL1", methods=['GET', 'POST'])
def show_toures_FL1():
    form = toures_form()
    if form.validate_on_submit():
        if int(form.tour.data) in range(1, 39):
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
            connection.request('GET', f"/v2/competitions/FL1/matches?matchday={form.tour.data}", None, headers)
            response = json.loads(connection.getresponse().read().decode())
            matches = response['matches']
            for i in range(len(matches)):
                matches[i]['utcDate'] = str(matches[i]['utcDate'])
            for i in range(len(matches)):
                matches[i]['utcDate'] = matches[i]['utcDate'][8:10] + '.' + matches[i]['utcDate'][5:7] + '.' + \
                                        matches[i]['utcDate'][:4] + ' ' + matches[i]['utcDate'][11:16]
            if int(form.tour.data) <= matches[0]['season']['currentMatchday']:
                show_score = True
            else:
                show_score = False
            print(show_score)
            return render_template("show_matches.html", matches=matches, name=response['competition']['name'],
                                   tour=form.tour.data, score=show_score)
        else:
            return render_template('toures_form.html',
                                   message="Нет тура с таким номером",
                                   form=form)
    return render_template('toures_form.html', title='Поиск статей', form=form)


@app.route("/matches_toures_BSA", methods=['GET', 'POST'])
def show_toures_BSA():
    form = toures_form()
    if form.validate_on_submit():
        if int(form.tour.data) in range(1, 39):
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
            connection.request('GET', f"/v2/competitions/BSA/matches?matchday={form.tour.data}", None, headers)
            response = json.loads(connection.getresponse().read().decode())
            matches = response['matches']
            for i in range(len(matches)):
                matches[i]['utcDate'] = str(matches[i]['utcDate'])
            for i in range(len(matches)):
                matches[i]['utcDate'] = matches[i]['utcDate'][8:10] + '.' + matches[i]['utcDate'][5:7] + '.' + \
                                        matches[i]['utcDate'][:4] + ' ' + matches[i]['utcDate'][11:16]
            if int(form.tour.data) <= matches[0]['season']['currentMatchday']:
                show_score = True
            else:
                show_score = False
            print(show_score)
            return render_template("show_matches.html", matches=matches, name=response['competition']['name'],
                                   tour=form.tour.data, score=show_score)
        else:
            return render_template('toures_form.html',
                                   message="Нет тура с таким номером",
                                   form=form)
    return render_template('toures_form.html', title='Поиск статей', form=form)


@app.route("/matches_toures_DED", methods=['GET', 'POST'])
def show_toures_DED():
    form = toures_form()
    if form.validate_on_submit():
        if int(form.tour.data) in range(1, 35):
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
            connection.request('GET', f"/v2/competitions/DED/matches?matchday={form.tour.data}", None, headers)
            response = json.loads(connection.getresponse().read().decode())
            matches = response['matches']
            for i in range(len(matches)):
                matches[i]['utcDate'] = str(matches[i]['utcDate'])
            for i in range(len(matches)):
                matches[i]['utcDate'] = matches[i]['utcDate'][8:10] + '.' + matches[i]['utcDate'][5:7] + '.' + \
                                        matches[i]['utcDate'][:4] + ' ' + matches[i]['utcDate'][11:16]
            if int(form.tour.data) <= matches[0]['season']['currentMatchday']:
                show_score = True
            else:
                show_score = False
            print(show_score)
            return render_template("show_matches.html", matches=matches, name=response['competition']['name'],
                                   tour=form.tour.data, score=show_score)
        else:
            return render_template('toures_form.html',
                                   message="Нет тура с таким номером",
                                   form=form)
    return render_template('toures_form.html', title='Поиск статей', form=form)


@app.route("/matches_toures_PPL", methods=['GET', 'POST'])
def show_toures_PPL():
    form = toures_form()
    if form.validate_on_submit():
        if int(form.tour.data) in range(1, 35):
            connection = http.client.HTTPConnection('api.football-data.org')
            headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
            connection.request('GET', f"/v2/competitions/PPL/matches?matchday={form.tour.data}", None, headers)
            response = json.loads(connection.getresponse().read().decode())
            matches = response['matches']
            for i in range(len(matches)):
                matches[i]['utcDate'] = str(matches[i]['utcDate'])
            for i in range(len(matches)):
                matches[i]['utcDate'] = matches[i]['utcDate'][8:10] + '.' + matches[i]['utcDate'][5:7] + '.' + \
                                        matches[i]['utcDate'][:4] + ' ' + matches[i]['utcDate'][11:16]
            if int(form.tour.data) <= matches[0]['season']['currentMatchday']:
                show_score = True
            else:
                show_score = False
            print(show_score)
            return render_template("show_matches.html", matches=matches, name=response['competition']['name'],
                                   tour=form.tour.data, score=show_score)
        else:
            return render_template('toures_form.html',
                                   message="Нет тура с таким номером",
                                   form=form)
    return render_template('toures_form.html', title='Поиск статей', form=form)


@app.route('/table_BL1', methods=['GET', 'POST'])
def show_table_BL1():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
    connection.request('GET', '/v2/competitions/BL1/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    table = response['standings'][0]['table']
    return render_template("show_table.html", table=table, name=response['competition']['name'])


@app.route('/table_FL1', methods=['GET', 'POST'])
def show_table_FL1():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
    connection.request('GET', '/v2/competitions/FL1/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    table = response['standings'][0]['table']
    return render_template("show_table.html", table=table, name=response['competition']['name'])


@app.route('/table_BSA', methods=['GET', 'POST'])
def show_table_BSA():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
    connection.request('GET', '/v2/competitions/BSA/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    table = response['standings'][0]['table']
    return render_template("show_table.html", table=table, name=response['competition']['name'])


@app.route('/table_DED', methods=['GET', 'POST'])
def show_table_DED():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
    connection.request('GET', '/v2/competitions/DED/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    table = response['standings'][0]['table']
    return render_template("show_table.html", table=table, name=response['competition']['name'])


@app.route('/table_PPL', methods=['GET', 'POST'])
def show_table_PPL():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
    connection.request('GET', '/v2/competitions/PPL/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    table = response['standings'][0]['table']
    return render_template("show_table.html", table=table, name=response['competition']['name'])


@app.route('/table_PD', methods=['GET', 'POST'])
def show_table_PD():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
    connection.request('GET', '/v2/competitions/PD/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    table = response['standings'][0]['table']
    return render_template("show_table.html", table=table, name=response['competition']['name'])


@app.route('/table_SA', methods=['GET', 'POST'])
def show_table_SA():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'a80b321e968a4931b45430b943db2a29'}
    connection.request('GET', '/v2/competitions/SA/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    table = response['standings'][0]['table']
    return render_template("show_table.html", table=table, name=response['competition']['name'])


@app.route('/leagues', methods=['GET', 'POST'])
def show_leagues():
    return render_template("matches.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/tables', methods=['GET', 'POST'])
def chose_league():
    return render_template('tables.html')


@app.route('/search_articles', methods=['GET', 'POST'])
def search_articles():
    form = SearchArticlesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(
            form.theme.data == News.title).all()
        return render_template("found_articles.html", news=news)
    return render_template('search_articles.html', title='Поиск статей', form=form)


@app.route('/article/<id>/<title>/<content>/<user>', methods=['GET', 'POST'])
def show_article(id, title, content, user):
    return render_template('article.html', id=id, content=content, title=title, user=user)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.description = form.description.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.description.data = news.description
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.description = form.description.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
