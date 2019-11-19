#!/bin/bash


filepath="/root/exchange_new/main_remind.py"

start(){
    nohup python $filepath>/dev/null 2>&1 &
    echo 'remind service OK'
}

stop(){
    serverpid=`ps -aux|grep "$filepath"|grep -v grep|awk '{print $2}'`
    echo $serverpid
    kill -9 $serverpid
    echo 'remind stop OK'
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: remind {start|stop|restart}"
    exit 1
esac
exit 0
