from flask import Flask, render_template, request, abort, redirect, session, send_file
import random
import string
import hashlib
import sqlite3
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

conn = sqlite3.connect('database.db', check_same_thread=False)
db = conn.cursor()

# Create tables if not exists
db.execute("""CREATE TABLE IF NOT EXISTS `users` (
`username` TEXT NOT NULL UNIQUE,
`password` TEXT,
`permissions` INTEGER NOT NULL
)""")

db.execute("""CREATE TABLE IF NOT EXISTS `config` (
`id` INTEGER NOT NULL,
`setuped` INTEGER NOT NULL,
`app_name` TEXT NOT NULL,
`app_url` TEXT NOT NULL,
`app_secret_key` TEXT NOT NULL,
`disable_authentication` INTEGER NOT NULL,
`default_url_length` INTEGER NOT NULL
)""")

db.execute("""CREATE TABLE IF NOT EXISTS `urls` (
`short_url` TEXT NOT NULL UNIQUE,
`url` TEXT NOT NULL,
`date` TEXT NOT NULL,
`ip` TEXT NOT NULL,
`clicks` INTEGER
)""")

db.execute("""CREATE TABLE IF NOT EXISTS `stats` (
`id` integer primary key NOT NULL,
`short_url` TEXT,
`date` TEXT,
`ip` TEXT,
`user_agent` TEXT,
`referer` TEXT
)""")

# Function to setup the app
def setup(app_name, app_url, disable_authentication, default_url_length):
    # Insert values to config table
    db.execute('SELECT setuped FROM config WHERE id = ?', ("1",))
    if db.fetchone() is None:
        db.execute("INSERT INTO config (id, setuped, app_name, app_url, app_secret_key, disable_authentication, default_url_length) VALUES (1, ?, ?, ?, ?, ?, ?)", (1, app_name, app_url, app.secret_key, disable_authentication, default_url_length))
        conn.commit()

# Function to get a config setting
def getting_config(setting):
    db.execute(f'SELECT {setting} FROM config WHERE id = ?', ("1",))
    result = db.fetchone()
    return result[0] if result else None

def changing_config(setting, value):
    db.execute(f'UPDATE config SET {setting} = ? WHERE id = ?', (value, "1"))
    conn.commit()

# Function to create a user
def creating_user(username, password, permissions):
    db.execute("INSERT INTO users (username, password, permissions) VALUES (?, ?, ?)", (username, password, permissions))
    conn.commit()

def delete_user(username):
    db.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()

# Function to get user info
def get_userinfo(username, column):
    db.execute(f'SELECT "{column}" FROM users WHERE username = ?', (username,))
    result = db.fetchone()
    return result[0] if result else None

def get_all_users():
    db.execute('SELECT * FROM users')
    column_names = [description[0] for description in db.description]  # Access description right after the query
    rows = db.fetchall()  # Fetch all rows after accessing the column names
    result = [dict(zip(column_names, row)) for row in rows]
    return result

# Function to shorten URL
def shortening_url(url, short_url):
    # Generate a random short URL if not provided
    if short_url == '':
        short_url = random_string(getting_config('default_url_length'))

    # Correct the URL if needed
    url = correction_of_url(url)
    app_url = getting_config('app_url')
    if app_url.endswith('/'):
        app_url = app_url[:-1]
    shortened_url = f"{app_url}/{short_url}"
    now = datetime.now()
    formatted_date = now.strftime("%b %d, %Y %H:%M")
    db.execute("INSERT INTO urls (short_url, url, date, ip, clicks) VALUES (?, ?, ?, ?, ?)", (short_url, url, formatted_date, request.remote_addr, 0))
    conn.commit()
    return shortened_url

def add_stats(short_url):
    now = datetime.now()
    formatted_date = now.strftime("%b %d, %Y %H:%M")
    db.execute("INSERT INTO stats (short_url, date, ip, user_agent, referer) VALUES (?, ?, ?, ?, ?)", (short_url, formatted_date, request.remote_addr, request.headers.get('User-Agent'), request.headers.get('Referer')))
    conn.commit()
    db.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_url = ?", (short_url,))
    conn.commit()

def get_stats(short_url):
    db.execute('SELECT * FROM stats WHERE short_url = ? ORDER BY id DESC', (short_url,))
    column_names = [description[0] for description in db.description]
    rows = db.fetchall()
    result = [dict(zip(column_names, row)) for row in rows]
    return result

# Correct the URL format
def correction_of_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    return url

# Function to check if a short URL exists
def does_shorted_url_exist(short_url):
    db.execute('SELECT short_url FROM urls WHERE short_url = ?', (short_url,))
    result = db.fetchone()
    return result[0] if result else None

def get_url(short_url):
    db.execute('SELECT url FROM urls WHERE short_url = ?', (short_url,))
    result = db.fetchone()
    return result[0] if result else None

def get_all_urls():
    db.execute('SELECT * FROM urls')
    column_names = [description[0] for description in db.description]  # Access description right after the query
    rows = db.fetchall()  # Fetch all rows after accessing the column names
    result = [dict(zip(column_names, row)) for row in rows]
    return result

def delete_url(short_url):
    db.execute('DELETE FROM urls WHERE short_url = ?', (short_url,))
    conn.commit()
    db.execute('DELETE FROM stats WHERE short_url = ?', (short_url,))
    conn.commit()

