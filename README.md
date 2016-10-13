# Spotify / Infinity Mirror

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Update](#update)

## Requirements
- [Python 2.7.x](http://docs.python-guide.org/en/latest/starting/installation/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [supervisor](http://supervisord.org/installing.html#installing)

## Installation
1. Clone the git: `git clone https://github.com/d3estudio/spotify-infinity-mirror`
2. Go into the new directory: `cd spotify-infinity-mirror`
3. For supervisor command install:
  1. For client setup: Run `./setup.sh --client`  
    This will install the requirements and setup the supervisor
  2. For client setup: Run `./setup.sh --server`  
    This will install the requirements and setup the supervisor

## Update
1. Go into the application directory: `cd spotify-infinity-mirror`
2. Run `./setup.sh --update`