var static_combo = $('#combobox-1').clone()
var static_author = $("#new-author-1").clone()

let curr_combo_id = parseInt($('.author-combo').last().data('count'))

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



var title_name_original = $('#title_name').val()
var date_original = $("#realease").val()
var isbn_original = $("#isbn").val()
var description_original = $("#description").val()
var authors_original = []
$('.author-combo').each(function(e){
    authors_original.push($(this).find('option:selected').val())
})

var genres_original = []
$('.genres').each(function(e){
    if($(this).is(":checked")){
        genres_original.push($(this).data('genre'))
    }
})

$("#title_name").keyup(function (e) { 
    if(title_name_original != $(this).val()){
        $(this).addClass("input-changed")
    } else {
        $(this).removeClass("input-changed")
    }
});

$("#realease").change(function (e) { 
    if(date_original != $(this).val()){
        $(this).addClass("input-changed")
    } else {
        $(this).removeClass("input-changed")
    }
});
$("#isbn").keyup(function (e) { 
    if(isbn_original != $(this).val()){
        $(this).addClass("input-changed")
    } else {
        $(this).removeClass("input-changed")
    }
});
$("#description").keyup(function (e) { 
    if(description_original != $(this).val()){
        $(this).addClass("input-changed")
    } else {
        $(this).removeClass("input-changed")
    }
});
document.getElementById("file-preview").style.display = "block";
var imgChanged = false
function showPreview(event){
    if(event.target.files.length > 0){
      var src = URL.createObjectURL(event.target.files[0]);
      var preview = document.getElementById("file-preview");
      preview.src = src;
      preview.style.display = "block";
      imgChanged=true
    }
}

$(document).on('click','#confirm-button',function (e) {
    e.preventDefault()
    var form_data = new FormData()

    var title_name = $('#title_name').val()
    var date = $("#realease").val()
    var isbn = $("#isbn").val()
    var description = $("#description").val()

    if(title_name == "" || date == "" || isbn == "" || description == ""){
        Toast.show("Musíte zadat všechny potřebné hodnoty (Jméno, Datum, ISBN, Popis knihy)","E",4000)
        return
    }
    form_data.append("title_name",title_name)
    form_data.append("date",date)
    form_data.append("isbn",isbn)
    form_data.append("description",description)

    var authors_ids = [];
    var new_authors = [];
    var delete_authors = [];
    var names = []
    var surnames = []

    $('.author-combo').each(function(e){
        authors_ids.push($(this).find('option:selected').val())
    })
    if(authors_ids.length !== new Set(authors_ids).size){
        Toast.show("Nelze přidat dva stejné autory k jedné knížce.","E",4000)
        return
    }

    authors_ids.forEach(function(item, index){
        if(!authors_original.includes(item)){
            new_authors.push(item)
        }
    })
    authors_original.forEach(function(item,index){
        if(!authors_ids.includes(item)){
            delete_authors.push(item)
        }
    })

    $('.input-name').each(function(e){
        if($(this).val() != '')
            names.push($(this).val())
    })
    $('.input-surname').each(function(e){
        if($(this).val() != '')
            surnames.push($(this).val())
    })

    if(new_authors.length > 0){
        form_data.append("new_author_ids[]",new_authors)
    }
    if(delete_authors.length > 0){
        form_data.append("delete_author_ids[]",delete_authors)
    }

    if(names.length != surnames.length){
        Toast.show("Každý autor musí mít jméno i příjmení.","E")
        return
    }
    if(names.length == 0 && authors_ids.length == 0){
        Toast.show("Kniha musí mít alespoň jednoho autora.","E")
        return
    }

    if(names.length > 0){
        form_data.append("names[]",names)
    }
    if(surnames.length > 0){
        form_data.append("surnames[]",surnames)
    }

    
    var ins = document.getElementById("title_picture").files.length

    if(imgChanged){
        var data = document.getElementById("title_picture").files[0]
        form_data.append("file",data)
    }

    var genre_ids = []

    $('.genres').each(function(e){
        if($(this).is(":checked")){
            genre_ids.push($(this).data('genre'))
        }
    })
    var new_genre_ids = []
    var delete_genre_ids = []
    genre_ids.forEach(function(item,index){
        if(!genres_original.includes(item)){
            new_genre_ids.push(item)
        }
    })
    genres_original.forEach(function(item,index){
        if(!genre_ids.includes(item)){
            delete_genre_ids.push(item)
        }
    })
    if(new_genre_ids.length > 0){
        form_data.append("new_genres[]",new_genre_ids)
    }
    if(delete_genre_ids.length > 0){
        form_data.append("delete_genres[]",delete_genre_ids)
    }
    console.log(new_genre_ids)
    console.log(delete_genre_ids)
    let title_id = $('.book-form').attr('id')
    
    $.ajax({
        type: "POST",
        url: `/distributor/bookedit/${title_id}/`,
        data: form_data,
        dataType: "json",
        contentType: false,
        processData: false,
        cache: false,
        success: function (response) {
            Toast.show("Kniha byla úspěšně upravena.","S",2000)
            setTimeout(() => {
                window.location.href = response['url'];
             },2000)
        },
        error: function(response){
            Toast.show("Něco se stalo, kniha se nepodařila upravit.","E",2000)
        }
    });

})