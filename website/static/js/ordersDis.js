$('.roll-down').click(function(e){
    e.preventDefault()
    var rollID ="#"+$(this).data('bottom')
    console.log(rollID)
    if($(rollID).data('open') == "0"){
        $(rollID).show()
        $(rollID).data('open','1')
    } else {
        $(rollID).hide()
        $(rollID).data('open','0')
    }
})

$(".check").click(function(e){
    let id = $(this).data('order')
    let insert_this = `
    <h1 class="popup-header">Potvrdit objednávku?</h1>
            <div class="btn-row">
                <button class="popup-button close" id="close">Zavřít</button>
                <button class="popup-button confirm" id="popup-confirm" data-order=${id}>Potvrdit</button>
            </div>
    `
    PopUp.show(insert_this)
})

$(document).on('click','#close',function(e){
    PopUp.hide()
})
$(document).on('click','#popup-confirm',function(e){
    e.preventDefault()
    var orderId = $(this).data('order')
    document.body.style.cursor='wait';
    $(this).css('cursor','wait')
    
    $.ajax({
        type: "GET",
        url: `/distributor/order/confirm/${orderId}/`,
        success: function (response) {
            document.body.style.cursor='default';
            $('.popup-button.confirm').css('cursor','default')
            Toast.show('Objednávka byla potvrzena.','S')
            PopUp.hide()
            $(`#order-box-${response['order']}`).remove()
            
        }
    });
})

/*
e.preventDefault()
    
*/
