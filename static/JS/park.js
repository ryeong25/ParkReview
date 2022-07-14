function save_review() {
    let date = $('#mm').val() + $('#dd').val()
    let rate = $('#rate').val()
    let comment = $('#comment').val()

    $.ajax({
        type: 'POST',
        url: '/api/postMyReviews,
        data: {
            parkId_give: parkId,
            selectedCourse,
            date_give: date,
            rate_give: rate,
            weather_give: weather,
            comment_give: comment
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}
