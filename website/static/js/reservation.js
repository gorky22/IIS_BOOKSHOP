$('#reservation').click(function(e){
    //isbookAvailible/<bookid>/<libid>/
    let libraryID = $('#res-combobox').find('option:selected').val()
    let bookID = $('#res-combobox').data('book');
    $.ajax({
        type: "GET",
        url: "/isbookAvailible/"+bookID+"/"+libraryID+"/",
        success: function (response) {
            let insert_this;

            if(response['answer']){
                
                insert_this = `
                <h1 class="popup-header">Potvrďte prosím rezervaci</h1>
                        <p class="popup-text">Požadovaná kniha: <span class="popup-bold">${$('.book-header-detail').text()}</span></p>
                        <p class="popup-text"> Kniha bude rezervována v: <span class="popup-bold">${$('#res-combobox').find('option:selected').text()}</span></p>
                        <div class="btn-row">
                            <button class="popup-button close" id="close">Zavřít</button>
                            <button class="popup-button confirm" id="confirm">Závazně rezervuji</button>
                        </div>
                `
            } else {
                if(response['res_bor']){
                    Toast.show(response.msg,'E')
                    return
                }
                insert_this = `
                <h1 class="popup-header">Kniha není k dispozici</h1>
                        <p class="popup-text">Chcete zařadit do fronty rezervací pro tuto knihu?</p>
                        <div class="btn-row">
                            <button class="popup-button close" id="close">Zavřít</button>
                            <button class="popup-button confirm" id="confirm-que">Zařadit do fronty</button>
                        </div>
                `
            }
            PopUp.show(insert_this)
        }
    });
    
    
})

$(document).on('click','#close',function(){
    PopUp.hide()   
})

$(document).on('click','#confirm',function(){
    let libraryID = $('#res-combobox').find('option:selected').val()
    let bookID = $('#res-combobox').data('book');
    let data = {'lib':libraryID}
    $.ajax({
        type: "POST",
        url: "/detail/"+bookID+"/",
        data: data,
        dataType: "json",
        success: function (response) {
            PopUp.hide()
            if(!response['err']){
                Toast.show('Rezervace byla úspěšná. Byla vložena do vašich rezervací','S')
            } else {
                Toast.show(response['msg'],'E')
            }
        }
    });
})

$(document).on('click','#confirm-que',function(){
    let libraryID = $('#res-combobox').find('option:selected').val()
    let bookID = $('#res-combobox').data('book');
    let data = {'lib':libraryID,'book':bookID}
    $.ajax({
        type: "POST",
        url: "/addToQue/",
        data: data,
        dataType: "json",
        success: function (response) {
            PopUp.hide()
            if(!response['err']){
                Toast.show('Úspěšně jste byl přidán do fronty rezervací, knihovník vás bude informovat o dalším stavu rezervace','S',4000)
            } else {
                Toast.show(response['msg'],'E',3000)
            }
        }
    });
})
