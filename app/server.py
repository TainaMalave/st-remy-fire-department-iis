from flask import Flask, render_template, redirect, url_for, request
import sqlite3 as sql
import base64
category_dropdown = ['Radio', 'PPE', 'Equipment', 'Air Pack', 'Personnel']


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


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
    conn = sql.connect('inventory.db')
    cursor = conn.cursor()

    if request.method == "POST":
        search = request.form['search']
        category = request.form['category_dropdown']

        if category == "Radio":
            columns = ["ID", "Type", "Make", "Model", "Serial Number", "Issued To",
                       "Date Issued", "Date of Purchase", "Accessories", "Notes", "Status"]

            radioSelect = "id, type, make,model,serialNum,issuedTo,dateIssued,dateOfPurchase,accessories,notes,status"

            if (search == "all" or len(search) == 0):
                cursor.execute("SELECT "+radioSelect+" FROM radio")
                conn.commit()
                data = cursor.fetchall()
                # print(data)
            else:
                search = "%" + search + "%"
                cursor.execute(
                    "SELECT "+radioSelect+" FROM radio WHERE id LIKE ? OR type LIKE ? OR make LIKE ? or model LIKE ? OR serialNum LIKE ? or issuedTo LIKE ? OR dateOfPurchase LIKE ? OR accessories LIKE ? OR notes LIKE ?")
                conn.commit()
                data = cursor.fetchall()

            """ for line in data:
                outputLine = []
                for col in line:
                    outputLine.append(col)

                outputLine[1] = "<img src='data:image/jpeg:base64," + \
                    base64.b64encode(outputLine[1].encode(
                        "ascii")).decode("ascii") + "'>"
                outputLine[11] = "<img src='data:image/jpeg:base64," + \
                    base64.b64encode(outputLine[11].encode(
                        "ascii")).decode("ascii") + "'>"
                output.append(outputLine) """

        try:
            return render_template('search.html', data=data, columns=columns, category=category, category_dropdown=category_dropdown)
        except:
            return render_template('search.html', category_dropdown=category_dropdown)
    return render_template('search.html', category_dropdown=category_dropdown)


"""         if (inventory == 'all' or len(inventory) == 0) and categories == 'all':
            cursor.execute("SELECT * from sampleData")
            conn.commit()
            data = cursor.fetchall()
        elif (inventory == 'all' or len(inventory) == 0):
            cursor.execute(
                'SELECT * FROM sampleData WHERE CATEGORY = ?', (categories,))
            print(categories)
            conn.commit()
            data = cursor.fetchall()
        elif categories == 'all':
            inventory = "%" + inventory + "%"
            cursor.execute('SELECT * FROM sampleData WHERE ' + whereSQL, (inventory, inventory,
                           inventory, inventory, inventory, inventory, inventory, inventory, inventory, inventory,))
            conn.commit()
            data = cursor.fetchall()
        else:
            inventory = "%" + inventory + "%"
            cursor.execute('SELECT * FROM sampleData WHERE' + whereSQL + 'AND CATEGORY = ?', (inventory, inventory,
                           inventory, inventory, inventory, inventory, inventory, inventory, inventory, inventory, categories))
            conn.commit()
            data = cursor.fetchall() """


def convertToBinaryData(file):
    return file.read()


@app.route("/dbEntry", methods=['GET', 'POST'])
def dbEntry():
    conn = sql.connect('inventory.db')
    cursor = conn.cursor()

    # Creating the drop down list for categories.

    if request.method == "POST":
        category = request.form["category_dropdown"]

        if category == "Radio":
            cursor.execute("INSERT INTO radio (id, barcode, type, make, model, serialNum, issuedTo, dateIssued, dateOfPurchase, accessories, notes, photo, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (request.form["id"], convertToBinaryData(request.files["barcode"]), request.form["type"], request.form[
                           "make"], request.form["model"], request.form["serialNum"], request.form["issuedTo"], request.form["dateIssued"], request.form["dateOfPurchase"], request.form["accessories"], request.form["notes"], convertToBinaryData(request.files["photo"]), request.form["status"]))
            conn.commit()
        elif category == "PPE":
            i = 1
        elif category == "Equipment":
            i = 1
        elif category == "Air Pack":
            i = 1
        elif category == "Personnel":
            i = 1

    return render_template('databaseEntry.html', category_dropdown=category_dropdown)


@app.route("/createDatabase", methods=['GET', 'POST'])
def createDatabase():
    conn = sql.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE radio (row BIGINT(20) PRIMARY KEY, id VARCHAR(20), barcode BIGBLOB, type VARCHAR(40), make VARCHAR(25), model VARCHAR(25), serialNum VARCHAR(35), issuedTo VARCHAR(35), dateIssued DATE, dateOfPurchase DATE, accessories TEXT, notes TEXT, photo BIGBLOB, status BIT)')

    conn.commit()

    cursor.execute(
        'CREATE TABLE ppe (row BIGINT(20) PRIMARY KEY, type VARCHAR(40), serialNum VARCHAR(35), dateOfManufacture DATE, issuedTo VARCHAR(35))')

    conn.commit()

    cursor.execute(
        'CREATE TABLE equipment (row BIGINT(20) PRIMARY KEY, type VARCHAR(40), make VARCHAR(25),  model VARCHAR(25), serialNum VARCHAR(35), issuedTo VARCHAR(35))')

    conn.commit()

    cursor.execute(
        'CREATE TABLE airpack (row BIGINT(20) PRIMARY KEY, serialNum VARCHAR(35), location TEXT)')

    conn.commit()

    cursor.execute('CREATE TABLE personnel (row BIGINT(20) PRIMARY KEY, name VARCHAR(35), rank VARCHAR(35), primaryRole VARCHAR(35), address TEXT, phone VARCHAR(12), email VARCHAR(50), emergencyContact VARCHAR(35), dateJoined DATE, certifications TEXT, dateOfLastPhysical DATE)')

    conn.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
