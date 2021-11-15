
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

