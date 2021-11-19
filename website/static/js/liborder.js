$('#pub-form .radio-button').on('change',function(){
    var publisher_id = $('.radio-button:checked').val()
    $('.books').html('')
    $.ajax({
        type: "GET",
        url: `/librarian/publisher/books/${publisher_id}/`,
        success: function (response) {
            $("#book-form-header").remove()
            $("#book-form").prepend(`<h1 class="side-header" id="book-form-header">Zaznamenejte poček knih u každé</h1>`)
            $("#confirm").remove()
            $("#book-form").append(`<button class="btn btn-blue" id="confirm">Potrvdit objednávku</button>`)
            let i = 0
            for(const book of response['books']){
                if(i%3 == 0 && i!=0){
                    $('.books').append(`<div class="separator"></div>`)
                }
                insert_this = `
                <div class="number-input-box">
                    <label class="book-label" for="book-${book.title_id}">${book.title_name}</label>
                    <input class="book-number" id="book-${book.title_id}" data-bookid="${book.title_id}" type="number" value="0" min="0">
                </div>
                `
                $('.books').append(insert_this)
                i++
            }
        }
    });
})

$(document).on('click','#confirm',function(e){
    e.preventDefault()
    let order= []
    let id_list= []
    let publisher = $('.radio-button:checked').val()
    $('.book-number').each(function (e) {
        var ids = $(this).attr('id')
        var val = $(this).val()
        if(val != 0){
            order.push(val)
            id_list.push($(this).data('bookid'))
        }
    })
    if (order.length > 0){
        let dataToSend = JSON.stringify({order:order,id_list:id_list,publisher:publisher})
        $.ajax({
            type: "POST",
            url: '/librarian/books/',
            data: dataToSend,
            traditional: true,
            dataType: "json",
            success: function (response) {
                Toast.show("Objednávka byla úspěšně odeslána distributorovi","S")
                $('.books').html('')
                $('.radio-button:checked').prop("checked",false)
            }
        });
    } else {
        Toast.show("V objednávce se nenachází, žádné položky","E")
    }
})

$('.radio-button:checked').prop("checked",false)

$(document).on('change',".book-number",function (e) {
    if($(this).val() < 0){
        $(this).val(0)
    }
})
