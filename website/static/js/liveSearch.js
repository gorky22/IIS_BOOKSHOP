var textSearch = ''
$(document).ready(function(){
    $('#searchBox').keyup(function(e){
        var find = new RegExp('.*'+$(this).val().toLowerCase()+".*")
        if($(this).val().length > textSearch.length){
            // prodlouzil se text - oddelavam ty co nesplnuji regex
            textSearch = $(this).val()
            $('.row').each(function(i,obj){
                if(!$(this).hasClass('not-display')){
                    var text = $(this).find('.liveSearchEmail').text().toLowerCase()
                    console.log(text)
                    //console.log(text + "---------" + textSearch)
                    if(!text.match(find))
                        $(this).addClass('not-display')
                }
            })
        } else {
            // text se zkratil kontroluji ty co maji not displayed a chci je zviditelnit
            textSearch = $(this).val()
            $('.row').each(function(i,obj){
                if($(this).hasClass('not-display')){
                    var text = $(this).find('.liveSearchEmail').text().toLowerCase()
                    if(text.match(find))
                        $(this).removeClass('not-display')
                }
            })
        }
    })
})