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
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace("/login")
            } else {
                alert(response['msg'])
            }
        }
    });
}
