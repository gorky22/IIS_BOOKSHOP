var static_combo = $('#combobox-1').clone()
var static_author = $("#new-author-1").clone()

let curr_combo_id = 1
let curr_auth_id = 1

$(document).on('click','#add-author-button',function (e){
    e.preventDefault()
    let new_combo = static_combo.clone()
    new_combo.attr('id',`combobox-${curr_combo_id+1}`)
    if(curr_combo_id == 0){
        $(".combo-label").after(new_combo)
    } else {
        $(`#combobox-${curr_combo_id}`).after(new_combo)
    }
    
    
    
    curr_combo_id++;
})
$(document).on('click','#delete-author-button',function (e){
    e.preventDefault()
    if(curr_combo_id > 0){
        $(`#combobox-${curr_combo_id}`).remove()
        curr_combo_id--;
    }
})

// add-new-author-button -tlacitko
// delete-new-author-button - tlacitko

$(document).on('click',"#add-new-author-button",function (e) {
    e.preventDefault()
    let new_name_surname = static_author.clone()
    new_name_surname.attr('id',`new-author-${curr_auth_id+1}`)
    new_name_surname.find(`#name-${curr_auth_id}`).attr('id',`name-${curr_auth_id+1}`)
    new_name_surname.find(`#surname-${curr_auth_id}`).attr('id',`surname-${curr_auth_id+1}`)
    if (curr_auth_id == 0){
        
        $(`.new-author`).after(new_name_surname)

    } else {
        $(`#new-author-${curr_auth_id}`).after(new_name_surname)
    }  
    curr_auth_id++;

})
$(document).on('click','#delete-new-author-button',function (e){
    e.preventDefault()
    if(curr_auth_id > 0){
        $(`#new-author-${curr_auth_id}`).remove()
        curr_auth_id--;
    }
})