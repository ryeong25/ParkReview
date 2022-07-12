from select import select
from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://Sparta:SpArTae8737be698@cluster0.licyu.mongodb.net/?retryWrites=true&w=majority')
db = client.parkReview

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

# 나의 리뷰
@app.route('/mypage/myReviews/<parkId>')
def getReviews(parkId):
    user=db.Users.find_one({'userId': 0})
    parks=list(db.Parks.find({}))

    userReviewId=user['reviewId']
    reviews=db.Reviews.find_one({'reviewId': userReviewId})
    print(reviews)

    return render_template("mypage.html", user=user, parks=parks, currList=reviews, parkId=parkId)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)