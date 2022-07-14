$(document).ready(function () {
    var list = all_parks;
    console.log(list);
})


function sign_out() {
    $.ajax({
        type: "POST",
        url: "/api/sign_out",
        data: {},
        success: function (response) {
            alert('로그아웃 되었습니다!')
            $.cookie('mytoken', response['token'], {path: '/'});
            window.location.replace("/login")
        }
    });
}
