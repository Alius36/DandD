$(document).ready(function(){
   $('#logout').on('click', function () {
       $.ajax({
              type: 'POST',
              url: $(this).attr('data-url'),
              dataType: 'application/json',
              statusCode: {
                200: function(data) {
                    var response = JSON.parse(data.responseText);
                    if (response.code == 302) {
                        $.toast({
                            text: 'Logout effettuato con successo!',
                            allowToastClose: true,
                            loader: true,
                            hideAfter: 2000,
                            icon: 'success'
                        });
                        setTimeout(function() {
                            window.location = response.url
                        }, 2000);

                    }
                    else {
                        $.toast({
                            text: 'Ci scusiamo per questo problema. Se persiste ci contatti!',
                            allowToastClose: true,
                            loader: false,
                            hideAfter: 4000,
                            icon: 'error'
                        });
                    }
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
   })
});