$('.delete-book').click(function(e){
    e.preventDefault()
    let bookid = $(this).data('book')
    insert_this = `
    <h1 class="popup-header">Opravdu chcete knihu smazat?</h1>
            <div class="btn-row">
                <button class="popup-button close" id="close">Zavřít</button>
                <button class="popup-button confirm" id="popup-del-book" data-book=${bookid}>Smazat knihu</button>
            </div>
    `
    PopUp.show(insert_this)
})
$(document).on('click','#close',function(e){
    PopUp.hide()
})
$(document).on('click','#popup-del-book',function(e){
    e.preventDefault()

    let bookid = $(this).data('book')

    $.ajax({
        type: "GET",
        url: `/distributor/bookdelete/${bookid}/`,
        success: function (response) {
            Toast.show('Kniha byla smazána.','S')
            $(`#book-${bookid}`).remove()
            PopUp.hide()
        }
    });
})