$(document).ready(function(){
    $('#registration_form').submit(function(event) {
        event.preventDefault();
        event.stopPropagation();
        //TODO input validation: regex, check username on change
        var pss = $('#password').val();
        var cnf_pss = $('#password_confirm').val();
        if (pss == cnf_pss) {
            $.ajax({
              type: $(this).attr('method'),
              url: $(this).attr('action'),
              header: {
                'Accept': 'application/json'
              },
              dataType: 'application/json',
              data: $(this).serialize(),
              statusCode: {
                200: function(data) {
                    $.toast({
                        text: data.statusText+': '+data.responseText,
                        allowToastClose: true,
                        loader: false,
                        icon: 'success'
                    });
                },
                406: function(data) {
                    $.toast({
                        text: data.statusText+': '+data.responseText,
                        allowToastClose: true,
                        loader: false,
                        icon: 'error'
                    });
                },
                409: function(data) {
                    $.toast({
                        text: data.statusText+': '+data.responseText,
                        allowToastClose: true,
                        loader: false,
                        icon: 'error'
                    });
                },
                500: function(data) {
                    $.toast({
                        text: data.statusText+': abbiamo qualche problema interno. Ci scusiamo per il disagio!',
                        allowToastClose: true,
                        loader: false,
                        icon: 'error'
                    });
                },
                default: function(data) {
                    $.toast({
                            text: 'Stiamo riscontrando delle anomalie. Ci scusiamo per il disagio!',
                            allowToastClose: true,
                            loader: false,
                            icon: 'error'
                    });
                }
              }
            });
        }
        else {
            $.toast({
                text: 'La password non é stata confermata correttamente! Riprova.',
                allowToastClose: true,
                loader: false,
                icon: 'error'
            })
        }
    });

//$('#username').on('input', function(e) {
//    console.log('editing')
//    // Ottengo lista username e confronto
//    $(this).css('border-color','#d81c1c');
//});

});