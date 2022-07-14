$(document).ready(function () {
    let parkId = $('#parkId').value
    let userId = $('#userId').value
    let date = $('#mm').val() + '-' + $('#dd').val()
    let weather = $('#weather').val()
    let rate = $('#rate').val()
    let comment = $('#comment').val()

    $('#ReviewBtn').on('click', function () {
        save_review()
    })


})

function save_review() {


    let parkId = $('#parkId').value
    let userId = $('#userId').value
    let date = $('#mm').val() + '-' + $('#dd').val()
    let weather = $('#weather').val()
    let rate = $('#rate').val()
    let comment = $('#comment').val()

    $.ajax({
        type: 'POST',
        url: '/api/postMyReview',
        data: {
            // reviewId: userId,
            // parkId_give: parkId,
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