<h1 align = 'center'>
    <img 
        src = '/assets/icon.png' 
        height = '200' 
        width = '200' 
        alt = 'Icon' 
    />
    <br>
    Shorten That
    <br>
</h1>

<div align = 'center'>
    <a href = 'https://github.com/jedrzejme/ShortenThat/'>
        <img src = 'https://img.shields.io/github/stars/jedrzejme/ShortenThat?style=for-the-badge&color=%23cfb002'/>
    </a>
    <a href = 'https://github.com/jedrzejme/ShortenThat/tags'>
        <img src = 'https://img.shields.io/github/v/tag/jedrzejme/ShortenThat?style=for-the-badge&label=version'/>
    </a>
    <a href = 'https://github.com/jedrzejme/ShortenThat/issues'>
        <img src = 'https://img.shields.io/github/issues/jedrzejme/ShortenThat?style=for-the-badge&color=%23ff6f00'/>
    </a>
    <a href = 'https://github.com/jedrzejme/ShortenThat/pulls'>
        <img src = 'https://img.shields.io/github/issues-pr/jedrzejme/ShortenThat?style=for-the-badge'/>
    </a>
</div>

<br>

**❓ What is this?** Web app for shortening links. Backend is written in Flask (Python framework).

**❓ How to use it?**
* [**Using docker-compose**](#using-docker-compose-to-run-shorten-that)
* [**Using Python**](#using-python-to-run-shorten-that)

**❓ What did I use?**
* [Python](https://www.python.org/)
* [Python libraries](/requirements.txt)
* [Docker](https://www.docker.com/)
* [Coding](https://code.visualstudio.com/)
* [Git management](https://desktop.github.com/)

## 🐳 Using docker-compose to run Shorten That
1) Install Docker, docker-compose and Git
2) Clone this repository and enter its directory:
```
git clone https://github.com/jedrzejme/ShortenThat.git
```
3) Edit config.ini (do not change port in config.ini; if you want to change external port change it in docker-compose.yml)
4) Create docker image:
```
docker build -t shorten-that .
```
5) Run docker-compose (by default it will run on port 5000):
```
docker-compose up -d
```
6) It works!

## 🐍 Using Python to run Shorten That
1) Install Python
2) Clone this repository and enter its directory:
```
git clone https://github.com/jedrzejme/ShortenThat.git
```
3) Install requirements.txt:
```
python -m pip install -r requirements.txt
```
4) Edit config.ini
5) Run app.py (by default it will run on port 5000):
```
python app.py
```
6) It works!

## 🚀 Features
* Authentication by password provided in config.ini
* Shortening URL with custom short URL

## 💲 Support
<p><a href="https://support.jedrzej.me/" target="_blank"> <img align="left" src="https://raw.githubusercontent.com/jedrzejme/jedrzejme/main/assets/supportme.svg" height="50" width="210" alt="jedrzejme" /></a></p>