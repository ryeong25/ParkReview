
# 샘플 데이터
user = { 
    'userId': 0,
    'reviewId': 0,
    'email': "canon@google.com", 
    'userName': "홍길동",
    'password': "1111",
    'parkCheck': [
        {
            'parkId': 0,
            'finished': 1,
            'favorite': 0
        },
        {
            'parkId': 1,
            'finished': 1,
            'favorite': 0
        },
        {
            'parkId': 2,
            'finished': 1,
            'favorite': 0
        }
    ]
}
# 코멘트
review = {
    'reviewId': 0,
    'reviews': [
        {
            'parkId': 2,
            'rate': 1,
            'finished_at': '2022-02-01',
            'comment': "앉을 자리도 없고 완전 더워요😡. 모기 있음"
        }, 
        {
            'parkId': 0,
            'rate': 5,
            'finished_at': '2022-02-02',
            'comment': "내일 또 오고 싶은 멋있는 공원👍👍👍"
        }, 
        {
            'parkId': 1,
            'rate': 4,
            'finished_at': '2022-02-03',
            'comment': "100년된 배나무가 멋있다.",
        }
    ]
}
# 공원
park = [
    {
        'parkId': 0, 
        'parkName': '장미공원', 
        'parkLocation': '서울 장미구 장미로', 
        'parkDesc': "5월의 장미가 아름다운 공원. 중랑천을 따라 3가지의 산책로를 걸을 수 있다.",
        'runningTime': '2시간',
        'course': [
            {
                "courseId": 0,
                'courseName': "어려운 코스",
                'imgUrl': 'course/0-0.jpg'
            },
            {
                "courseId": 1,
                'courseName': "쉬어가는 코스",
                'imgUrl': 'course/0-1.jpg'
            }
        ]
    },
    {
        'parkId': 1, 
        'parkName': '배나무공원', 
        'parkLocation': '서울 아삭구 시원로', 
        'parkDesc': '배나무가 남아있는 공원으로, 배 직판장에서 먹골배를 박스째 구입할 수 있고, 배 따기 체험등을 할 수 있는 시민들의 휴식공간이다.', 
        'runningTime': '1시간',
        'course': [
            {
                "courseId": 0,
                'courseName': "배나무 코스",
                'imgUrl': 'course/1-0.jpg'
            },
            {
                "courseId": 1,
                'courseName': "그냥 코스",
                'imgUrl': 'course/1-1.jpg'
            }
        ]
    },
    {
        'parkId': 2, 
        'parkName': '물빛 공원', 
        'parkLocation': '서울 물빛구 호수로', 
        'parkDesc': '자연을 닮은 인공호수를 바라보며 산책할 수 있는 공원이다. 음악과 함께하는 분수 공연을 구경할 수 있는 여름부터, 꽁꽁 언 호수를 바라볼 수 있는 겨울까지 인기가 많은 공원이다.', 
        'runningTime': '1시간 30분',
        'course': [
            {
                "courseId": 0,
                'courseName': "경사진 코스",
                'imgUrl': 'course/2-0.jpg'
            },
            {
                "courseId": 1,
                'courseName': "호수를 둘러가는 코스",
                'imgUrl': 'course/2-1.jpg'
            }
        ]
    }
]