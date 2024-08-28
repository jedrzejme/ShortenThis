from flask import Flask, render_template, request, abort, redirect, session
from configparser import ConfigParser

app = Flask(__name__, static_url_path='/static')

# Config for app settings
app_config = ConfigParser()
app_config.read('config.ini')

# Function to shorten URL
def shortening_url(url, short_url):
    urls_config = ConfigParser()
    urls_config.read('urls.ini')

    # Check if short_url exists, if not, add it
    if not urls_config.has_section(short_url):
        urls_config.add_section(short_url)
    urls_config.set(short_url, 'url', url)

    # Write the changes to urls.ini
    with open('urls.ini', 'w') as configfile:
        urls_config.write(configfile)

# Correct the URL format
def correction_of_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    return url

def random_string(length):
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def hash_string(string):
    import hashlib
    return hashlib.sha256(string.encode()).hexdigest()

# App settings from config.ini
app.secret_key = str(random_string(32))
app_config.set('main', 'app_secret_key', app.secret_key)
port = app_config.getint('main', 'port')
debug = app_config.getboolean('main', 'debug')

@app.route('/', methods=['GET', 'POST'])
def index():
    setuped = app_config.getboolean('main', 'setuped')
    
    if not setuped:
        if request.method == 'POST':
            # Handle the form submission
            app_url = str(request.form.get("app-url"))
            app_config.set('main', 'app_url', app_url)
            
            default_url_length = str(request.form.get("default-url-length"))
            app_config.set('main', 'default_url_length', default_url_length)

            if request.form.get("enable-authentication") == 'on':
                password = hash_string(str(request.form.get("password")))
                if password == '':
                    app_config.set('main', 'disable_authentication', 'True')
                else:
                    app_config.set('main', 'password', password)
                    app_config.set('main', 'disable_authentication', 'False')
            else:
                app_config.set('main', 'disable_authentication', 'True')

            app_config.set('main', 'setuped', 'True')
            
            # Save changes to the config.ini
            with open('config.ini', 'w') as configfile:
                app_config.write(configfile)
            
            # Redirect to the index after setup
            return redirect('/')
        
        # Render the setup page on GET requests
        return render_template('setup.html')
    
    # If already setup, render the index page
    return render_template('index.html', disable_authentication=app_config.getboolean('main', 'disable_authentication'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = str(request.form.get("password"))
        
        # Read from config.ini again to ensure fresh data
        app_config.read('config.ini')

        # Check password and set session if authenticated
        if hash_string(password) == app_config.get('main', 'password'):
            session['auth'] = True
            return redirect('/shorten-url')
        
    return render_template('login.html')

@app.route('/shorten-url', methods=['GET', 'POST'])
def shorten_url():
    if session.get('auth') or app_config.get('main', 'disable_authentication') == 'True':
        if request.method == 'POST':
            url = request.form.get("url")
            short_url = request.form.get("custom-short-url")

            # Generate a random short URL if not provided
            if short_url == '':
                short_url = random_string(app_config.getint('main', 'default_url_length'))

            # Correct the URL if needed
            url = correction_of_url(url)

            # Shorten and store the URL
            shortening_url(url, short_url)

            # Generate the shortened URL
            app_url = app_config.get('main', 'app_url')
            if app_url.endswith('/'):
                app_url = app_url[:-1]
            shortened_url = f"{app_url}/{short_url}"
            return render_template('shorten-url.html', shortened_url=shortened_url)
        else:
            return render_template('shorten-url.html')
    else:
        return redirect('/login')

@app.route('/<short_url>')
def shortUrl(short_url):
    urls_config = ConfigParser()
    urls_config.read('urls.ini')

    # Check if the short_url exists in urls.ini
    if urls_config.has_section(short_url):
        url = urls_config.get(short_url, 'url')
        return redirect(url, code=301)
    else:
        return abort(404, description="URL not found")

if __name__ == '__main__':
    app.run(host="localhost", port=port, debug=debug)