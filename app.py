from flask import Flask, render_template
from datamanager.data_manager import SQLiteDataManager

app = Flask(__name__)

data_manager = SQLiteDataManager('moviwebapp.db')  


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
