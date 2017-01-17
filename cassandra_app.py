from flask import Flask
from cassandra.cluster import Cluster
import subprocess
import cassandra_utils

app = Flask(__name__)
cluster = Cluster(cassandra_utils.get_cluster('cnode'))

session = cluster.connect('demo')

def set_cluster(nodes):
    return Cluster(nodes)

@app.route('/user/<user>')
def get_per_user(user):
    nodes = subprocess.Popen('sudo docker run -it --rm --net container:cnode2 poklet/cassandra nodetool -h localhost getendpoints  demo users {user}'.format(user=user), shell=True, stdout=subprocess.PIPE).stdout.read().decode() 
    rows = session.execute('select * from users where user = \'{user}\';'.format(user=user))
    text = ''
    for row in rows:
        text += str(row.data_field1) + ", "
    return text + str(nodes)

@app.route('/data/<field>')
def get_per_data(field):
    nodes = subprocess.Popen('sudo docker run -it --rm --net container:cnode2 poklet/cassandra nodetool -h localhost getendpoints  demo data {field}'.format(field=field), shell=True, stdout=subprocess.PIPE).stdout.read().decode() 
    rows = session.execute('select * from data where field1 = \'{field}\';'.format(field=field))
    text = ''
    for row in rows:
        text += str(row.user) + ", "
    return text + str(nodes)

@app.route('/set/<user>/<field>')
def set_user(user, field):
    try:
        session.execute("insert into users (user, data_field1, timestamp) values ('%s', '%s', '%s');"%(user, field, "123"))
        session.execute("insert into data (field1, user, timestamp) values ('%s', '%s', '123');"%(field, user))
        return 'Inserted'
    except:
        return "Failed"


@app.route("/")
def test():
    return "Works"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
