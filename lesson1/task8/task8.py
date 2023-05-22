from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Главная")

@app.route("/about/")
def about():
    return render_template("about.html", title = "О нас")

@app.route("/contacts/")
def contacts():
    return render_template("contacts.html", title = "Контакты" )

if __name__ == "__main__":
    app.run()
