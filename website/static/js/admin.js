// Odstranenie uzivatela
// ak bolo stlacene tlacidlo Nie schova sa Pop up okno
document.getElementById('btnNo').addEventListener('click', function() {
    document.querySelector('.bg-modal-delete').style.display = 'none'
})

// Odstranenie uzivatela
// ak bolo stlacene tlacidlo Exit schova sa Pop Up okno
document.querySelector('.btnClose').addEventListener('click', function() {
    document.querySelector('.bg-modal-delete').style.display = 'none'
})


// Tlacidlo na odstranenie uzivatela
$('.deleteBtn').click(function(e){
    e.preventDefault()
    e.stopPropagation();
    e.stopImmediatePropagation();

    var email= {"email" : $(this).data('user')}
    let str  = email['email']

    document.getElementById('deleteEmail').innerHTML = str
    document.getElementById('deleteEmail').style.fontWeight = 'bold'
   
    // Zobrazi sa Pop Up okno
    document.querySelector('.bg-modal-delete').style.display = 'flex'
})

// Odstranenie uzivatela
// Ak bolo stlacene tlacidlo ANO
document.getElementById('btnYes').addEventListener('click', function() {
    var str = document.getElementById('deleteEmail').innerHTML

    var email = {"email" : str}
    $.ajax({
        type: "POST",
        url: "/admin/delete/",
        data: email,
        dataType: "json",
        success: function (response) {
            if (response['message'] == 'ok')
            {
                Toast.show('Uspešne si odstránil uživateľa','S')
                location.reload()
            }                
        }
    });
    document.querySelector('.bg-modal-delete').style.display = 'none'
})



// Funkcia ktora nastavi Check box
function checkBtn(id, value){
    if (value == 1) {
        document.getElementById(id).classList.add('fa-check')
        document.getElementById(id).classList.remove('fa-times')
        document.getElementById(id).style.marginRight = "1rem"
        document.getElementById(id).style.marginLeft = "1rem"
    } else {
        document.getElementById(id).classList.add('fa-times')
        document.getElementById(id).style.marginRight = "1.3rem"
        document.getElementById(id).style.marginLeft = "1.3rem"

        document.getElementById(id).classList.remove('fa-check')
    }
}

// Funkcia ktora nastavi Placeholder-y
function setPlaceholder(user){
    $('#nameI').attr('placeholder', user['user_name'])
    $('#surnameI').attr('placeholder', user['user_surname'])
    $('#e-mailI').attr('placeholder', user['email'])

    var birth_date = beautifulDate(user['birth_date'])
    
    $('#birth-dateI').attr('placeholder', birth_date)
}


// Editacia uzivatela 
// Tlacidlo na editovanie uzivatela 
$('.editBtn').click(function(e){
    e.preventDefault()
    
    document.getElementById('res-combobox').value=0

    var email =  $(this).data('edit')
    var user = false

    $.ajax({
        type: "GET",
        url: "/admin/user/"+email,
        success: function (response) {
            var user = response['user']
            var date = beautifulDate(user['birth_date'])

            document.getElementById('name').innerHTML = user['user_name']
            document.getElementById('surname').innerHTML = user['user_surname']
            document.getElementById('e-mail').innerHTML = user['email']
            document.getElementById('birth-date').innerHTML = date
            
            checkBtn("adminR", user['admin'])
            checkBtn("libR", user['librarian'])
            if (user['librarian'] == 1){
                document.getElementById("res-combobox").classList.remove('hide')
                document.getElementById("hide_br").classList.remove('hide')
                document.getElementById('res-combobox').value=user['library_id']
            } else {
                document.getElementById("res-combobox").classList.add('hide')
                document.getElementById("hide_br").classList.add('hide')
            }
            checkBtn("disR", user['distributor'])
            if (user['distributor'] == 1){
                document.getElementById("res-comboboxDis").classList.remove('hide')
                document.getElementById("hide_br_dis").classList.remove('hide')
            
            } else {
                document.getElementById("res-comboboxDis").classList.add('hide')
                document.getElementById("hide_br_dis").classList.add('hide')
            }
            checkBtn("basicUserR", user['reader'])

            setPlaceholder(user)
            
            // Zobrazi sa Pop Up okno na editaciu            
            document.querySelector('.bg-modal-edit').style.display = 'flex'

        }
    });
})


