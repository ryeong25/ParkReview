# <<<<<<< HEAD
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.parkReview

# =======
from select import select
from flask import Flask, jsonify, render_template
from pymongo import MongoClient
>>>>>>> ae8993430ec3f085aa55054aa20dd6f4b9ebc9aa

app = Flask(__name__)

client = MongoClient('mongodb+srv://Sparta:SpArTae8737be698@cluster0.licyu.mongodb.net/?retryWrites=true&w=majority')
db = client.parkReview

@app.route('/detail')
def detail():
    return render_template("index.html")


@app.route('/')
def main():
    return render_template("mainpage.html")

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route('/user/userId')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# 마이페이지
@app.route('/mypage')
def mypage():
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({}))
    currList=parks

    return render_template("mypage.html", user=user, parks=parks, currList=currList, parkId="all")

# 나의 공원
@app.route('/mypage/myParks/<parkId>')
def getParks(parkId):
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({}))
    currList=parks

    print('here')

    return render_template("mypage.html", user=user, parks=parks, currList=currList, parkId=parkId)

<<<<<<< HEAD
@app.route('/user/userId')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


=======
# 나의 리뷰
@app.route('/mypage/myReviews/<parkId>')
def getReviews(parkId):
    user=db.Users.find_one({'userId': 0})
    parks=db.Parks.find({})

    userReviewId=user['reviewId']
    reviews=db.Reviews.find_one({'reviewId': userReviewId})
    print(reviews)

    return render_template("mypage.html", user=user, parks=parks, currList=reviews, parkId=parkId)
>>>>>>> ae8993430ec3f085aa55054aa20dd6f4b9ebc9aa

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)