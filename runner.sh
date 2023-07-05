#! /bin/bash
export PYTHONPATH=`pwd`

echo "Enter command (server/client)"
read action
if [ $action = "server" ]
then
  python server/main.py
else
  python client/main.py
fi