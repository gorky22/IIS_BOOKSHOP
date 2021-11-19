var textSearch = ''
$(document).ready(function(){
    $('#live-search').keyup(function(e){
        console.log($(this).val().toLowerCase())
        var find = new RegExp('.*'+$(this).val().toLowerCase()+".*")
        if($(this).val().length > textSearch.length){
            // prodlouzil se text - oddelavam ty co nesplnuji regex
            textSearch = $(this).val()
            $('.book-div').each(function(i,obj){
                if(!$(this).hasClass('book-botDisplayed')){
                    var text = $(this).find('.book-header').text().toLowerCase()
                    console.log(text)
                    if(!text.match(find))
                        $(this).addClass('book-botDisplayed')
                }
            })
        } else {
            // text se zkratil kontroluji ty co maji not displayed a chci je zviditelnit
            textSearch = $(this).val()
            $('.book-div').each(function(i,obj){
                if($(this).hasClass('book-botDisplayed')){
                    var text = $(this).find('.book-header').text().toLowerCase()
                    if(text.match(find))
                        $(this).removeClass('book-botDisplayed')
                }
            })
        }
    })
})