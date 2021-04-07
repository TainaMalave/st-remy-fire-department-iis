from flask import Flask, render_template, redirect, url_for, request
import sqlite3 as sql
import base64
import json


class model:
    @staticmethod
    def get_db():
        conn = sql.connect('inventory.db')
        cursor = conn.cursor()
        return conn, cursor

    def get_columns(self):
        conn, cursor = model.get_db()
        cursor.execute("PRAGMA TABLE_INFO ("+self.table_name+")")
        conn.commit()
        data = cursor.fetchall()

        columns = []
        for column in data:
            columns.append(column[1])
        return columns

    def handle_record(self, record):
        columns = self.get_columns()
        definition_columns = self.get_defintion_columns()
        item = {}
        new_record = []
        for j in range(len(record)):
            field = record[j]
            column = columns[j]
            if column in definition_columns:
                definition_column = definition_columns[column]
                if definition_column["type"] == "image":
                    if field is not None:
                        item[column] = "<img src='data:image/png;charset=utf-8;base64, " + \
                            base64.b64encode(field).decode('ascii') + "'/>"
                    else:
                        item[column] = "thats sad man :,("
                elif definition_column["type"] == "link":
                    url = "/details?row=" + \
                        str(item["row"]) + "&category=" + self.category
                    item[column] = "<a href='" + \
                        url + "'>" + field + "</a>"
                else:
                    item[column] = field
                new_record.append(item[column])
            else:
                item[column] = field
        return new_record, item

    def handle_records(self, records):
        columns = self.get_columns()
        definition_columns = self.get_defintion_columns()
        result = []
        new_records = []
        for i in range(len(records)):
            record = records[i]
            new_record, item = self.handle_record(record)
            result.append(item)
            new_records.append(new_record)
        return new_records, result

    def get_defintion_columns(self):
        columns = {}
        for column in self.definition:
            columns[column["column"]] = column
        return columns

    def get_record_where(self, where_clause, tuple):
        conn, cursor = self.get_db()
        cursor.execute("SELECT * FROM " + self.table_name +
                       " WHERE " + where_clause, tuple)
        conn.commit()
        return self.handle_record(cursor.fetchone())

    def get_records(self):
        conn, cursor = self.get_db()
        cursor.execute("SELECT * FROM " + self.table_name)
        conn.commit()
        return self.handle_records(cursor.fetchall())

    definition = []
    table_name = ""
    category = ""


class radio_model(model):
    table_name = "radio"
    category = "radio"
    definition = [{"column": "id", "type": "link", "header": "ID"},
                  {"column": "barcode", "type": "image", "header": "Barcode"},
                  {"column": "type", "type": "string", "header": "Type"},
                  {"column": "make", "type": "string", "header": "Make"},
                  {"column": "model", "type": "string", "header": "Model"},
                  {"column": "serialNum", "type": "string",
                      "header": "Serial Number"},
                  {"column": "issuedTo", "type": "string", "header": "Issued To"},
                  {"column": "dateIssued", "type": "date", "header": "Date Issued"},
                  {"column": "dateOfPurchase", "type": "date",
                      "header": "Date of Purchase"},
                  {"column": "accessories", "type": "string",
                      "header": "Accessories"},
                  {"column": "notes", "type": "text", "header": "Notes"},
                  {"column": "photo", "type": "image", "header": "Photo"},
                  {"column": "status", "type": "boolean", "header": "Status"}, ]

    def search_records(self, search):
        conn, cursor = self.get_db()
        search = "%" + search + "%"
        cursor.execute("SELECT * FROM radio WHERE id LIKE ? OR type LIKE ? OR make LIKE ? or model LIKE ? OR serialNum LIKE ? or issuedTo LIKE ? OR dateOfPurchase LIKE ? OR accessories LIKE ? OR notes LIKE ?",
                       (search, search, search, search, search, search, search, search, search,))
        conn.commit()
        return self.handle_records(cursor.fetchall())


