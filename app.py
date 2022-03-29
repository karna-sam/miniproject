from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import sqlite3 as sql


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class User(db.Model):
    """Create user table"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/", methods=["GET", "POST"])
def home():
    """Session control"""
    if not session.get("logged_in"):
        return render_template("index.html")
    else:
        if request.method == "POST":
            return render_template("index.html")
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Form"""
    if request.method == "GET":
        return render_template("login.html")
    else:
        name = request.form["username"]
        passw = request.form["password"]
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session["logged_in"] = True
                return redirect(url_for("home1"))
            else:
                return "Invalid Credentials"
        except:
            return "Invalid Credentials"


@app.route("/register/", methods=["GET", "POST"])
def register():
    """Register Form"""
    if request.method == "POST":
        new_user = User(
            username=request.form["username"], password=request.form["password"]
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html")
    return render_template("register.html")


@app.route("/logout")
def logout():
    """Logout Form"""
    session["logged_in"] = False
    return redirect(url_for("home"))


@app.route("/home")
def home1():
    return render_template("home.html")



    # stock balance
@app.route("/stockbalance")
def Stockbalance():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Product")

    rows = cur.fetchall()
    return render_template("stock.html", rows=rows)


con = sql.connect(
    "database.db", check_same_thread=False
)  # con is a variable and sql.connect is used to connect the test(BASICALLY CONNECTION)
con.row_factory = sql.Row  # when queriying instead of tuples, objects are returned
cur = (
    con.cursor()
)  # cur is a object which can further be used with methods like execute


# stock balance
@app.route("/stockbalance")
def Stockbalance1():
    con = sql.connect("database.db")  # connecting DB
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Product")  # executes the query
    rows = cur.fetchall()  # returns all the rows in list type
    return render_template("stock.html", rows=rows)


# Product Page
@app.route("/Product")
def Product():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from Product")

    rows = cur.fetchall()  # returns all the rows in list type
    return render_template("Product.html", rows=rows)


# ADD Product
@app.route("/addProduct", methods=["POST"])  # POST=sends the data to DB/server
def addProduct():
    if request.method == "POST":
        try:
            pn = request.form["pn"]  # accepts product name
            pd = request.form["pd"]  # accepts product description
            pq = request.form["pq"]  # accepts product quantity

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO Product (productName,productDescription,QTY) VALUES (?,?,?)",
                    (pn, pd, pq),
                )

                con.commit()  # saves all changes to DB
                msg = "Record added"  # display a message
        except:
            con.rollback()  # return the DB to previous state
            msg = "error in  operation"

        finally:

            return redirect(
                url_for("Product") + "?msg=" + msg
            )  # redirects to the products page with message msg
            con.close()  # close the connection


# Edit Product
@app.route("/editProduct", methods=["POST"])
def editProduct():
    if request.method == "POST":
        try:
            productID = request.form["ProductID"]  # for this product ID
            productName = request.form["NEWProductName"]  # accepts all the data
            productDescription = request.form["NEWProductDescription"]
            ProductQty = request.form["NEWProductQty"]
            cur.execute(
                "UPDATE Product SET productName = ?,productDescription = ?, QTY = ? WHERE productID = ?",
                (productName, productDescription, ProductQty, productID),
            )  # update query

            con.commit()
            msg = "Product Edited "
        except:
            con.rollback()
            msg = "error in operation"

        finally:
            return redirect(
                url_for("Product") + "?msg=" + msg
            )  # redirect to the products page with msg
            con.close()

        # Delete Product


@app.route("/deleteProduct/<productID>")  # for the productID
def deleteProduct(productID):
    try:
        cur.execute(
            "DELETE FROM Product WHERE productID = ?", (productID,)
        )  # delete query

        con.commit()
        msg = "Product Deleted"
    except:
        con.rollback()
        msg = "error in operation"

    finally:
        return redirect(
            url_for("Product") + "?msg=" + msg
        )  # redirect to product page with msg
        con.close()

        # Location Page


@app.route("/Location")
def Location():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from locations")

    rows = cur.fetchall()
    return render_template("Location.html", rows=rows)

    # ADD Locations


