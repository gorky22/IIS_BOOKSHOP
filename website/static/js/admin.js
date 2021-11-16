
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

$('.editBtn').click(function(e){
    e.preventDefault()
    e.stopPropagation();
    e.stopImmediatePropagation();


    
    var email =  $(this).data('edit')
    var user = false
    $.ajax({
        type: "GET",
        url: "/admin/user/"+email,
        success: function (response) {
            var user = response['user']
            document.getElementById('name').innerHTML = user['name']
            document.getElementById('surname').innerHTML = user['surname']
            document.getElementById('e-mail').innerHTML = user['email']
            document.getElementById('birth-date').innerHTML = user['birth_date']
            
            checkBtn("adminR", user['admin'])
            checkBtn("libR", user['librarian'])
            checkBtn("disR", user['distributor'])
            checkBtn("basicUserR", user['reader'])


            console.log(user['name'])
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

