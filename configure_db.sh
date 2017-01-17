#!/bin/bash

sudo docker run -it --rm --net container:cnode1 poklet/cassandra cqlsh -e "create keyspace demo with replication = {'class':'SimpleStrategy', 'replication_factor':2};"
sudo docker run -it --rm --net container:cnode1 poklet/cassandra cqlsh -k demo -e "create table data (field1 text, field2 text, user text, user_field1 text, user_field2 text, timestamp text, PRIMARY KEY (field1, user, timestamp));"
sudo docker run -it --rm --net container:cnode1 poklet/cassandra cqlsh -k demo -e "create table users (user text, user_field1 text, user_field2 text, data_field1 text, data_field2 text, timestamp text, PRIMARY KEY (user, data_field1, timestamp));"
#"insert into names (id, name) values (2, 'gibberish');"
