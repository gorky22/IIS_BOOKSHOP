$('.roll-down').click(function(){

    var id = "#" + $(this).attr('id') +"-show"
    console.log(id)
    if($(id).data('open') == "0"){
        $(id).show()
        $(id).data('open','1')
    } else { 
        $(id).hide()
        $(id).data('open','0')
    }
})

$('.time-btn').click(function (e) {
    e.preventDefault()

    var resId = $(this).attr('id').split("-")[2]
    $.ajax({
        type: "GET",
        url: `/reservation/delay/${resId}/`,
        success: function (response) {
            Toast.show("Vaše rezervace byla prodloužena o 10 dní.","S")
            $(`#date-${resId}`).text(response['newtime'])
        }
    });
})