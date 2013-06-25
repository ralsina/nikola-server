#!/bin/bash
case $1 in
   start)
      shift
      echo $$ > /home/alva/$1.pid;
      shift
      username=$1
      shift
      exec sudo -u $username $*
      ;;
    stop)  
      kill `cat /home/alva/$2.pid` ;;
    *)  
      echo "usage: xyz {start|stop}" ;;
esac
exit 0

