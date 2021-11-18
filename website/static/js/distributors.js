// Odstranenie distributora
// ak bolo stlacene tlacidlo Nie schova sa Pop up okno
document.getElementById('btnNo').addEventListener('click', function() {
    document.querySelector('.bg-modal-delete').style.display = 'none'
})

// Odstranenie distributora
// ak bolo stlacene tlacidlo Exit schova sa Pop Up okno
document.querySelector('.btnClose').addEventListener('click', function() {
    document.querySelector('.bg-modal-delete').style.display = 'none'
})


// Tlacidlo na odstranenie distributora
$('.deleteBtn').click(function(e){
    e.preventDefault()
    e.stopPropagation();
    e.stopImmediatePropagation();

    var email= {"email" : $(this).data('distributor')}
    let str  = email['email']

    document.getElementById('deleteEmail').innerHTML = str
    document.getElementById('deleteEmail').style.fontWeight = 'bold'
   
    // Zobrazi sa Pop Up okno
    document.querySelector('.bg-modal-delete').style.display = 'flex'
})

// Odstranenie distributora
// Ak bolo stlacene tlacidlo ANO
document.getElementById('btnYes').addEventListener('click', function() {
    var str = document.getElementById('deleteEmail').innerHTML
    
    var email = {"email" : str}
    $.ajax({
        type: "POST",
        url: "/admin/distributors/delete/",
        data: email,
        dataType: "json",
        success: function (response) {
            if (response['message'] == 'ok')
            {
                Toast.show('Uspešne si odstránil vydavatela','S')
               
            }   
            document.querySelector('.bg-modal-delete').style.display = 'none'             
        }
    });
 
})