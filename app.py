from flask import Flask, render_template
from flaskext.mysql import MySQL
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'results'

mysql = MySQL()
mysql.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users')
def users():
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("SELECT * FROM scores")
    if resultValue > 0:
        userDetails = cur.fetchall()
        scores = [user[1] for user in userDetails]
        students = [user[0] for user in userDetails]
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Bar(x=students, y=scores), row=1, col=1)
        fig.update_layout(title='Student Scores', xaxis_title='Students', yaxis_title='Score')
        graph_div = fig.to_html(full_html=False)
        return render_template('users.html', userDetails=userDetails, graph_div=graph_div)



if __name__ == '__main__':
    app.run(debug=True)
