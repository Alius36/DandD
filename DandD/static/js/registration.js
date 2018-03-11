$(document).ready(function(){
    $('#registration_form').submit(function(event) {
        event.preventDefault();
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
                $.toast(data.message);
              },
              error: function(data){
                $.toast(data.message);
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
});