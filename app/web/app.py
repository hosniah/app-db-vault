from flask import Flask, request, render_template
from flask import request

import MySQLdb as mdb
import sys


import hvac


app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/read')
def read():
    # Check https://github.com/ianunruh/hvac
    _vault_token = request.args.get('vault_token', 'no-token provide with vault_token=TOKEN')
    client = hvac.Client()
    client = hvac.Client(url='http://main-secrets:8200')
    client = hvac.Client(url='http://main-secrets:8200', token=_vault_token)

    client.write('secret/foo', baz='bar', lease='1h')
    print(client.read('secret/foo'))

    client.delete('secret/foo')
    return "Read! " + _vault_token


@app.route('/connect')
def connect():
    try:
        con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')

        cur = con.cursor()
        cur.execute("SELECT VERSION()")

        ver = cur.fetchone()

        print "Database version : %s " % ver

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:
        if con:
            con.close()


if __name__ == "__main__":
    print "Hello world"
    app.run(host="0.0.0.0", debug=True)
