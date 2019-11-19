#!/bin/bash


filepath="/root/exchange_new/main_futures.py"

start(){
    nohup python $filepath>/dev/null 2>&1 &
    echo 'futures service OK'
}

stop(){
    serverpid=`ps -aux|grep "$filepath"|grep -v grep|awk '{print $2}'`
    echo $serverpid
    kill -9 $serverpid
    echo 'futures stop OK'
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
    echo "Usage: futures {start|stop|restart}"
    exit 1
esac
exit 0
