$(document).ready(function(){
    $('#registration_form').submit(function(event) {
        event.preventDefault();
        //TODO input validation: regex, check username on change
        var form_data = $(this).serialize();
        var pss = $('#password').val();
        var cnf_pss = $('#password_confirm').val();
        if (pss == cnf_pss) {
            $.ajax({
              type: $(this).attr('method'),
              url: $(this).attr('action'),
              dataType: 'JSON',
              data: $(this).serialize(),
              success: function(data){
                if (data.code == 200){
                    $.toast({
                        text: data.message,
                        allowToastClose: true,
                        loader: false,
                        icon: 'success'
                    });
                }
                else {
                    $.toast({
                        text: data.message,
                        allowToastClose: true,
                        loader: false,
                        icon: 'error'
                    });
                }
              },
              error: function(data){
                $.toast({
                    text: 'Registrazione fallita!',
                    allowToastClose: true,
                    loader: false,
                    icon: 'error'
                });
              }
            });
        }
        else{
            $.toast({
                text: 'La password non é stata confermata correttamente! Controlla.',
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