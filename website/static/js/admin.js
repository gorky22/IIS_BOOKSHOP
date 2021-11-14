
$('.deleteBtn').click(function(e){
    e.preventDefault()

    var name= {"name" : $(this).data('user')}
    $.ajax({
        type: "POST",
        url: "/admin/delete/",
        data: name,
        dataType: "json",
        success: function (response) {
            alert(response['name'])
        }
    });
})