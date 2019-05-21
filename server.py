from flask import Flask, request
from flask_restplus import Resource, Api, fields, cors
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)
api = Api(app)

newspaper = api.model('news', {
    'title': fields.String(required=True, description='title'),
    'description': fields.String(required=True, description='user username'),
    'author': fields.String(required=True, description='user password')
})

db = yaml.load(open("db.yaml"))
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]

mysql = MySQL(app)

@api.route('/newspapers')
class NewsPapapers(Resource):

    def __convertToJson(self, objectList):
        result = []
        for value in objectList:
            result.append({
            "id": value[0],
            "title": value[1],
            "description": value[2],
            "author": value[3]
            })
        return result

    def get(self):
        cur = mysql.connection.cursor()
        query = "SELECT * FROM newspaper"
        newspapers = cur.execute(query)
        newspapersDetails = cur.fetchall()
        print(newspapersDetails)
        result = self.__convertToJson(newspapersDetails)
        return result , 200 , {'Access-Control-Allow-Origin': '*'}

    @cors.crossdomain(origin='*')
    def post(self):
        data = request.json
        cur = mysql.connection.cursor()
        query = "INSERT INTO newspaper(title, description, author) values ('%s', '%s', '%s');" % (data['title'], data['description'], data['author'])
        cur.execute(query)
        print(query)
        mysql.connection.commit()
        cur.close()
        return "success", 200

@api.route('/newspapers/<int:id>')
class NewsPapapersById(Resource):

    @cors.crossdomain(origin='*')
    def delete(self, id):
        cur = mysql.connection.cursor()
        query = "DELETE FROM newspaper WHERE id=%s" % (id)
        cur.execute(query)
        print(query)
        mysql.connection.commit()
        cur.close()
        return "success", 200

    def get(self, id):
        cur = mysql.connection.cursor()
        query = "SELECT * FROM newspaper WHERE id=%s" % (id)
        newspapers = cur.execute(query)
        newspapersDetails = cur.fetchone()
        print(newspapersDetails)
        mysql.connection.commit()
        cur.close()
        resp = dict(name='bob smith')
        return {
                "id": newspapersDetails[0],
                "title": newspapersDetails[1],
                "description": newspapersDetails[2],
                "author": newspapersDetails[3]
                } , 200  , {'Access-Control-Allow-Origin': '*'}

    @cors.crossdomain(origin='*')
    def put(self, id):
        data = request.json
        cur = mysql.connection.cursor()
        query = "UPDATE newspaper set title='%s' , description='%s' , author='%s' where id=%s" % (data['title'], data['description'], data['author'], id)
        cur.execute(query)
        print(query)
        mysql.connection.commit()
        cur.close()
        return "success", 200

if __name__ == '__main__':
    app.run(debug=True)
