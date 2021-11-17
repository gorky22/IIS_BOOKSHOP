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

    var borId = $(this).attr('id').split("-")[2]
    $.ajax({
        type: "GET",
        url: `/borrow/delay/${borId}/`,
        success: function (response) {
            Toast.show("Vaše výpůjčka byla prodloužena o 10 dní.","S")
            $(`#date-${borId}`).text(response['newtime'])
        }
    });
})