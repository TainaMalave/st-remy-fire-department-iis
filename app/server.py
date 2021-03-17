from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

""" @app.route("/login")
def login():
    return render_template('login.html') """


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)