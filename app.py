import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from my_photo import check_photo_str, check_photo


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pfc.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# 3つ目
@app.route("/")
# @login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")

# 4つ目
@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """Post pictures of what I eat"""

    if request.method == "POST":
        # pictureに入力した画像を格納
        path = request.form.get("picture")
        # pictureが空白、もしくは存在しない場合
        if not path:
            return apology("picture not exist", 400)


        path = "static/test_image/" + path

        LABELS = ["寿司", "サラダ", "麻婆豆腐"]
        CALORIES = [588, 118, 648]

        idx, per = check_photo(path)
        idx += 1
        idx = str(idx)
        row = db.execute("SELECT * FROM nutritions WHERE id = ?", idx)
        name = row[0]["dish"]
        # return apology(dish_name)
        # これは画像が正しくインプットされているかどうかのテストコードです

        protain = row[0]["protain"]
        fat = row[0]["fat"]
        carbohydrate = row[0]["carbohydrate"]
        calorie = row[0]["calorie"]

        return render_template("check.html", path=path, name=name, per=per, protain=protain, fat=fat,  carbohydrate=carbohydrate, calorie=calorie)

    else:
        return render_template("post.html")

    # return apology("TODO")

# 2つ目
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        # return apology(str(session["user_id"]))
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# 1つ目
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # usernameの入力
        username = request.form.get("username")
        # username未入力の場合
        if not username:
            return apology("username", 400)

        # passwordの入力
        password = request.form.get("password")
        # password未入力の場合
        if not password:
            return apology("password", 400)

        check_large = 0
        check_small = 0
        check_number = 0
        for i in password:
            if ord(i) in range(ord("A"), ord("Z") + 1):
                check_large = 1
            elif ord(i) in range(ord("a"), ord("z") + 1):
                check_small = 1
            elif ord(i) in range(ord("0"), ord("9") + 1):
                check_number = 1

            if check_large == 1 and check_small == 1 and check_number == 1:
                break

        if check_large == 0 or check_small == 0 or check_number == 0:
            return apology("pattern of password", 400)

        # passwordの再入力
        password_again = request.form.get("confirmation")
        # password_again未入力の場合
        if not password_again:
            return apology("confirmation", 400)

        # 再入力したpasswordの正誤確認
        if password_again != password:
            return apology("pass worng", 400)

        # 入力したusernameに合致するデータをデータベースから1行でrowsに格納
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # rowsに格納されたデータがない、すなわち登録したusernameに重複がない場合
        if len(rows) != 1:
            password = generate_password_hash(password, method="sha256")
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)
            return redirect("/login")
        # 登録したusernameがすでに登録済みである場合
        elif rows[0]["username"] == username:
            return apology("already used", 400)

        session["user_id"] = rows[0]["id"]
        return redirect("/login")

    else:
        return render_template("register.html")

# 5つ目
@app.route("/prepare", methods=["GET", "POST"])
def prepare():
    """料理をデータベースへ登録"""

    if request.method == "POST":

        # 料理名の入力
        dish_name = request.form.get("dish_name")
        # dish_name未入力の場合
        if not dish_name:
            return apology("dish_name", 400)

        # 入力したdish_nameに合致するデータをデータベースから1行でrowsに格納
        rows = db.execute("SELECT * FROM nutritions WHERE dish = ?", dish_name)
        # 登録したdish_nameがすでに登録済みである場合
        if len(rows) == 1:
            return apology("already prepared", 400)

        # protainの入力
        protain = request.form.get("protain")
        # protain未入力の場合
        if not protain:
            return apology("protain", 400)

        # fatの入力
        fat = request.form.get("fat")
        # fat未入力の場合
        if not fat:
            return apology("fat", 400)

        # carbohydrateの入力
        carbohydrate = request.form.get("carbohydrate")
        # carbohydrate未入力の場合
        if not carbohydrate:
            return apology("carbohydrate", 400)

        # calorieの入力
        calorie = request.form.get("calorie")
        # carbohydrate未入力の場合
        if not calorie:
            return apology("calorie", 400)

        db.execute("INSERT INTO nutritions (dish, protain, fat, carbohydrate, calorie) VALUES(?, ?, ?, ?, ?)",
                    dish_name, protain, fat, carbohydrate, calorie)

        return redirect("/login")

    else:
        return render_template("prepare.html")


if __name__ == "__main__":
    app.run()