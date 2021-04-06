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

        if category == "PPE":
            columns = ["Type", "Serial Number",
                       "Date of Manufacture", "Issued To"]
            ppe_select = "type, serialNum, dateOfManufacture, issuedTo"

            if (search == "all" or len(search) == 0):
                cursor.execute("SELECT "+ppe_select+" FROM ppe")
                conn.commit()
                data = cursor.fetchall()
                # print(data)
            else:
                search = "%" + search + "%"
                cursor.execute(
                    "SELECT "+ppe_select+" FROM ppe WHERE type LIKE ? OR serialNum LIKE ? OR dateOfManufacture LIKE ? OR issuedTo LIKE ?")
                conn.commit()
                data = cursor.fetchall()

        if category == "Equipment":
            columns = ["Type", "Make", "Model", "Serial Number", "Issued To"]
            equipment_select = "type, make, model, serialNum, issuedTo"

            if (search == "all" or len(search) == 0):
                cursor.execute("SELECT "+equipment_select+" FROM equipment")
                conn.commit()
                data = cursor.fetchall()
                # print(data)
            else:
                search = "%" + search + "%"
                cursor.execute(
                    "SELECT "+equipment_select+" FROM equipment WHERE type LIKE ? OR make LIKE ? OR model LIKE ? OR serialNum LIKE ? OR issuedTo LIKE ?")
                conn.commit()
                data = cursor.fetchall()

        if category == "Air Pack":
            columns = ["Serial Number", "Location"]
            airpack_select = "serialNum, location"

            if (search == "all" or len(search) == 0):
                cursor.execute("SELECT "+airpack_select+" FROM airpack")
                conn.commit()
                data = cursor.fetchall()
                # print(data)
            else:
                search = "%" + search + "%"
                cursor.execute(
                    "SELECT "+airpack_select+" FROM airpack WHERE serialNum LIKE ? OR location LIKE ?")
                conn.commit()
                data = cursor.fetchall()

        if category == "Personnel":
            columns = ["Name", "Rank", "Primary Role", "Address", "Phone", "Email",
                       "Emergency Contact", "Date Joined", "Certifications", "Date of Last Physical"]
            personnel_select = "name, rank, primaryRole, address, phone, email, emergencyContact, dateJoined, certifications, dateOfLastPhysical"

            if (search == "all" or len(search) == 0):
                cursor.execute("SELECT "+personnel_select+" FROM personnel")
                conn.commit()
                data = cursor.fetchall()
                # print(data)
            else:
                search = "%" + search + "%"
                cursor.execute(
                    "SELECT "+personnel_select+" FROM personnel WHERE name LIKE ? OR rank LIKE ? OR primaryROLE LIKE ? OR address LIKE ? OR phone LIKE ? OR email LIKE ? OR emergencyContact LIKE ? OR dateJoined LIKE ? OR certifications LIKE ? OR dateOfLastPhyiscal LIKE ?")
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

    if request.method == "POST":
        category = request.form["category_dropdown"]

        if category == "Radio":
            cursor.execute("INSERT INTO radio (id, barcode, type, make, model, serialNum, issuedTo, dateIssued, dateOfPurchase, accessories, notes, photo, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (request.form["id"], convertToBinaryData(request.files["barcode"]), request.form["type"], request.form[
                           "make"], request.form["model"], request.form["serialNum"], request.form["issuedTo"], request.form["dateIssued"], request.form["dateOfPurchase"], request.form["accessories"], request.form["notes"], convertToBinaryData(request.files["photo"]), request.form["status"]))
            conn.commit()
        elif category == "PPE":
            cursor.execute("INSERT INTO ppe (type, serialNum, dateOfManufacture, issuedTo) VALUES (?,?,?,?)", (
                request.form["type"], request.form["serialNum"], request.form["dateOfManufacture"], request.form["issuedTo"]))
            conn.commit()
        elif category == "Equipment":
            cursor.execute("INSERT INTO equipment (type, make, model, serialNum, issuedTo) VALUES (?,?,?,?,?)", (
                request.form["type"], request.form["make"], request.form["model"], request.form["serialNum"], request.form["issuedTo"]))
            conn.commit()
        elif category == "Air Pack":
            cursor.execute("INSERT INTO airpack (serialNum, location) VALUES (?,?)", (
                request.form["serialNum"], request.form["location"]))
            conn.commit()
        elif category == "Personnel":
            cursor.execute("INSERT INTO personnel (name, rank, primaryRole, address, phone, email, emergencyContact, dateJoined, certifications, dateOfLastPhysical) VALUES (?,?,?,?,?,?,?,?,?,?)", (
                request.form["name"], request.form["rank"], request.form["primaryRole"], request.form["address"], request.form["phone"], request.form["email"], request.form["emergencyContact"], request.form["dateJoined"], request.form["certifications"], request.form["dateOfLastPhyiscal"]))
            conn.commit()

    return render_template('databaseEntry.html', category_dropdown=category_dropdown)


# Creating tables in the DB.
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
