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
            }                
        }
    });
    document.querySelector('.bg-modal-delete').style.display = 'none'
})

// Funkcia na vypisanie datumu v krajsie forme
function beautifulDate(input_date) {
    var date = new Date(input_date)
    var year = date.getFullYear()
    var month = date.getMonth()
    var day = date.getDate()
    var birth_date = year + '-' + month + '-' + day

    return birth_date
}


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
            checkBtn("disR", user['distributor'])
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


// Editacia uzivatela
// Ak bolo stlacene tlacidlo exit
document.querySelector('.btnCloseEdit').addEventListener('click', function() {
    document.querySelector('.bg-modal-edit').style.display = 'none'

    delete_inputs()
})



// Editacia uzivatela
// Ak bolo stlacene tlacidlo na ulozenie zmien
$('#sendEdit').click(function(e){
    var email = document.getElementById('e-mail').innerHTML
    alert(email)

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
            if (response['message'] == 'ok')
            {
                Toast.show('Úspešna editácia uživateľa','S')
            }        
            
            document.querySelector('.bg-modal-edit').style.display = 'none'
            delete_inputs()
        }
    });
    
  

})








