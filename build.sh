#!/bin/bash
docker-compose build
docker-compose up -d
sleep 30s
docker-compose ps
sleep 30s
docker-compose logs userssvc
#svc_status=$(docker-compose ps |  grep "userssvc" | awk '{ print $4}')
#echo $svc_status
#if [ "$svc_status" != "Up" ]
#then
#   echo "User service is not up"
#   exit 1
#fi
#port=$(docker-compose ps |  grep "userssvc" | awk '{ print $5}' | awk '{split($0,a,":"); print a[3] a[2]}' | awk '{split($0,a,"-"); print a[1]}')
port=5000
echo $port
curl -X PUT http://localhost:$port/user -H "Content-Type: application/json" -d '{"emailId":"pradeeep@abc.com","displayName":"Pradeep S","password":"test123"}'
#add_status=$(curl -s -o /dev/null -w "%{http_code}"  -X PUT -X PUT http://localhost:$port/user -H "Content-Type: application/json" -d '{"emailId":"pradeeep@abc.com","displayName":"Pradeep S","password":"test123"}' | grep "202")
#echo $add_status
#if [[ "$add_status" != "202" ]]
#then
#  echo "curl request failed for add user"
#  exit 1
#fi
curl http://localhost:$port/user
#status=$(curl -s --head --request GET http://localhost:$port/user | grep "200 OK")
#echo $status
#if [[ "$status" != *"200 OK"* ]]
#then
#  echo "curl request failed."
#  exit 1
#fi
docker images
