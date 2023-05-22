from flask import Flask, render_template
import data
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Главная", categories=data.categories)

@app.route("/category/<int:id>/")
def category(id):
    return render_template("category.html", category=data.get_category(id), products=data.get_category_products(id))

@app.route("/product/<int:id>/")
def product(id):
    return render_template("product.html", product=data.get_product(id))

if __name__ == "__main__":
    app.run(debug=True)