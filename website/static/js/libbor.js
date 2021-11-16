$('.confirm-bor').click(function(e){
    e.preventDefault()
    let borId = $(this).data('bor')
    insert_this = `
                <h1 class="popup-header">Skutečně chcete výpůjčku ukončit?</h1>
                        <div class="btn-row">
                            <button class="popup-button close" id="close">Zavřít</button>
                            <button class="popup-button confirm" id="popup-del-bor" data-bor=${borId}>Ukončit výpůjčku</button>
                        </div>
                `
    PopUp.show(insert_this)
})




$(document).on('click','#close',function(e){
    PopUp.hide()
})
$(document).on('click','#popup-del-bor',function(e){
    bor_id = $(this).data('bor')
    $.ajax({
        type: "GET",
        url: `/librarian/borrowed/delete/${bor_id}/`,
        success: function (response) {
            $(`#bor-num-${bor_id}`).remove()
            PopUp.hide()
            Toast.show('Kniha byla úspěšně vrácena.','S')
        }
    });
})