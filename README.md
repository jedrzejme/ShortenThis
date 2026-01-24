<h1 align = 'center'>
    <img 
        src = '/assets/icon.png' 
        height = '200' 
        width = '200' 
        alt = 'Icon' 
    />
    <br>
    Shorten This
    <br>
</h1>

<div align = 'center'>
    <a href = 'https://github.com/jbakalarski/ShortenThis/'>
        <img src = 'https://img.shields.io/github/stars/jbakalarski/ShortenThis?style=for-the-badge&color=%23cfb002'/>
    </a>
    <a href = 'https://github.com/jbakalarski/ShortenThis/tags'>
        <img src = 'https://img.shields.io/github/v/tag/jbakalarski/ShortenThis?style=for-the-badge&label=version'/>
    </a>
    <a href = 'https://github.com/jbakalarski/ShortenThis/issues'>
        <img src = 'https://img.shields.io/github/issues/jbakalarski/ShortenThis?style=for-the-badge&color=%23ff6f00'/>
    </a>
    <a href = 'https://github.com/jbakalarski/ShortenThis/pulls'>
        <img src = 'https://img.shields.io/github/issues-pr/jbakalarski/ShortenThis?style=for-the-badge'/>
    </a>
</div>

<br>

**❓ What is this?** Web app for shortening links. Backend is written in Flask (Python framework).

**❓ How to use it?**
* [**Using docker-compose**](#-using-docker-compose-to-run-shorten-this)
* [**Using Python**](#-using-python-to-run-shorten-this)

**❓ What did I use?**
* [Python](https://www.python.org/)
* [Docker](https://www.docker.com/)
* [Bootstrap Studio](https://bootstrapstudio.io/)
* [Coding](https://code.visualstudio.com/)
* [Git management](https://desktop.github.com/)

## 🐳 Using docker-compose to run Shorten This
1) Install Docker and docker-compose
2) Create file called docker-compose.yml and paste this inside:
```
services:
    shorten-this:
        container_name: shorten-this
        ports:
            - 5000:5000 # <Host Port>:<Container Port (do not change)>
        image: jedrzejme/shorten-this:latest
        volumes:
            - database.db:/app/database.db
        restart: unless-stopped
```
3) Optionally edit port in docker-compose.yml
4) Create empty file called database.db in the same directory as docker-compose.yml
5) Run docker-compose (by default it will run on port 5000):
```
docker-compose up -d
```
6) It works!

## 🐍 Using Python to run Shorten This
1) Install Python
2) Clone this repository and enter its directory:
```
git clone https://github.com/jbakalarski/ShortenThis.git
```
3) Install requirements.txt:
```
python -m pip install -r requirements.txt
```
4) Optionally edit port in app.py (port is defined at the bottom of script)
5) Create empty file called database.db in the same directory as this repository
6) Run app.py (by default it will run on port 5000):
```
python app.py
```
7) It works!

## 🚀 Features
* Setup screen on first run
* Authentication by password
* Settings screen
* Users screen
* Shortening URL with custom short URL (if not provided, short URL will be set to random string of length provided in setup)
* Stats of shortened URL
* Option to delete link in control panel
* Usage of sqlite3 to manage data about links and app

## 💲 Support
<p><a href="https://support.jedrzej.me/" target="_blank"> <img align="left" src="https://raw.githubusercontent.com/jbakalarski/jbakalarski/main/assets/supportme.png" width="172" height="56" alt="jbakalarski" /></a></p>