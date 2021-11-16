$('#reservation').click(function(e){
    
    let libraryID = $('#res-combobox').find('option:selected').val()
    let bookID = $('#res-combobox').data('book');
    let data = {'lib':libraryID}
    $.ajax({
        type: "POST",
        url: "/detail/"+bookID+"/",
        data: data,
        dataType: "json",
        success: function (response) {
            if(!response['err']){
                Toast.show('Rezervace byla úspěšná. Byla vložena do vašich rezervací','S')
            } else {
                Toast.show(response['msg'],'E')
            }
        }
    });
})