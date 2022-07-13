from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for , json
from werkzeug.utils import secure_filename
from datetime import timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'


ca = certifi.where()
client = MongoClient('mongodb+srv://Sparta:SpArTae8737be698@cluster0.licyu.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.parkReview

@app.route('/')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.Users.find_one({"email": payload["userId"]})
        return render_template("mainpage.html", user=user)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/parkpage/<parkId>')
def park(parkId):
    token_receive = request.cookies.get('mytoken')
    parks = db.Parks.find_one({"parkId": parkId })
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.Users.find_one({'userId': payload['userId']}, {"_id": False})
        currList = db.Reviews.find_one({'reviewId': payload['userId']})
        return render_template("park.html", user=user, parks=parks, currList=currList)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("main"))


@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')

#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/&')
def start():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.Users.find_one({"userId": payload['userId']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


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
           'parkCheck':[]}

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
        # JWT 토큰에는, payloaduserId와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        userId = result['userId']
        payload = {
            'userId': userId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 *1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        # token을 시크릿키로 디코딩합니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        userinfo = db.Users.find_one({'userId': payload['userId']}, {'_id': 0})
        return jsonify({'result': 'success', 'email': userinfo['email']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/api/sign_up/check_dup', methods=['POST'])
def check_dup():
    email_receive = request.form['email_give']
    exists = bool(db.Users.find_one({"email": email_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 마이페이지
@app.route('/mypage')
def mypage():
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({'parkId': 0}))
    currList=parks

    return redirect('/mypage/myParks/all')

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

    return render_template("mypage.html", user=user, parks=parks, currList=reviews, parkId=parkId)

@app.route('/api/checkLogin')
def checkLogin():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.Users.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})



@app.route('/api/postMyReviews/<reviewId>', methods=['POST'])
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
