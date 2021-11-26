$("#login").click(function(e){
    e.preventDefault()
    
    var email = $("#email").val()
    var pass = $("#pass").val()
    var data = {
        "email" : email,
        "pass" : pass,
    }
    if(!testEmail(email)){
        Toast.show("E-mail je neplatný","e")
        return
    }
    $.ajax({
        type: "POST",
        url: "/auth/login/",
        data: data,
        dataType: "json",
        success: function (response) {
            if(response['err']){
                Toast.show(response['message'],'E')
            } else {
                Toast.show('Přihlášení proběhlo v pořádku','S')
                setTimeout(() => {
                   window.location.href = response['url'];
                },1000)
            }
        },
        error: function (response){
            Toast.show('Při přihlašování nastala chyba. Zkuste to prosím později','E')
        }
    });




})

function testEmail(value){
    if(value.length < 7){
        return false;
    } else if(!value.includes("@")){
        return false;
    } else if(!value.includes(".")){
        return false;
    } else if (value.includes(" ")){
        return false;
    }
    return true;
    
}
