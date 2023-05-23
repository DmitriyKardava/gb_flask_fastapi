from flask import Flask, render_template
import data
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Главная", categories=data.categories)


@app.route("/category/<int:category_id>/")
def category(category_id):
    return render_template("category.html",
                           category=data.get_category(category_id),
                           products=data.get_category_products(category_id))


@app.route("/product/<int:product_id>/")
def product(product_id):
    return render_template("product.html", product=data.get_product(product_id))


if __name__ == "__main__":
    app.run(debug=True)
