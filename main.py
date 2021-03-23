from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index(name=None, items=None):
    poetry = ['картина', 'корзина', 'картонка']
    return render_template('index.html', name='qqqqqqqqqqqqqqqqqqq', items=poetry)


app.run('127.0.0.1', 8080, debug=True)