#!/bin/bash

for cont in `sudo docker ps -q` ; do
    sudo docker kill $cont
done
#sudo docker kill cnode1
#sudo docker kill cnode2

sudo docker rm `sudo docker ps -qa`
