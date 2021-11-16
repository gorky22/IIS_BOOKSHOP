$('.delete-res').click(function(e){
    e.preventDefault()
    let resId = $(this).data('res')
    insert_this = `
                <h1 class="popup-header">Skutečně chcete rezervaci ukončit?</h1>
                        <div class="btn-row">
                            <button class="popup-button close" id="close">Zavřít</button>
                            <button class="popup-button confirm" id="popup-del-res" data-res=${resId}>Smazat</button>
                        </div>
                `
    PopUp.show(insert_this)
})
$('.confirm-res').click(function(e){
    e.preventDefault()
    let resId = $(this).data('res')
    let library_id = $("#library-res-table").data('library')
    let user_id = $(`#res-num-${resId}`).data('user')
    let book_id = $(`#res-num-${resId}`).data('book')

    var data = {
        'library_id':library_id,
        'user_id':user_id,
        'title_id':book_id,
        'res_id':resId
    }
    $.ajax({
        type: "POST",
        url: `/librarian/reservations/confirm/${resId}/`,
        data: data,
        dataType: "json",
        success: function (response) {
            resId = response['resToDelete']
            $(`#res-num-${resId}`).remove()
            Toast.show(`Rezervace s číslem ${resId} byla úspěšně přesunuta do výpůjček.`,'S',4000)
        }
    });
})




$(document).on('click','#close',function(e){
    PopUp.hide()
})





$(document).on('click','#popup-del-res',function(e){
    let resID = $(this).data('res')
    // /reservations/delete/<resid>/
    $.ajax({
        type: "GET",
        url: `/librarian/reservations/delete/${resID}/`,
        success: function (response) {
            PopUp.hide()
            Toast.show(`Rezervace s číslem ${resID} byla úspěšně vymazána.`,'S')
            $(`#res-num-${resID}`).remove();
        }
    });
})