# Function to generate a random string
def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to hash a string
def hash_string(string):
    return hashlib.sha256(string.encode()).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def index():
    db.execute('SELECT setuped FROM config WHERE id = ?', ("1",))
    setuped = db.fetchone()
    
    if not setuped:
        if request.method == 'POST':
            # Handle the form submission
            app_name = str(request.form.get("app-name"))
            app_url = str(request.form.get("app-url"))
            default_url_length = str(request.form.get("default-url-length"))
            favicon = request.files.get('favicon') or None
            if favicon:
                file = favicon
                file.save("static/assets/img/favicon.png")

            if request.form.get("enable-authentication") == 'on':
                username = str(request.form.get("username"))
                password = hash_string(str(request.form.get("password")))
                creating_user(username, password, 10)
                if password == '':
                    disable_authentication = 1
                else:
                    disable_authentication = 0
            else:
                disable_authentication = 1

            setup(app_name, app_url, disable_authentication, default_url_length)

            # Redirect to the index after setup
            return redirect('/')
        
        # Render the setup page on GET requests
        return render_template('setup.html', app_name="Shorten This", app_url = f"{request.headers.get('X-Forwarded-Proto') or request.scheme}://{request.headers.get('X-Forwarded-Host') or request.host}")
    
    # If already setup, render the index page
    return render_template('index.html', app_name=getting_config('app_name'), disable_authentication=getting_config('disable_authentication'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not bool(getting_config('disable_authentication')):
        if request.method == 'POST':
            username = str(request.form.get("username"))
            password = str(request.form.get("password"))

            # Check password and set session if authenticated
            if hash_string(password) == get_userinfo(username, "password"):
                session['auth'] = True
                session['username'] = username
                return redirect('/control-panel?section=urls')
            
        return render_template('login.html', app_name=getting_config('app_name'))
    else:
        return redirect('/')

@app.route('/control-panel', methods=['GET', 'POST'])
def control_panel():
    if session.get('auth') or bool(getting_config('disable_authentication')):
        section = request.args.get("section")
        if section == 'urls':
            if request.method == 'POST':
                url = request.form.get("url")
                short_url = request.form.get("custom-short-url")
                shortened_url = shortening_url(url, short_url)
                return render_template('control-panel.html', app_name=getting_config('app_name'), shortened_url=shortened_url, username=session.get('username') or "user", urls=get_all_urls(), disable_authentication=bool(getting_config('disable_authentication')), section=request.args.get("section"))
            return render_template('control-panel.html', app_name=getting_config('app_name'), username=session.get('username') or "user", urls=get_all_urls(), disable_authentication=bool(getting_config('disable_authentication')), section=request.args.get("section"))
        elif section == 'settings' and session.get('auth'):
            if request.method == 'POST':
                app_name = str(request.form.get("app-name"))
                app_url = str(request.form.get("app-url"))
                default_url_length = str(request.form.get("default-url-length"))
                favicon = request.files.get('favicon') or None
                if favicon:
                    file = favicon
                    file.save("static/assets/img/favicon.png")

                changing_config('app_name', app_name)
                changing_config('app_url', app_url)
                changing_config('default_url_length', default_url_length)
                return redirect('control-panel?section=settings')
            return render_template('control-panel.html', app_name=getting_config('app_name'), username=session.get('username') or "user", app_url = getting_config('app_url'), default_url_length = int(getting_config('default_url_length')), section=request.args.get("section"))
        elif section == 'users' and session.get('auth'):
            if request.method == 'POST':
                username = str(request.form.get("username"))
                password = hash_string(str(request.form.get("password")))
                permissions = 10
                creating_user(username, password, permissions)
                return redirect('control-panel?section=users')
            return render_template('control-panel.html', app_name=getting_config('app_name'), username=session.get('username') or "user", users=get_all_users(), disable_authentication=bool(getting_config('disable_authentication')), section=request.args.get("section"))
        elif section == 'stats' and session.get('auth') or bool(getting_config('disable_authentication')):
            short_url = request.args.get('short_url')
            return render_template('control-panel.html', app_name=getting_config('app_name'), username=session.get('username') or "user", stats=get_stats(short_url), disable_authentication=bool(getting_config('disable_authentication')), section=request.args.get("section"), short_url=short_url)
    else:
        return redirect('/login')
    
@app.route('/control-panel/action', methods=['GET', 'POST'])
def control_panel_action():
    action = request.args.get('action')
    if action == 'delete_url' and (session.get('auth') or bool(getting_config('disable_authentication'))):
        short_url = request.args.get('short_url')
        delete_url(short_url)
        return redirect('/control-panel?section=urls')
    elif action == 'delete_user' and session.get('auth'):
        username = request.args.get('username')
        delete_user(username)
        return redirect('/control-panel?section=users')
    elif action == 'download_backup' and session.get('auth'):
        now = datetime.now()
        return send_file("database.db", as_attachment=True, download_name=f"""{getting_config("app_name")}-backup-{now.strftime("%Y-%m-%d %H-%M-%S")}.db""")
    else:
        return abort(404, description="Action not found")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/<short_url>')
def shortUrl(short_url):
    # Check if the short_url exists
    if does_shorted_url_exist(short_url) == short_url:
        url = get_url(short_url)
        add_stats(short_url)
        print(dict(request.headers))
        return redirect(url, code=301)
    else:
        return abort(404, description="URL not found")

app.secret_key = str(random_string(32))
app_port = 5000
app_debug = False

if __name__ == '__main__':
    app.run(host="localhost", port=app_port, debug=app_debug)