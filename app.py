from flask import Flask, render_template, request, abort, redirect, session
from configparser import ConfigParser

app = Flask(__name__, static_url_path='/static')

# Config for app settings
app_config = ConfigParser()
app_config.read('config.ini')

# App settings from config.ini
app_url = app_config.get('main', 'app_url')
port = app_config.getint('main', 'port')
debug = app_config.getboolean('main', 'debug')
app.secret_key = app_config.get('main', 'app_secret_key')
default_url_lenght = app_config.getint('main', 'default_url_lenght')

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

def random_string():
    length = default_url_lenght
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get("password")
        
        # Read from config.ini again to ensure fresh data
        app_config.read('config.ini')

        # Check password and set session if authenticated
        if password == app_config.get('main', 'password'):
            session['auth'] = True
            return redirect('/shorten-url')
        
    return render_template('login.html')

@app.route('/shorten-url', methods=['GET', 'POST'])
def shorten_url():
    if session.get('auth'):
        if request.method == 'POST':
            url = request.form.get("url")
            short_url = request.form.get("custom-short-url")

            # Generate a random short URL if not provided
            if short_url == '':
                short_url = random_string()

            # Correct the URL if needed
            url = correction_of_url(url)

            # Shorten and store the URL
            shortening_url(url, short_url)

            # Generate the shortened URL
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