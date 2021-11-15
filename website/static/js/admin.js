
$('.deleteBtn').click(function(e){
    e.preventDefault()

    var email= {"email" : $(this).data('user')}
    $.ajax({
        type: "POST",
        url: "/admin/delete/",
        data: email,
        dataType: "json",
        success: function (response) {
            alert(response['message'])
        }
    });
})