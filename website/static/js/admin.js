
$('.deleteBtn').click(function(e){
    e.preventDefault()
    e.stopPropagation();
    e.stopImmediatePropagation();

    var email= {"email" : $(this).data('user')}
    
    let str  = email['email']
    

    
    document.querySelector('.bg-modal-delete').style.display = 'flex'
    document.getElementById('deleteEmail').innerHTML = str
    document.getElementById('deleteEmail').style.fontWeight = 'bold'

    // ak bolo stlacene tlacidlo Nie
    document.getElementById('btnNo').addEventListener('click', function() {
        document.querySelector('.bg-modal-delete').style.display = 'none'
    })

    // ak bolo stlacene tlacidlo exit
    document.querySelector('.btnClose').addEventListener('click', function() {
        document.querySelector('.bg-modal-delete').style.display = 'none'
    })

    
    // ak bolo stlacene tlacidlo Ano
    document.getElementById('btnYes').addEventListener('click', function() {
        $.ajax({
            type: "POST",
            url: "/admin/delete/",
            data: email,
            dataType: "json",
            success: function (response) {
                location.reload()   // aby obnovilo stranku 
            }
        });
    })
})


function checkBtn(id, value){
    if (value == 1) {
        document.getElementById(id).classList.add('fa-check')
        document.getElementById(id).classList.remove('fa-times')
    } else {
        document.getElementById(id).classList.add('fa-times')
        document.getElementById(id).classList.remove('fa-check')
    }
}

function setPlaceholder(user){
    $('#nameI').attr('placeholder', user['user_name'])
    $('#surnameI').attr('placeholder', user['user_surname'])
    $('#e-mailI').attr('placeholder', user['email'])
    $('#birth-dateI').attr('placeholder', user['birth_date'])
}



$('.editBtn').click(function(e){
    e.preventDefault()
    e.stopPropagation();
    e.stopImmediatePropagation();
    
    var email =  $(this).data('edit')

    $('#sendEdit').click(function(e){

        var name = $('#nameI').val()
        var surname = $('#surnameI').val()
        var new_email = $('#e-mailI').val()
        var birth_date = $('#birth-dateI').val()
        var adminR = 0
        var libR = 0
        var disR = 0
        var basicUserR = 0

        if (document.getElementById('adminR').classList.contains('fa-check')){
            adminR = 1
        }
        if (document.getElementById('libR').classList.contains('fa-check')){
            libR = 1
        }
        if (document.getElementById('disR').classList.contains('fa-check')){
            disR = 1
        }
        if (document.getElementById('basicUserR').classList.contains('fa-check')){
            basicUserR = 1
        }

        var data = {
            "old_email" : email,
            "email" : new_email,
            "user_name" : name,
            "user_surname" : surname,
            "birth_date" : birth_date,
            "admin" : adminR,
            "librarian" : libR,
            "distributor" : disR,
            "reader" : basicUserR,
        }

        $.ajax({
            type: "POST",
            url: "/admin/editUser/",
            data: data,
            dataType: "json",
            success: function (response) {

            }
        });
        document.getElementById("e-mailI").value = ""
        document.querySelector('.bg-modal-edit').style.display = 'none'

       
       

    })
  
    var user = false
    $.ajax({
        type: "GET",
        url: "/admin/user/"+email,
        success: function (response) {
            var user = response['user']
            document.getElementById('name').innerHTML = user['user_name']
            document.getElementById('surname').innerHTML = user['user_surname']
            document.getElementById('e-mail').innerHTML = user['email']
            document.getElementById('birth-date').innerHTML = user['birth_date']
            
            checkBtn("adminR", user['admin'])
            checkBtn("libR", user['librarian'])
            checkBtn("disR", user['distributor'])
            checkBtn("basicUserR", user['reader'])

            setPlaceholder(user)
            
            
            $('#adminAdd').click(function(e){
                checkBtn("adminR", 1)
            })
            $('#adminRemove').click(function(e){
                checkBtn("adminR", 0)
            })
            $('#libAdd').click(function(e){
                checkBtn("libR", 1)
            })
            $('#libRemove').click(function(e){
                checkBtn("libR", 0)
            })
            $('#disAdd').click(function(e){
                checkBtn("disR", 1)
            })
            $('#disRemove').click(function(e){
                checkBtn("disR", 0)
            })
            $('#basicUserAdd').click(function(e){
                checkBtn("basicUserR", 1)
            })
            $('#basicUserRemove').click(function(e){
                checkBtn("basicUserR", 0)
            })

        }
    });
    console.log(user['name'])
    document.querySelector('.bg-modal-edit').style.display = 'flex'
    


     // ak bolo stlacene tlacidlo exit
     document.querySelector('.btnCloseEdit').addEventListener('click', function() {
        document.querySelector('.bg-modal-edit').style.display = 'none'
    })
    /*
    document.getElementById('btnYes').addEventListener('click', function() {
        $.ajax({
            type: "POST",
            url: "/admin/delete/",
            data: email,
            dataType: "json",
            success: function (response) {
                location.reload()   // aby obnovilo stranku 
            }
        });
    })
    */
})

    
    








