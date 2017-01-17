#!/bin/bash
#sudo docker network create --subnet=172.18.0.0/16 cassandra_net
#sudo docker run --name cnode1 --net cassandra_net --ip 172.18.0.2/16 -d cassandra
#sudo docker run --name cnode2 --net cassandra_net --ip 172.18.0.3/16 -d -e CASSANDRA_SEEDS="$(docker inspect --format='{{ .NetworkSettings.IPAddress }}' cnode1)" cassandra

sudo docker run -d --name cnode1 poklet/cassandra start
if [[ $# < 1 ]] ; then
    exit
fi
COUNTER=$1
COUNTER=$(($COUNTER-1))
while [[ $COUNTER > 0 ]] ; do
    COUNTER=$(($COUNTER-1))
    sudo docker run -d --name cnode$(($1-$COUNTER)) --link cnode1:seed poklet/cassandra start seed
done
