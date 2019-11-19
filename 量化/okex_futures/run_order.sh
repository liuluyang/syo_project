#!/bin/bash


filepath="/root/okex_futures/sar_process_3.py"

start(){
    nohup python $filepath>/dev/null 2>&1 &
    echo 'trans service OK'
}

stop(){
    serverpid=`ps -aux|grep "$filepath"|grep -v grep|awk '{print $2}'`
    echo $serverpid
    kill -9 $serverpid
    echo 'trans stop OK'
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
    echo "Usage: exchange {start|stop|restart}"
    exit 1
esac
exit 0
