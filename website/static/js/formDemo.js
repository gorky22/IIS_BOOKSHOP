$("#submit-button").click(function(e){
    e.preventDefault()

    
    var text = $("#text").val()
    console.log(text)
    var data = {"text" : text}
    $.ajax({
        type: "POST",
        url: "/form/demo/",
        data: data,
        dataType: "json",
        success: function (response) {
            
        }
    });
})