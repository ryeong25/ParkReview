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
def getMyParks(parkId):
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({}))
    currList=parks

    print('here')

    return render_template("mypage.html", user=user, parks=parks, currList=currList, parkId=parkId)

# 나의 리뷰
@app.route('/mypage/myReviews/<parkId>')
def getMyReviews(parkId):
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({}))

    userReviewId=user['reviewId']
    reviews=db.Reviews.find_one({'reviewId': userReviewId})
    print(reviews)

    return render_template("mypage.html", user=user, parks=parks, currList=reviews, parkId=parkId)


<<<<<<< HEAD
=======


@app.route('/api/getParkInfo/<parkId>')
def getParks(parkId):
    currList = db.Parks.find_one({'parkId':parkId})
    return jsonify({'Parks': currList})

@app.route('/api/checkLogin')
def checkLogin():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/park/<parkId>')
def park(userId,parkId):
    return render_template("park.html", userId=userId, parkId=parkId)




@app.route('/api/checkLogin')
def checkLogin():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})



@app.route('/api/getParkInfo/<parkId>')
def getParks(parkId):
    currList = db.Parks.find_one({'parkId':parkId})
    return jsonify({'Parks': currList})


@app.route('/api/getMyReviews/<userId>')
def getReviews(userId):
    currList = db.Users.find_one({'userId':userId})
    return jsonify({'users': currList})

@app.route('/api/getMyReviews/<reviewId>')
def getReviews(reviewId):
    currList = db.Reviews.find_one({'reviewId':reviewId})
    return jsonify({'Reviews': currList})

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


>>>>>>> seongryeong
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
