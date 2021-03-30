from flask import Flask, render_template, redirect, url_for, request
import sqlite3 as sql
conn = sql.connect('sampleData.db')
cursor = conn.cursor()

alttable = 'UPDATE sampleData SET category = "Power Supply" WHERE ID LIKE "PWRSP1"'
cursor.execute(alttable)
conn.commit()

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
        cursor.execute('SELECT DISTINCT category FROM sampleData WHERE ID != "ID #"')
        conn.commit()
        category = cursor.fetchall()

        inventory = request.form['inventory']
        categories = request.form['categories']
        whereSQL = "(ID LIKE ? OR Type LIKE ? OR Manufacturer LIKE ? OR Model LIKE ? OR Serial LIKE ? OR IssuedTo LIKE ? OR DateIssued LIKE ? OR DatePurchased LIKE ? OR Accessories LIKE ? OR Status like ?)"
        # all in the search box will return all the tuples
        if (inventory == 'all' or len(inventory) == 0) and categories == 'all':
            cursor.execute("SELECT * from sampleData")
            conn.commit()
            data = cursor.fetchall()
        elif (inventory == 'all' or len(inventory) == 0):
            cursor.execute('SELECT * FROM sampleData WHERE CATEGORY = ?', (categories,))
            print(categories)
            conn.commit()
            data = cursor.fetchall()
        elif categories == 'all':
            inventory = "%" + inventory + "%"
            cursor.execute('SELECT * FROM sampleData WHERE ' + whereSQL, (inventory, inventory,inventory,inventory,inventory,inventory,inventory,inventory,inventory,inventory,))
            conn.commit()
            data = cursor.fetchall()
        else:
            inventory = "%" + inventory + "%"
            cursor.execute('SELECT * FROM sampleData WHERE' + whereSQL + 'AND CATEGORY = ?', (inventory,inventory,inventory,inventory,inventory,inventory,inventory,inventory,inventory,inventory, categories))
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data, category=category)
    return render_template('search.html')


@app.route("/dbEntry", methods=['GET', 'POST'])
def dbEntry():
    conn = sql.connect('sampleData.db')
    cursor = conn.cursor()

    if request.method == "POST":
        id = request.form['id']
        type = request.form['type']
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        serial = request.form['serial']
        issuedTo = request.form['issued-to']
        dateIssued = request.form['date-issued']
        datePurchased = request.form['date-purchased']
        accessories = request.form['accessories']
        status = request.form['status']
        category = request.form['category']

        cursor.execute('INSERT INTO sampleData (ID, Type, Manufacturer, Model, Serial, IssuedTo, DateIssued, DatePurchased, Accessories, Status, category) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (id,type,manufacturer,model,serial,issuedTo,dateIssued,datePurchased,accessories, status,category))
        
        conn.commit()

    return render_template('databaseEntry.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)