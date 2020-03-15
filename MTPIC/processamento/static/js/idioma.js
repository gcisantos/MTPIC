$(function(){

    $(".imagem").click(function(){
        var ling = $(this).attr("id");
        $("body").css("cursor", "progress");
        $.ajax({
            url: '/iniciaServer/',
            type: 'POST',

            data: {'linguagem':ling, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
            dataType: 'json',
            success: function (data) {
                window.location.replace("/inicio/");
            }, timeout: 100000
        }).done(function (data) {
            $("#loading").modal('hide');
            $("body").css("cursor", "default");

        });
    });
})