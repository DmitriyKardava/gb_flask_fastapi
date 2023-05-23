from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("email_form.html")


@app.post("/submit")
def submit_email():
    context = {"name": request.form.get('name'), "email": request.form.get('email')}
    response = make_response(render_template('greetings.html', **context))
    response.set_cookie('username', context['name'])
    response.set_cookie('email', context['email'])
    return response


@app.post("/logout")
def logout():
    response = make_response(redirect(url_for("index")))
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


if __name__ == "__main__":
    app.run(debug=True)
