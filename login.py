from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 連接到 SQLite 資料庫
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 建立用來儲存使用者資訊的資料表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()

# 驗證使用者資訊的函式
def authenticate(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['register-username']
    password = request.form['register-password']

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        # Redirect to the register success page with the username and password as arguments
        return redirect(url_for('register_success', username=username, password=password))
    except sqlite3.IntegrityError:
        return "使用者名稱已存在。請選擇不同的使用者名稱。"

@app.route('/register_success')
def register_success():
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template('register_success.html', username=username, password=password)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['login-username']
    password = request.form['login-password']

    user = authenticate(username, password)

    if user:
        # Redirect to the login success page with the username as an argument
        return redirect(url_for('login_success', username=username))
    else:
        return "無效的使用者名稱或密碼。"

@app.route('/login_success')
def login_success():
    username = request.args.get('username')
    return render_template('login_success.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
