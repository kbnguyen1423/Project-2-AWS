from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = '/var/www/html/flaskapp/users'
app.config.from_object(__name__)

conn = sqlite3.connect(app.config['DATABASE'])
cursor = conn.cursor()

cursor.execute('''  CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL
        )
        ''')
conn.commit()

conn.close()


@app.route('/')
def registration_page():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Registration Page</title>
        </head>
        <body>
            <h1>Registration Page</h1>
            <form action="/register" method="post">
                <label>Username:</label>
                <input type="text" name="username" required><br>
                <label>Password:</label>
                <input type="password" name="password" required><br>
                <label>First Name:</label>
                <input type="text" name="first_name" required><br>
                <label>Last Name:</label>
                <input type="text" name="last_name" required><br>
                <label>Email:</label>
                <input type="email" name="email" required><br>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
    '''



@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (username, password, first_name, last_name, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, first_name, last_name, email))
        conn.commit()

        return redirect(url_for('login_page'))

    except sqlite3.IntegrityError:
        return "Username already exists, please choose another."

    finally:
        conn.close()

@app.route('/login')
def login_page():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login Page</title>
        </head>
        <body>
            <h1>Login Page</h1>
            <form action="/retrieve_info" method="post">
                <label>Username:</label>
                <input type="text" name="username" required><br>
                <label>Password:</label>
                <input type="password" name="password" required><br>
                <input type="submit" value="Login">
            </form>
        </body>
        </html>
    '''


@app.route('/retrieve_info', methods=['POST'])
def retrieve_info():
    entered_username = request.form.get('username')
    entered_password = request.form.get('password')

    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (entered_username, entered_password))
    user_info = cursor.fetchone()

    if user_info:
        user_info_dict = {
            'id': user_info[0],
            'username': user_info[1],
            'password': user_info[2],
            'first_name': user_info[3],
            'last_name': user_info[4],
            'email': user_info[5]
        }

        return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>User Information</title>
            </head>
            <body>
                <h1>User Information</h1>
                <p>First Name: {user_info_dict['first_name']}</p>
                <p>Last Name: {user_info_dict['last_name']}</p>
                <p>Email: {user_info_dict['email']}</p>
            </body>
            </html>
        '''

    else:
        return "Invalid credentials."


if __name__ == '__main__':
    app.run(debug=True)

