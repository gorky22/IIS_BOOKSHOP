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




function showPreview(event){
    if(event.target.files.length > 0){
      var src = URL.createObjectURL(event.target.files[0]);
      var preview = document.getElementById("file-preview");
      preview.src = src;
      preview.style.display = "block";
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
        Toast.show("Musíte přidat všechny potřebné hodnoty (Jméno, Datum, ISBN, Popis knihy)","E",4000)
        return
    }
    form_data.append("title_name",title_name)
    form_data.append("date",date)
    form_data.append("isbn",isbn)
    form_data.append("description",description)

    var authors_ids = [];
    var names = []
    var surnames = []
    $('.author-combo').each(function(e){
        authors_ids.push($(this).find('option:selected').val())
    })
    if(authors_ids.length !== new Set(authors_ids).size){
        Toast.show("Nelze přidat dva stejné autory k jedné knížce.","E",4000)
        return
    }
    $('.input-name').each(function(e){
        if($(this).val() != '')
            names.push($(this).val())
    })
    $('.input-surname').each(function(e){
        if($(this).val() != '')
            surnames.push($(this).val())
    })

    if(authors_ids.length > 0){
        form_data.append("author_ids[]",authors_ids)
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
    var genres_ids = []
    $('.genres').each(function(e){
        if($(this).is(":checked")){
            genres_ids.push($(this).data('genre'))
        }
    })
    if(genres_ids.length > 0){
        form_data.append("genres[]",genres_ids)
    } else {
        Toast.show("Prosím vyberte alespoň jeden žánr pro tuto knihu.","E")
        return
    }



    var ins = document.getElementById("title_picture").files.length
    console.log(ins)
    if(ins == 0){
        Toast.show("Musíte zadat obrázek obalu knížky","E")
    } else {
        var data = document.getElementById("title_picture").files[0]
        form_data.append("file",data)
    }

    $.ajax({
        type: "POST",
        url: "/distributor/books/",
        data: form_data,
        dataType: "json",
        contentType: false,
        processData: false,
        cache: false,
        success: function (response) {
            Toast.show("Kniha byla úspěšně přidána do databáze.","S",2000)
            setTimeout(() => {
                window.location.href = response['url'];
             },2000)
        },
        error: function(response){
            Toast.show("Něco se stalo, kniha nemohla být přidána do databáze.","E",2000)
        }
    });

})