$('#rate').click(function(e){
    e.preventDefault()
    insert_this = `
    <h1 class="popup-header">Ohodnoťte knihu</h1>
            <p class="popup-text">Hodnocená kniha: <span class="popup-bold">${$('.book-header-detail').text()}</span></p>
            <input type="range" min="0" max="10" value="5" step="0.1" class="slider" id="rating">
            <div class="btn-row">
                <button class="popup-button close" id="close">Zavřít</button>
                <button class="popup-button confirm" id="confirm-rating">ohodnotit</button>
            </div>
    `
    PopUp.show(insert_this)
})

$(document).on('click','#close',function(e){
    e.preventDefault()
    PopUp.hide()
})

$(document).on('click',"#confirm-rating",function(e){
    let value = $("#rating").val()
    let old_value = $("#old-rating").text()
    let id_book = $("#res-combobox").data('book')

    var data = {'value': value, 'old_value' : old_value,'title_id': id_book}
    $.ajax({
        type: "POST",
        url: "/rate/book/",
        data: data,
        dataType: "json",
        success: function (response) {
            if(response['err']){
                Toast.show(response['msg'],'E')
            }else {
                $("#old-rating").text(response['new_value'])
                $("#detail-rating").attr('src',response['path_to_image'])
                PopUp.hide()
                Toast.show('Hodnocení bylo přidáno','S')
                
            }
        }
    });
})