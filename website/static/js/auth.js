$('#registration').click(function (e) { 
    e.preventDefault();
    
    var email = $('#email').val()
    var firstName = $("#firstName").val()
    var surName = $("#surName").val()
    var pass1 = $("#pass1").val()
    var pass2 = $("#pass2").val()
    var day = $("#day").val()
    var month = $("#month").val()
    var year = $("#year").val()


    var data = {
        "email" : email,
        "firstName" : firstName,
        "surName" : surName,
        "pass1" : pass1,
        "pass2" : pass2,
        "day" : day,
        "month" : month,
        "year" : year,
    }

    $.ajax({
        type: "POST",
        url: "/auth/register/",
        data: data,
        dataType: "json",
        success: function (response) {
            if(response['err']){
                Toast.show(response['message'],'E')
            } else {
                Toast.show('Byl jste úspěšně zaregistrován','S')
                setTimeout(() => {
                   window.location.href = response['url'];
                },2000)
            }
        },
        error: function (response){
            Toast.show('Při registraci nastala chyba. Zkuste to prosím později','E')
        }
    });



});


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
function testPassword(value){
    let longPass = new RegExp('(?=.{8,})')
    let upperCase = new RegExp('(?=.*[A-Z])')
    let lowerCase = new RegExp('(?=.*[a-z])')
    let digit = new RegExp('(?=.*[0-9])')

    if(longPass.test(value) && upperCase.test(value) && lowerCase.test(value) && digit.test(value) ){
        return true
    }
    return false
}

function testSamePasswords(pass1,pass2){
    if(pass1 == pass2 && testPassword(pass1)){
        return true
    } else{
        return false
    }
}


$('#email').focusout(function (e) { 
    var value = $(this).val()
    
    if(testEmail(value)){
        $(this).css("box-shadow","0px 2px 5px rgba(0,255,0, 0.5)")
    } else {
        $(this).css("box-shadow","0px 2px 5px rgba(255,0,0, 0.5)")
        Toast.show('Nesprávný tvar e-mailu.','E')
    }
    
});
$("#firstName").focusout(function(e){
    var value = $(this).val()
    var err = false;
    if(value.includes(".") || value.includes(" ")){
        $(this).css("box-shadow","0px 2px 5px rgba(255,0,0, 0.5)")
        err = true
        Toast.show('Křestní jméno nesmí obsahovat tečku nebo mezeru.','E')
    }
    if(!err){
        $(this).css("box-shadow","0px 2px 5px rgba(0,255,0, 0.5)")
    }
})
$("#surName").focusout(function(e){
    var value = $(this).val()
    var err = false;
    if(value.includes(".") || value.includes(" ")){
        $(this).css("box-shadow","0px 2px 5px rgba(255,0,0, 0.5)")
        err = true
        Toast.show('Příjmení nesmí obsahovat tečku nebo mezeru.','E')
    }
    if(!err){
        $(this).css("box-shadow","0px 2px 5px rgba(0,255,0, 0.5)")
    }
})
$("#pass1").focusout(function(e){
    var value = $(this).val()
    
    if(testPassword(value)){
        $(this).css("box-shadow","0px 2px 5px rgba(0,255,0, 0.5)")
    } else {
        $(this).css("box-shadow","0px 2px 5px rgba(255,0,0, 0.5)")
        Toast.show('Heslo musí obsahovat alespoň jednu číslici, musí být 8 znaků dlouhé a musí obsahovat jedno velké a malé písmeno.','E',4000)
    }
    
})
$("#pass2").focusout(function(e){
    var value = $(this).val()
    var pass = $("#pass1").val()
    if(testSamePasswords(pass,value)){
        $(this).css("box-shadow","0px 2px 5px rgba(0,255,0, 0.5)")
    } else { 
        $(this).css("box-shadow","0px 2px 5px rgba(255,0,0, 0.5)")
        Toast.show('Vaše hesla se neshodují','E',4000)
    }
})


$('input').focusout(function(e){
    if(testEmail($('#email').val()) && testSamePasswords($("#pass1").val(),$("#pass2").val())){
        $('#registration').prop("disabled",false)
        $('#registration').css("background-color","#623CEA")
        $('#registration').css("cursor","pointer")
    } else {
        $('#registration').prop("disabled",true)
        $('#registration').css("cursor","not-allowed")
        $('#registration').css("background-color","#FF0000")
    }
})