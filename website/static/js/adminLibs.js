// Odstranenie knihovne
// ak bolo stlacene tlacidlo Exit schova sa Pop Up okno
document.querySelector('.btnClose').addEventListener('click', function() {
    document.querySelector('.bg-modal-delete').style.display = 'none'
})


// Odstranenie knihovne
// ak bolo stlacene tlacidlo Nie schova sa Pop up okno
document.getElementById('btnNo').addEventListener('click', function() {
    document.querySelector('.bg-modal-delete').style.display = 'none'
})


// Tlacidlo na odstranenie knihovne
$('.deleteBtn').click(function(e){
    e.preventDefault()

    var email= {"email" : $(this).data('lib')}
    let lib_email  = email['email']

    document.getElementById('deleteLib').innerHTML = lib_email
   
    // Zobrazi sa Pop Up okno
    document.querySelector('.bg-modal-delete').style.display = 'flex'
})


// Odstranenie knihovne
// Ak bolo stlacene tlacidlo ANO
document.getElementById('btnYes').addEventListener('click', function() {
    var str = document.getElementById('deleteLib').innerHTML

    var email = {"email" : str}
    $.ajax({
        type: "POST",
        url: "/admin/deleteLib/",
        data: email,
        dataType: "json",
        success: function (response) {
            if (response['message'] == 'ok')
            {
                Toast.show('Uspešne si odstránil knihovnu','S')
                location.reload()
            }                
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
            //document.getElementById('town').innerHTML = lib['town']
            //document.getElementById('town').innerHTML = lib['town']
            document.getElementById('opening_hours').innerHTML = lib['opening_hours']
            document.getElementById('web_link').innerHTML = lib['webpage_link']
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
    //document.getElementById("townI").value = ""
    document.getElementById('opening_hoursI').value = ""
    document.getElementById('web_linkI').value = ""
    document.getElementById('lib_emailI').value = ""

    document.getElementById('nameAdd').value = ""
    document.getElementById('townAdd').value = ""
    document.getElementById('adressAdd').value = ""
    document.getElementById('descriptionAdd').value = ""
    document.getElementById('opening_hoursAdd').value = ""
    document.getElementById('web_linkAdd').value = ""
    document.getElementById('path_picAdd').value = ""
    document.getElementById('lib_emailAdd').value = ""

}


// Editacia knihovne
// Ak bolo stlacene tlacidlo exit
document.querySelector('.btnCloseEdit').addEventListener('click', function() {
    document.querySelector('.bg-modal-edit').style.display = 'none'

    delete_inputs()
})


function checkImage(id){
    var tmp = document.getElementById(id).files.length

    if(tmp == 0){
        Toast.show("Musite zadat obrázok knižnice", "E")
        return false
    }
    return true
}

// Editacia knihovne
// Ak bolo stlacene tlacidlo na ulozenie zmien
$('#sendEdit').click(function(e){
    var old_email = document.getElementById('lib_email').innerHTML

    var name = $('#nameI').val()
    //var town = $('#townI').val()
    var opening_hours = $('#opening_hoursI').val()
    var web_link = $('#web_linkI').val()
    var lib_email = $('#lib_emailI').val()

    
    var file = document.getElementById("path_picEdit").files[0]

    var form_data = new FormData()

    form_data.append("old_email", old_email)
    form_data.append("library_name", name)
    form_data.append("opening_hours", opening_hours)
    form_data.append("webpage_link", web_link)
    form_data.append("library_email", lib_email)
    form_data.append("file", file)
    
   
    
    if(testEmail(lib_email) && checkTime(opening_hours, 0))
    {
        $.ajax({
            type: "POST",
            url: "/admin/editLib/",
            data: form_data,
            dataType: "json",
            contentType: false,
            processData: false,
            cache: false,
            success: function (response) {
                if (response['message'] == 'ok')
                {
                    Toast.show('Úspešna editácia knihovny','S')
                    document.querySelector('.bg-modal-edit').style.display = 'none'
                    delete_inputs()
                    location.reload()
                }    
            }
        });
    } 
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

    delete_inputs()
})


function chechValue(data){

    if (data['library_name'] == "") {
        return "Zadajte názov knihovny"
    } 
    if (data['town'] == "") {
        return "Zadajte názov mesta"
    } 
    if (data['adress'] == "") {
        return "Zadajte adresu"
    } 
    if (data['description'] == "") {
        return "Zadajte popis"
    }
    if (data['opening_hours'] == "") {
        return "Zadajte otváracie hodiny"
    }
    if (data['webpage_link'] == "") {
        return "Zadajte webovú stránku"
    }
    if (data['path_to_picture'] == "") {
        return "Zadajte obrazok"
    }
    if (data['library_email'] == "") {
        return "Zadajte email"
    }
}


// Pridanie knihovne
// Ak bolo stlacene tlacidlo na pridanie
$('#sendAdd').click(function(e){
    var name = $('#nameAdd').val()
    var town = $('#townAdd').val()
    var address = $('#adressAdd').val()
    var description = $('#descriptionAdd').val()
    var opening_hours = $('#opening_hoursAdd').val()
    var web_link = $('#web_linkAdd').val()
    var lib_email = $('#lib_emailAdd').val()
    var file = document.getElementById("path_picAdd").files[0]

    var form_data = new FormData()

    form_data.append("library_name", name)
    form_data.append("town", town)
    form_data.append("adress", address)
    form_data.append("description", description)
    form_data.append("opening_hours", opening_hours)
    form_data.append("webpage_link", web_link)
    form_data.append("library_email", lib_email)
    form_data.append("file", file)
    

    if (testEmail(lib_email) && checkTime(opening_hours, 1)  && checkImage("path_picAdd"))    
    {
        $.ajax({
            type: "POST",
            url: "/admin/addLib/",
            data: form_data,
            dataType: "json",
            contentType: false,
            processData: false,
            cache: false,
            success: function (response) {
                if (response['message'] == 'ok')
                {
                    Toast.show('Úspešna pridanie knihovne','S')
                    document.querySelector('.bg-modal-add').style.display = 'none'
                    delete_inputs()
                    location.reload()
                } else {
                    msg = chechValue(data)
                    Toast.show(msg,'E')
                }
            }
        });
    }
})