class personnel_model(model):
    table_name = "personnel"
    category = "personnel"
    definition = [{"column": "name", "type": "string", "header": "Name"},
                  {"column": "rank", "type": "string", "header": "Rank"},
                  {"column": "primaryRole", "type": "string",
                      "header": "Primary Role"},
                  {"column": "address", "type": "text", "header": "Adress"},
                  {"column": "phone", "type": "string", "header": "Phone"},
                  {"column": "email", "type": "string", "header": "Email"},
                  {"column": "emergencyContact", "type": "string",
                      "header": "Emergency Contact"},
                  {"column": "dateJoined", "type": "date", "header": "Date Joined"},
                  {"column": "certifications", "type": "text",
                      "header": "Certifications"},
                  {"column": "dateOfLastPhysical", "type": "date",
                      "header": "Date of Last Physical"},
                  {"column": "photo", "type": "image", "header": "Photo"}, ]

    def search_records(self, search):
        search = "%" + search + "%"
        cursor.execute("SELECT * FROM personnel WHERE name LIKE ? OR rank LIKE ? OR primaryROLE LIKE ? OR address LIKE ? OR phone LIKE ? OR email LIKE ? OR emergencyContact LIKE ? OR dateJoined LIKE ? OR certifications LIKE ? OR dateOfLastPhysical LIKE ?",
                       (search, search, search, search, search, search, search, search, search, search,))
        conn.commit()
        return self.handle_records(cursor.fetchall())


model_radio = radio_model()
model_personnel = personnel_model()

category_definition = {
    "Radio": model_radio.definition,
    "PPE": [
        {"column": "type", "type": "string"},
        {"column": "serialNum", "type": "string"},
        {"column": "dateOfManufacture", "type": "date"},
        {"column": "issuedTo", "type": "string"},
    ],
    "Equipment": [
        {"column": "type", "type": "string"},
        {"column": "make", "type": "string"},
        {"column": "model", "type": "string"},
        {"column": "serialNum", "type": "string"},
        {"column": "issuedTo", "type": "string"},
    ],
    "Air Pack": [
        {"column": "serialNum", "type": "string"},
        {"column": "location", "type": "text"},
    ],
    "Personnel": model_personnel.definition
}


