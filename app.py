from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

ca = certifi.where()
client = MongoClient('mongodb+srv://Sparta:SpArTae8737be698@cluster0.licyu.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.parkReview


@app.route('/api/checkLogin')
def checkLogin():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userId = int(payload['userId'])
        user = db.Users.find_one({'userId': userId})
        return user, userId
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login.html', msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login.html', msg="로그인 시간이 만료되었습니다."))
    except:
        return redirect(url_for('login.html', msg="다시 로그인 해주세요!"))


@app.route('/')
def main():
    try:
        user, userId = checkLogin()
    except:
        return redirect(url_for("login", msg="다시 로그인 해주세요!"))
    return render_template('mainpage.html', user=user, userId=userId)


@app.route('/parkpage/<parkId>')
def park(parkId):
    try:
        user, userId = checkLogin()
    except:
        return redirect(url_for("login", msg="다시 로그인 해주세요!"))
    intParkId = int(parkId)
    parks = db.Parks.find_one({"parkId": intParkId})
    currList = db.Reviews.find_one({'reviewId': userId}, {"_id": False})
    return render_template("park.html", user=user, parks=parks, currList=currList, parkId=intParkId)


@app.route('/header')
def header():
    return render_template('header.html')


@app.route('/footer')
def footer():
    return render_template('footer.html')


#################################
##  HTML을 주는 부분             ##
#################################

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/test')
def test():
    doc = [{'parkId': 2, 'courseId': 0, 'rate': 1, 'weather': '☔', 'finished_at': '2022-02-01',
            'comment': '앉을 자리도 없고 완전 더워요😡. 모기 있음'},
           {'parkId': 0, 'courseId': 1, 'rate': 5, 'weather': '☀', 'finished_at': '2022-02-02',
            'comment': '내일 또 오고 싶은 멋있는 공원👍👍👍'},
           {'parkId': 1, 'courseId': 2, 'rate': 4, 'weather': '🌤', 'finished_at': '2022-02-03',
            'comment': '캠핑하면서 자전거 타고 라면과 치킨 먹기!'},
           {'parkId': 1, 'courseId': 2, 'rate': 5, 'weather': '🌤', 'finished_at': '2022-02-03',
            'comment': '음악 분수대가 시원하고 멋있다.'},
           {'parkId': 0, 'courseId': 2, 'rate': 5, 'weather': '☀', 'finished_at': '2022-02-04',
            'comment': '멋있다. 출구 근처에 웨이팅하는 도토리묵 맛집 있음!😄'},
           {'parkId': 2, 'courseId': 1, 'rate': 4, 'weather': '☀', 'finished_at': '2022-02-05',
            'comment': '한바퀴 둘러보기 좋습니다.🚲'},
           {'parkId': 0, 'courseId': 0, 'finished_at': 'MM월-DD일', 'rate': '평점', 'weather': '날씨', 'comment': ''}]
    new = {'reviewId': 0, 'reviews': doc}
    db.Reviews.insert_one(new)
    return render_template('login.html')




# [회원가입 API]
# id, pw, nickname, email을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/sign_up/save', methods=['POST'])
def api_register():
    email_receive = request.form['email_give']
    userName_receive = request.form['userName_give']
    pw_receive = request.form['password_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    userIdNum = db.Users.count_documents({})

    doc = {'userId': userIdNum,
           'email': email_receive,
           'userName': userName_receive,
           'password': pw_hash,
           'parkCheck': []}

    db.Users.insert_one(doc)
    return jsonify({'result': 'success'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/sign_in', methods=['POST'])
def api_login():
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    result = db.Users.find_one({'email': email_receive, 'password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        userId = result['userId']
        payload = {
            'userId': userId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/sign_out', methods=['POST'])
def api_logout():
    try:
        user, userId = checkLogin()
    except:
        return redirect(url_for("login", msg="다시 로그인 해주세요!"))
    payload = {
        'userId': userId,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=0)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return jsonify({'result': 'success', 'token': token})


@app.route('/api/sign_up/check_dup', methods=['POST'])
def check_dup():
    email_receive = request.form['email_give']
    exists = bool(db.Users.find_one({"email": email_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 마이페이지
@app.route('/mypage')
def mypage():
    try:
        user, userId = checkLogin()
    except:
        return redirect(url_for("login", msg="다시 로그인 해주세요!"))
    parks = list(db.Parks.find({}))
    currList = parks
    return redirect('/mypage/myParks/all')


# 나의 공원
@app.route('/mypage/myParks/<parkId>')
def getMyParks(parkId):
    try:
        user, userId = checkLogin()
    except:
        return redirect(url_for("login", msg="다시 로그인 해주세요!"))

    parkCheck = user['parkCheck']
    parks = list(db.Parks.find({}))
    currList = parks

    return render_template("mypage.html", user=user, parks=parks, currList=currList, parkId=parkId)


# 나의 리뷰
@app.route('/mypage/myReviews/<parkId>')
def getMyReviews(parkId):
    try:
        user, userId = checkLogin()
    except:
        return redirect(url_for("login", msg="다시 로그인 해주세요!"))
    parks = list(db.Parks.find({}))

    userReviewId = user['reviewId']
    reviews = db.Reviews.find_one({'reviewId': userReviewId})
    print(reviews)

    return render_template("mypage.html", user=user, parks=parks, currList=reviews, parkId=parkId)


@app.route('/api/postMyReview', methods=['POST'])
def postReview():
    try:
        user, userId = checkLogin()
    except:
        return redirect(url_for("login", msg="다시 로그인 해주세요!"))

    # parkId_receive = request.form['parkId_give']
    date_receive = request.form['date_give']
    rate_receive = request.form['rate_give']
    weather_receive = request.form['weather_give']
    comment_receive = request.form['comment_give']

    doc = {
        'parkId': 0,
        'courseId': 0,
        'finished_at': date_receive,
        'rate': rate_receive,
        'weather': weather_receive,
        'comment': comment_receive
    }
    currList = db.Reviews.find_one({'reviewId': userId})
    if not currList == True:
        new = {'reviewId': userId, 'reviews': doc}
        db.Reviews.insert_one(new)
        return jsonify({'msg': '리뷰 저장 완료'})
    else:
        new = currList['reviews']
        new.append(doc)
        db.Reviews.update_one({'reviewId': userId}, {"$set": {"reviews": new}})
        return jsonify({'msg': '리뷰 저장 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