@app.route("/addlocation", methods=["POST"])
def addlocation():
    if request.method == "POST":
        try:
            ln = request.form["ln"]

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO locations (locationName) VALUES (?)", (ln,))

                con.commit()
                msg = "successfully added"
        except:
            con.rollback()
            msg = "error in operation"

        finally:
            return redirect(url_for("Location") + "?msg=" + msg)
            con.close()

            # Edit Location


@app.route("/editlocation", methods=["POST"])
def editlocation():
    if request.method == "POST":
        try:
            locationID = request.form["locationID"]
            locationName = request.form["NEWLocationName"]
            cur.execute(
                "UPDATE locations SET locationName = ? WHERE locationID = ?",
                (locationName, locationID),
            )

            con.commit()
            msg = "location Edit Successfully"
        except:
            con.rollback()
            msg = "error operation"

        finally:
            return redirect(url_for("Location") + "?msg=" + msg)
            con.close()

            # Delete Location


@app.route("/deletelocation/<locationID>")
def deletelocation(locationID):
    try:
        cur.execute("DELETE FROM locations WHERE locationID = ? ", (locationID))

        con.commit()
        msg = "location Delete Successfully"
    except:
        con.rollback()
        msg = "error operation"

    finally:
        return redirect(url_for("Location") + "?msg=" + msg)
        con.close()


# Product movement


@app.route("/ProductMovement")
def ProductMovement():
    cur.execute("select * from product_movement")

    rows = cur.fetchall()

    cur.execute("select * from Stockbalance")
    productRows = cur.fetchall()

    cur.execute("select * from locations")
    locationRows = cur.fetchall()

    for pr in productRows:
        for lr in locationRows:
            cur.execute(
                "SELECT * FROM Balance WHERE locationName = ? AND productName = ? ",
                (lr["locationName"], pr["productName"]),
            )
            data = cur.fetchall()

            if len(data) == 0:
                cur.execute(
                    "INSERT INTO Balance (locationName, productName, qty)VALUES (?,?,?)",
                    (lr["locationName"], pr["productName"], 0),
                )
                con.commit()

    return render_template(
        "ProductMovement.html",
        rows=rows,
        productRows=productRows,
        locationRows=locationRows,
    )

    # ADD ProductMovement


@app.route("/addProductMovement", methods=["POST"])
def addProductMovement():
    if request.method == "POST":
        try:
            pn = request.form["pn"]
            datetime = request.form["datetime"]
            fromlocation = request.form["fromlocation"]
            tolocation = request.form["tolocation"]
            pq = request.form["pq"]

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO product_movement (productName,Timing,fromlocation,tolocation,QTY) VALUES (?,?,?,?,?)",
                    (pn, datetime, fromlocation, tolocation, pq),
                )

                con.commit()
                msg = "Record added"
        except:
            con.rollback()
            msg = "error in  operation"

        finally:
            return redirect(url_for("ProductMovement") + "?msg=" + msg)
            con.close()

            # Edit ProductMovement


@app.route("/editProductMovement", methods=["POST"])
def editProductMovement():
    if request.method == "POST":
        try:
            movementID = request.form["movementID"]
            ProductName = request.form["NEWProductName"]
            datetime = request.form["NEWDateTime"]
            fromlocation = request.form["NEWfromlocation"]
            tolocation = request.form["NEWtolocation"]
            qty = request.form["NEWProductQty"]
            cur.execute(
                "UPDATE product_movement SET productName = ?,Timing = ?,fromlocation = ?,tolocation = ?,QTY = ? WHERE movementID = ?",
                (ProductName, datetime, fromlocation, tolocation, qty, movementID),
            )

            con.commit()
            msg = " movement Edit Successfully"
        except:
            con.rollback()
            msg = "error operation"

        finally:
            return redirect(url_for("ProductMovement") + "?msg=" + msg)
            con.close()

            # Delete Product Movement


@app.route("/deleteprouctmovement/<movementID>")
def deleteprouctmovement(movementID):
    try:
        cur.execute("DELETE FROM product_movement WHERE movementID = ? ", (movementID))

        con.commit()
        msg = "movement Delete Successfully"
    except:
        con.rollback()
        msg = "error operation"

    finally:
        return redirect(url_for("ProductMovement") + "?msg=" + msg)
        con.close()


if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host="0.0.0.0")