def get_category_names():
    return category_definition.keys()


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
        search_all = (search == "all" or len(search) == 0)
        output = []

        if category == "Radio":
            data, records = model_radio.get_records(
            ) if search_all else model_radio.search_records(search)

        if category == "PPE":
            ppe_select = "type, serialNum, dateOfManufacture, issuedTo"

            if (search == "all" or len(search) == 0):
                cursor.execute("SELECT "+ppe_select+" FROM ppe")
                conn.commit()
                data = cursor.fetchall()
            else:
                search = "%" + search + "%"
                cursor.execute(
                    "SELECT "+ppe_select+" FROM ppe WHERE type LIKE ? OR serialNum LIKE ? OR dateOfManufacture LIKE ? OR issuedTo LIKE ?")
                conn.commit()
                data = cursor.fetchall()

        if category == "Equipment":
            equipment_select = "type, make, model, serialNum, issuedTo"

            if (search == "all" or len(search) == 0):
                cursor.execute("SELECT "+equipment_select+" FROM equipment")
                conn.commit()
                data = cursor.fetchall()
            else:
                search = "%" + search + "%"
                cursor.execute(
                    "SELECT "+equipment_select+" FROM equipment WHERE type LIKE ? OR make LIKE ? OR model LIKE ? OR serialNum LIKE ? OR issuedTo LIKE ?")
                conn.commit()
                data = cursor.fetchall()

        if category == "Air Pack":
            airpack_select = "serialNum, location"

            if (search == "all" or len(search) == 0):
                cursor.execute("SELECT "+airpack_select+" FROM airpack")
                conn.commit()
                data = cursor.fetchall()
            else:
                search = "%" + search + "%"
                cursor.execute(
                    "SELECT "+airpack_select+" FROM airpack WHERE serialNum LIKE ? OR location LIKE ?")
                conn.commit()
                data = cursor.fetchall()

        if category == "Personnel":
            data, records = model_personnel.get_records(
            ) if search_all else model_personnel.search_records(search)

        try:
            return render_template('search.html', data=data, category=category, category_definition=category_definition, category_dropdown=get_category_names())
        except:
            return render_template('search.html', category_dropdown=get_category_names(), category_definition=category_definition, category=category)
    return render_template('search.html', category_definition=category_definition, category_dropdown=get_category_names(), category=category)


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
            cursor.execute("INSERT INTO personnel (name, rank, primaryRole, address, phone, email, emergencyContact, dateJoined, certifications, dateOfLastPhysical, photo) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                request.form["name"], request.form["rank"], request.form["primaryRole"], request.form["address"], request.form["phone"], request.form["email"], request.form["emergencyContact"], request.form["dateJoined"], request.form["certifications"], request.form["dateOfLastPhyiscal"], convertToBinaryData(request.files["photo"])))
            conn.commit()

    return render_template('databaseEntry.html', category_dropdown=get_category_names(), category_definition=json.dumps(category_definition))


@app.route("/details", methods=['GET'])
def show_details():
    conn = sql.connect('inventory.db')
    cursor = conn.cursor()
    row = request.args.get('row')
    category = request.args.get('category')
    left_column = {}
    right_column = {}

    if category == 'radio':
        record, item = model_radio.get_record_where("row = ?", (row))
        model_definition = model_radio.get_defintion_columns()
        keys = item.keys()
        for column in keys:
            if column in model_definition:
                column_definition = model_definition[column]
                if column_definition["type"] == "image":
                    right_column[column_definition["header"]] = item[column]
                else:
                    left_column[column_definition["header"]] = item[column]
    if category == 'personnel':
        record, item = model_personnel.get_record_where("row = ?", (row))
        model_definition = model_personnel.get_defintion_columns()
        keys = item.keys()
        for column in keys:
            if column in model_definition:
                column_definition = model_definition[column]
                if column_definition["type"] == "image":
                    right_column[column_definition["header"]] = item[column]
                else:
                    left_column[column_definition["header"]] = item[column]
    return render_template('details.html', left_column=left_column, right_column=right_column)


# Creating tables in the DB.
schema_version = 0


@app.route("/createDatabase", methods=['GET', 'POST'])
def createDatabase():
    conn = sql.connect('inventory.db')
    cursor = conn.cursor()

    if schema_version == -1:
        cursor.execute("DROP TABLE radio")
        conn.commit()
        cursor.execute("DROP TABLE ppe")
        conn.commit()
        cursor.execute("DROP TABLE equipment")
        conn.commit()
        cursor.execute("DROP TABLE airpack")
        conn.commit()
        cursor.execute("DROP TABLE personnel")
        conn.commit()
    if schema_version == 0:
        cursor.execute('CREATE TABLE radio (row INTEGER PRIMARY KEY AUTOINCREMENT, id VARCHAR(20), barcode BIGBLOB, type VARCHAR(40), make VARCHAR(25), model VARCHAR(25), serialNum VARCHAR(35), issuedTo VARCHAR(35), dateIssued DATE, dateOfPurchase DATE, accessories TEXT, notes TEXT, photo BIGBLOB, status BIT)')

        conn.commit()

        cursor.execute(
            'CREATE TABLE ppe (row INTEGER PRIMARY KEY AUTOINCREMENT, type VARCHAR(40), serialNum VARCHAR(35), dateOfManufacture DATE, issuedTo VARCHAR(35))')

        conn.commit()

        cursor.execute(
            'CREATE TABLE equipment (row INTEGER PRIMARY KEY AUTOINCREMENT, type VARCHAR(40), make VARCHAR(25),  model VARCHAR(25), serialNum VARCHAR(35), issuedTo VARCHAR(35))')

        conn.commit()

        cursor.execute(
            'CREATE TABLE airpack (row INTEGER PRIMARY KEY AUTOINCREMENT, serialNum VARCHAR(35), location TEXT)')

        conn.commit()

        cursor.execute('CREATE TABLE personnel (row INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(35), rank VARCHAR(35), primaryRole VARCHAR(35), address TEXT, phone VARCHAR(12), email VARCHAR(50), emergencyContact VARCHAR(35), dateJoined DATE, certifications TEXT, dateOfLastPhysical DATE, photo BIGBLOB)')

        conn.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
