// Odstranenie tagu
// ak bolo stlacene tlacidlo Exit schova sa Pop Up okno
document.querySelector('.btnClose').addEventListener('click', function() {
    document.querySelector('.bg-modal-delete').style.display = 'none'
})


// Odstranenie tagu
// ak bolo stlacene tlacidlo Nie schova sa Pop up okno
document.getElementById('btnNo').addEventListener('click', function() {
    document.querySelector('.bg-modal-delete').style.display = 'none'
})


// Tlacidlo na odstranenie tagu
$('.deleteBtn').click(function(e){
    e.preventDefault()

    var tmp = {"name" : $(this).data('tag')}
    let name  = tmp['name']

    var tag = {"id" : $(this).data('id')}
    var tag_id = tag['id']

    document.getElementById('deleteTag').innerHTML = name
    document.getElementById('idTag').innerHTML = tag_id
   

    // Zobrazi sa Pop Up okno
    document.querySelector('.bg-modal-delete').style.display = 'flex'
})


// Odstranenie tagu
// Ak bolo stlacene tlacidlo ANO
document.getElementById('btnYes').addEventListener('click', function() {
    var tag_id = document.getElementById('idTag').innerHTML

    var data = {"genre_id" : tag_id}
    $.ajax({
        type: "POST",
        url: "/admin/deleteTag/",
        data: data,
        dataType: "json",
        success: function (response) {
            if (response['message'] == 'ok')
            {
                Toast.show('Uspešne si odstránil Tag','S')
                location.reload()
            }                
        }
    });
    document.querySelector('.bg-modal-delete').style.display = 'none'
})


// Editacia tagu 
// Tlacidlo na editovanie knihovne 
$('.editBtn').click(function(e){
    e.preventDefault()
    
    var id =  $(this).data('id')
    $.ajax({
        type: "GET",
        url: "/admin/tags/"+id,
        success: function (response) {
            var tag = response['tag']

            document.getElementById('name').innerHTML = tag['name']
            document.getElementById('idTagEdit').innerHTML = id

            $('#nameI').attr('placeholder', tag['name'])

            // Zobrazi sa Pop Up okno na editaciu            
            document.querySelector('.bg-modal-edit').style.display = 'flex'
        }
    });
})

// Editacia tagu
// Ak bolo stlacene tlacidlo exit
document.querySelector('.btnCloseEdit').addEventListener('click', function() {
    document.querySelector('.bg-modal-edit').style.display = 'none'

    document.getElementById('nameI').value = ""


})


// Editacia tagu
// Ak bolo stlacene tlacidlo na ulozenie zmien
$('#sendEdit').click(function(e){
    var id = document.getElementById('idTagEdit').innerHTML
    var name = $('#nameI').val()
   
    var data = {
        "genre_id" : id,
        "name" : name,
    }

    $.ajax({
        type: "POST",
        url: "/admin/editTag/",
        data: data,
        dataType: "json",
        success: function (response) {
            if (response['message'] == 'ok')
            {
                Toast.show('Úspešna editácia tagu','S')
                document.querySelector('.bg-modal-edit').style.display = 'none'

                document.getElementById('nameI').value = ""

                location.reload()
            }    
        }
    });
})



// Tlacidlo na pridanie tagu
$('#btnAddTag').click(function(e){
    e.preventDefault()
   
    // Zobrazi sa Pop Up okno
    document.querySelector('.bg-modal-add').style.display = 'flex'
})



// Pridanie tagu
// ak bolo stlacene tlacidlo Exit schova sa Pop Up okno
document.querySelector('.btnCloseAdd').addEventListener('click', function() {
    document.querySelector('.bg-modal-add').style.display = 'none'

    document.getElementById('nameAdd').value = ""

})


// Pridanie tagu
// Ak bolo stlacene tlacidlo na pridanie
$('#sendAdd').click(function(e){

    var name = $('#nameAdd').val()

    data = {
        "name" : name,
    }

    $.ajax({
        type: "POST",
        url: "/admin/addTag/",
        data: data,
        dataType: "json",
        success: function (response) {
            if (response['message'] == 'ok')
            {
                Toast.show('Úspešné pridanie tagu','S')
                document.querySelector('.bg-modal-add').style.display = 'none'
                document.getElementById('nameAdd').value = ""

                location.reload()
            } else {
                Toast.show('Zadaj nazov','E')
            }


        }
    });
})