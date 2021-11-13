
var opened= false;


$('#btn-menu').click(function(e){
    if(!opened){
        $('.nav-box').show(400)
    } else {
        $('.nav-box').hide(400)
    }
    opened = !opened;
})