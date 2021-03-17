from flask import Flask, render_template, redirect, url_for, request
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

# Database information -> will more to separate file later
""" DB = 'sampleDB.db'
conn = sql.connect('sampleDb.db')
cursor = conn.cursor()
 """
# new login route that should redirect to search/enter page after login
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password123':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('searchOrEntry'))
    return render_template('login.html', error=error)

@app.route("/searchOrEntry")
def searchOrEntry():
    return render_template('searchOrEntry.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    conn = sql.connect('sampleData.db')
    cursor = conn.cursor()
    if request.method == "POST":
        inventory = request.form['inventory']
        # search by ID or issued too
        cursor.execute('SELECT * FROM sampleData WHERE ID LIKE ?', (inventory,))
        conn.commit()
        data = cursor.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0 and inventory == 'all': 
            cursor.execute("SELECT * from sampleData")
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)