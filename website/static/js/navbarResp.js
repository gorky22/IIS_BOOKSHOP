
var opened= false;


function showNavbar(){
    $('.nav-box').show(200)
    $('.hamburger-btn').css('left','81vw')
    $('#hamburger').hide()
    $('#cross').show()
}

function hideNavbar(){
    $('.nav-box').hide(200)
    $('.hamburger-btn').css('left','1rem')
    $('#cross').hide()
    $('#hamburger').show()
}
$('#cross').hide()
$('#btn-menu').click(function(e){
    if(!opened){
        showNavbar()
    } else {
        hideNavbar()
    }
    opened = !opened;
})