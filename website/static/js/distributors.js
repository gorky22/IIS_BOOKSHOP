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
            document.querySelector('.'+ email["email"]).style.display = 'none'             
        }
        
    });
    document.querySelector('.bg-modal-delete').style.display = 'none'
})

// Funkcia ktora nastavi Placeholder-y
function setPlaceholder(lib){
    $('#nameI').attr('placeholder', lib['library_name'])
    $('#townI').attr('placeholder', lib['town'])
    $('#opening_hoursI').attr('placeholder', lib['opening_hours'])
    $('#web_linkI').attr('placeholder', lib['webpage_link'])
    $('#path_picI').attr('placeholder', lib['path_to_picture'])
    $('#lib_emailI').attr('placeholder', lib['library_email'])

}


// Editacia knihovne 
// Tlacidlo na editovanie knihovne 
$('.editBtn').click(function(e){
    e.preventDefault()
    
    var email =  $(this).data('edit')

    $.ajax({
        type: "GET",
        url: "/admin/library/"+email,
        success: function (response) {
            var lib = response['lib']

            document.getElementById('name').innerHTML = lib['library_name']
            document.getElementById('town').innerHTML = lib['town']
            document.getElementById('opening_hours').innerHTML = lib['opening_hours']
            document.getElementById('web_link').innerHTML = lib['webpage_link']
            document.getElementById('path_pic').innerHTML = lib['path_to_picture']
            document.getElementById('lib_email').innerHTML = lib['library_email']

            setPlaceholder(lib)

            // Zobrazi sa Pop Up okno na editaciu            
            document.querySelector('.bg-modal-edit').style.display = 'flex'
        }
    });


     
})


// Funkcia na odstraninie starych inputov
function delete_inputs(){

    document.getElementById('nameI').value = ""
    document.getElementById("townI").value = ""
    document.getElementById('opening_hoursI').value = ""
    document.getElementById('web_linkI').value = ""
    document.getElementById('path_picI').value = ""
    document.getElementById('lib_emailI').value = ""

}


// Editacia knihovne
// Ak bolo stlacene tlacidlo exit
document.querySelector('.btnCloseEdit').addEventListener('click', function() {
    document.querySelector('.bg-modal-edit').style.display = 'none'

    delete_inputs()
})


// Editacia knihovne
// Ak bolo stlacene tlacidlo na ulozenie zmien
$('#sendEdit').click(function(e){
    var old_email = document.getElementById('lib_email').innerHTML

    var name = $('#nameI').val()
    var town = $('#townI').val()
    var opening_hours = $('#opening_hoursI').val()
    var web_link = $('#web_linkI').val()
    var path_pic = $('#path_picI').val()
    var lib_email = $('#lib_emailI').val()
   


    
   
    var data = {
        "old_email" : old_email,
        "library_name" : name,
        "town" : town,
        "opening_hours" : opening_hours,
        "webpage_link" : web_link,
        "path_to_picture" : path_pic,
        "library_email" : lib_email,
    }

    $.ajax({
        type: "POST",
        url: "/admin/editLib/",
        data: data,
        dataType: "json",
        success: function (response) {
            if (response['message'] == 'ok')
            {
                Toast.show('Úspešna editácia knihovny','S')
                document.querySelector('.bg-modal-edit').style.display = 'none'

                delete_inputs()
            }    
        }
    });
})


// Tlacidlo na pridanie knihovne
$('#btnAddLib').click(function(e){
    e.preventDefault()
   
    // Zobrazi sa Pop Up okno
    document.querySelector('.bg-modal-add').style.display = 'flex'
})


// Pridanie knihovne
// ak bolo stlacene tlacidlo Exit schova sa Pop Up okno
document.querySelector('.btnCloseAdd').addEventListener('click', function() {
    document.querySelector('.bg-modal-add').style.display = 'none'
})



// Pridanie knihovne
// Ak bolo stlacene tlacidlo na pridanie
$('#sendAdd').click(function(e){

    var data = 'fero'

    $.ajax({
        type: "POST",
        url: "/admin/addLib/",
        data: data,
        dataType: "json",
        success: function (response) {

            document.querySelector('.bg-modal-add').style.display = 'none'
        }
    });
})