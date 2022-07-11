from flask import Flask, jsonify, render_template

app = Flask(__name__)

# 샘플 데이터
listA = {
    'userId': "canon", 
    'username': "홍길동",
    'reviews': [
        {
            'parkId': 2,
            'rate': 1,
            'comment': "앉을 자리도 없고 완전 더워요😡. 모기 있음"
        }, 
        {
            'parkId': 0,
            'rate': 5,
            'comment': "내일 또 오고 싶은 멋있는 공원👍👍👍"
        }, 
        {
            'parkId': 1,
            'rate': 4,
            'comment': "100년된 배나무가 멋있다."
        }
    ]
}
listB = [
    {
        'parkId': 0, 
        'parkName': '장미공원', 
        'parkLocation': '서울 장미구 장미로', 
        'parkDesc': "5월의 장미가 아름다운 공원. 중랑천을 따라 3가지의 산책로를 걸을 수 있다.",
        'finished_at': '2022-02-00',
        'finished': 1,
        'favorite': 0
    },
    {
        'parkId': 1, 
        'parkName': '배나무공원', 
        'parkLocation': '서울 아삭구 시원로', 
        'parkDesc': '배나무가 남아있는 공원으로, 배 직판장에서 먹골배를 박스째 구입할 수 있고, 배 따기 체험등을 할 수 있는 시민들의 휴식공간이다.', 
        'finished_at': '2022-02-01',
        'finished': 0,
        'favorite': 1
    },
    {
        'parkId': 2, 
        'parkName': '물빛 공원', 
        'parkLocation': '서울 물빛구 호수로', 
        'parkDesc': '자연을 닮은 인공호수를 바라보며 산책할 수 있는 공원이다. 음악과 함께하는 분수 공연을 구경할 수 있는 여름부터, 꽁꽁 언 호수를 바라볼 수 있는 겨울까지 인기가 많은 공원이다.', 
        'finished_at': '2022-02-02',
        'finished': 1,
        'favorite': 1
    }
    ]

@app.route('/mypage')
def mypage():
    return render_template("mypage.html", users=listA, parks=listB)

@app.route('/getMyReviews/<parkId>')
def getReviews(parkId):
    currList = listB

    # currList = list 중에 parkId가 parkId인 리스트 
    # currList = db.컬렉션명.find_one({'parkId': parkId})
    # if parkId == 'all': 전부 find()
    # if parkId == 'favorite': db.컬렉션명.find({'favorite': 1})의 코멘트
    # if parkId == 'finished': db.컬렉션명.find({'finished': 1})
    
    # return render_template("index.html", users=listA, parks=currList)

    return jsonify({'parkId': parkId})

@app.route('/getMyParks/<parkId>')
def getParks(parkId):
    currList = listB

    # currList = list 중에 parkId가 parkId인 리스트 
    # currList = db.컬렉션명.find_one({'parkId': parkId})
    # if parkId == 'all': 전부 find()
    # if parkId == 'favorite': db.컬렉션명.find({'favorite': 1})의 코멘트
    # if parkId == 'finished': db.컬렉션명.find({'finished': 1})
    
    # return render_template("index.html", users=listA, parks=currList)

    return jsonify({'parkId': parkId})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)