// Funkcia na odstraninie starych inputov
function delete_inputs(){

    document.getElementById('nameI').value = ""
    document.getElementById("e-mailI").value = ""
    document.getElementById('surnameI').value = ""
    document.getElementById('birth-dateI').value = ""

}


// Editacia uzivatela 
// Vykreslenie Check boxu
// Nazaklade toho ci ma uzivatel dane prava
$('#adminAdd').click(function(e){
    checkBtn("adminR", 1)
})
$('#adminRemove').click(function(e){
    checkBtn("adminR", 0)
})
$('#libAdd').click(function(e){
    document.getElementById("res-combobox").classList.remove('hide')
    document.getElementById("hide_br").classList.remove('hide')

    document.getElementById('res-combobox').value=0

    //$('#res-combobox').find('option:selected').val(10)
    //var fero = $('#res-combobox').find('option:selected').val()
    
    //document.getElementById('res-combobox').value=55
    //alert(fero)

    checkBtn("libR", 1)
})
$('#libRemove').click(function(e){
    document.getElementById("res-combobox").classList.add('hide')
    document.getElementById("hide_br").classList.add('hide')

    //odobrat knihovnu v ktorej user pracuje
    document.getElementById('res-combobox').value=0
    checkBtn("libR", 0)
})
$('#disAdd').click(function(e){
    document.getElementById("res-comboboxDis").classList.remove('hide')
    document.getElementById("hide_br_dis").classList.remove('hide')

    //odobrat knihovnu v ktorej user pracuje
    document.getElementById('res-comboboxDis').value=0

    checkBtn("disR", 1)
})
$('#disRemove').click(function(e){
    document.getElementById("res-comboboxDis").classList.add('hide')
    document.getElementById("hide_br_dis").classList.add('hide')

    //odobrat knihovnu v ktorej user pracuje
    document.getElementById('res-comboboxDis').value=0
    checkBtn("disR", 0)
})
$('#basicUserAdd').click(function(e){
    checkBtn("basicUserR", 1)
})
$('#basicUserRemove').click(function(e){
    checkBtn("basicUserR", 0)
})


// Editacia uzivatela
// Ak bolo stlacene tlacidlo exit
document.querySelector('.btnCloseEdit').addEventListener('click', function() {
    document.querySelector('.bg-modal-edit').style.display = 'none'

    document.getElementById("res-combobox").classList.add('hide')
    document.getElementById("hide_br").classList.add('hide')

    delete_inputs()
})



// Editacia uzivatela
// Ak bolo stlacene tlacidlo na ulozenie zmien
$('#sendEdit').click(function(e){
    var email = document.getElementById('e-mail').innerHTML

    var name = $('#nameI').val()
    var surname = $('#surnameI').val()
    var new_email = $('#e-mailI').val()
    var birth_date = $('#birth-dateI').val()
    var adminR = 0
    var libR = 0
    var disR = 0
    var basicUserR = 0
    var libraryId = $('#res-combobox').find('option:selected').val()

    if (document.getElementById('adminR').classList.contains('fa-check')){
        adminR = 1
    }
    if (document.getElementById('libR').classList.contains('fa-check')){
        libR = 1
    } else {
        document.getElementById("res-combobox").classList.add('hide')
        document.getElementById("hide_br").classList.add('hide')
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
        "library_id" : libraryId,
    }

    if(testEmail(new_email)){
        $.ajax({
            type: "POST",
            url: "/admin/editUser/",
            data: data,
            dataType: "json",
            success: function (response) {
                if (response['message'] == 'ok')
                {
                    Toast.show('Úspešna editácia uživateľa','S')
                    document.querySelector('.bg-modal-edit').style.display = 'none'
                    delete_inputs()
                    location.reload()
    
                } else {
                    Toast.show('Knihovnikovi nebola priadana knihovna','E')
                }    
            }
        });
    } 
    
})








