$(document).ready(function(){
    console.log('sono dentro!');
    $('#login_form').submit(function(event){
        event.preventDefault();
        event.stopPropagation();
        var username = $('#username').val();
        $.ajax({
              type: $(this).attr('method'),
              url: $(this).attr('action'),
              dataType: 'application/json',
              data: $(this).serialize(),
              statusCode: {
                200: function(data) {
                    var response = JSON.parse(data.responseText);
                    if (response.code == 302) {
                        $.toast({
                            text: 'Benvenuto '+username+'!',
                            allowToastClose: true,
                            loader: true,
                            hideAfter: 3000,
                            icon: 'success'
                        });
                        setTimeout(function() {
                            window.location = response.url
                        }, 3000);

                    }
                    else {
                        console.log('Unexepted error')
                        $.toast({
                            text: 'Ci scusiamo per questo problema. Se persiste ci contatti!',
                            allowToastClose: true,
                            loader: false,
                            hideAfter: 4000,
                            icon: 'error'
                        });
                    }
                },
                406: function(data) {
                    $.toast({
                            text: data.statusText+': '+data.responseText,
                            allowToastClose: true,
                            loader: false,
                            hideAfter: 4000,
                            icon: 'error'
                    });
                },
                409: function(data) {
                    $.toast({
                            text: data.statusText+': '+data.responseText,
                            allowToastClose: true,
                            loader: false,
                            hideAfter: 4000,
                            icon: 'error'
                    });
                },
                500: function(data) {
                    $.toast({
                            text: data.statusText+': abbiamo qualche problema interno. Ci scusiamo per il disagio!',
                            allowToastClose: true,
                            loader: false,
                            hideAfter: 4000,
                            icon: 'error'
                    });
                },
                default: function(data) {
                    $.toast({
                            text: 'Stiamo riscontrando delle anomalie. Ci scusiamo per il disagio!',
                            allowToastClose: true,
                            loader: false,
                            hideAfter: 4000,
                            icon: 'error'
                    });
                }

              }
        });

    });
});
