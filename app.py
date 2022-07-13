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

client = MongoClient('mongodb+srv://Sparta:SpArTae8737be698@cluster0.licyu.mongodb.net/?retryWrites=true&w=majority')
db = client.parkReview

@app.route('/detail')
def detail():
    return render_template("index.html")


@app.route('/')
def main():
    return render_template("mainpage.html")

@app.route('/park/<parkId>')
def park(parkId):
    return render_template("park.html", parkId=parkId)

@app.route('/api/postMyRevies/<reviewId>', methods=['POST'])
def postReview(reviewId):
    currList = db.Reviews.find_one({'reviewId':reviewId})
    parkId_receive = request.form['parkId_give']
    date_receive = request.form['date_give']
    rate_receive = request.form['rate_give']
    weather_receive = request.form['weather_give']
    comment_receive = request.form['comment_give']

    doc = {
        'parkId': parkId_receive,
        'finished_at': date_receive,
        'rate': rate_receive,
        'weather': weather_receive,
        'comment': comment_receive
    }
    currList.reviews.insert_one(doc)
    return jsonify({'msg': '리뷰 저장 완료'})

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')

# 마이페이지
@app.route('/mypage')
def mypage():
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({}))
    currList=parks

    return render_template("mypage.html", user=user, parks=parks, currList=currList, parkId="all")

# 나의 공원
@app.route('/mypage/myParks/<parkId>')
def getMyParks(parkId):
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({}))
    currList=parks

    return render_template("mypage.html", user=user, parks=parks, currList=currList, parkId=parkId)

# 나의 리뷰
@app.route('/mypage/myReviews/<parkId>')
def getMyReviews(parkId):
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({}))

    userReviewId=user['reviewId']
    reviews=db.Reviews.find_one({'reviewId': userReviewId})

    return render_template("mypage.html", user=user, parks=parks, currList=reviews, parkId=parkId)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
