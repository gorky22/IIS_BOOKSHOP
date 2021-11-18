$(".confirm-votes").click(function(e){
    let book_id = $(this).data('book')
    $.ajax({
        type: "GET",
        url: `/librarian/confirm/votes/${book_id}/`,
        success: function (response) {
            if(response['err']){
                Toast.show(response['msg'],'E')
            } else {
                Toast.show('Toto hlasování úspěšně skončilo. Knihu jste již zakoupili','S')
                $(`#book-${book_id}`).remove()
            }
            
        }
    });
})