$("#login").click(function(e){
    e.preventDefault()

    var email = $("#email").val()
    var pass = $("#pass").val()
    var data = {
        "email" : email,
        "pass" : pass,
    }

    $.ajax({
        type: "POST",
        url: "/auth/login/",
        data: data,
        dataType: "json",
        success: function (response) {
            if(!response['err'])
                window.location.href = '/'
        }
    });




})