$('#reservation-delete').click(function(e){
    e.preventDefault()
    var resId = $(this).data('res')
    $.ajax({
        type: "GET",
        url: "/librarian/reservations/delete/"+resId+"/",
        success: function (response) {
            Toast.show('Rezervace přesunuta do výpůjček','S')
        }
    });
})