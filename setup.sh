#!/usr/bin/env bash
#encoding=utf8

define(){ IFS='\n' read -r -d '' ${1} || true; }

supervisord_path="/etc/supervisor/conf.d"
application_path=$(cd "$(dirname "$0")"; pwd)
application_config="
[program:infinity_mirror]
autostart = true
autorestart = true
startretries = 3
startsecs = 1
stopwaitsecs = 1
numprocs = 1
priority = 99
redirect_stder = true
stdout_logfile = /var/log/supervisor/infinity_mirror.log
user = pi
directory = $application_path"

function ApplicationInstallClient() {
  instance="client"
  sudo echo "$application_config"  > /etc/supervisor/conf.d/infinity-mirror.conf
  sudo echo "command = python $application_path/$instance.py" >> /etc/supervisor/conf.d/infinity-mirror.conf
}

function ApplicationInstallServer() {
  instance="server"
  sudo echo "$application_config" > /etc/supervisor/conf.d/infinity-mirror.conf
  sudo echo "command = python $application_path/$instance.py" >> /etc/supervisor/conf.d/infinity-mirror.conf
}

function ApplicationUpdate () {
  cd $application_path
  git pull
  pip install -r requirements.txt --upgrade
  pip install -r requirements.txt
}


function ApplicationHelp () {
  echo "usage:"
  echo "	-c,--client.		Install Client Version."
  echo "	-s,--server.		  Install Server Version."
  echo "	-u,--update.		Command git pull to update."
}

case $* in
  --client|-c)
    ApplicationInstallClient
  ;;
  --server|-s)
    ApplicationInstallServer
  ;;
  --update|-u)
    ApplicationUpdate
  ;;
  --help|-h)
    ApplicationHelp
  ;;
  *)
    ApplicationHelp
  ;;
  esac
exit 0
