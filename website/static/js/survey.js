$('.book-btn').click(function(e){
    let libid = $('.library-name').data('lib')
    let title_id = $(this).attr('id')
    let data = {'lib_id':libid,'title_id':title_id}
    $.ajax({
        type: "POST",
        url: `/surveys/${libid}/`,
        data: data,
        dataType: "json",
        success: function (response) {
            if(response['err']){
                Toast.show(response['msg'],'E')
            } else {
                Toast.show("Vaše odpověď byla zaznamenána","S")
            }
        },
        error: function (response) {
            Toast.show("Na tuto operaci nemáte práva",'E')
        }
    });
})