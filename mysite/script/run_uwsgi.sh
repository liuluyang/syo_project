#!/bin/bash
#!/bin/bash
### BEGIN INIT INFO
# Provides:          PythonFuzzyMatching
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: PythonFuzzyMatching service
# Description:       PythonFuzzyMatching service
### END INIT INFO

#filepath="/home/watchtime.py"

start(){
    uwsgi --ini /var/www/mysite/script/uwsgi.ini
    echo 'mysite uwsgi service OK'
}

stop(){
    uwsgi --stop /var/www/mysite/script/uwsgi.pid
    echo 'mysite uwsgi service stop OK'
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
    sleep 2
    start
    ;;
  *)
    echo "Usage: mysite {start|stop|restart}"
    exit 1
esac
exit 0
