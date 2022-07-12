from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import jwt
import datetime
import hashlib
# 샘플 데이터
app = Flask(__name__)


client = MongoClient(mongodb+srv://Sparta:SpArTae8737be698@cluster0.licyu.mongodb.net/?retryWrites=true&w=majority)
db = client.parkReview
SECRET_KEY = 'sparta'

@app.route('/mypage')
def mypage():
    return render_template("mypage.html")

@app.route('/park/<parkId>')
def park(parkId):
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)