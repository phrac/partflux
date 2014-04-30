$(document).ready(function() {
    $('.modal-form').submit(function() { // catch the form's submit event
        $('.modal-form-submit').button('loading');

        var successTitle = $(this).attr('data-gritter-title-success');
        var successMsg = $(this).attr('data-gritter-msg-success');
        var errorTitle = $(this).attr('data-gritter-title-error');
        var divUpdate = $(this).attr('data-div-update');
        var formReset = $(this).attr('data-form-reset');

        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success..
                console.log(response);
                $('.modal').modal('hide');
                if(!formReset) {
                    $('.modal-form').each(function() {
                        this.reset();
                    });
                };
                if(divUpdate){
                    $(divUpdate).hide().html(response).fadeIn("slow");
                };
                $('button').button('reset');
                $('.control-group').removeClass('success');
                $('.control-group').removeClass('error');
            },
            error: function(xhr, textStatus, error) {
                $('.modal').modal('hide');
                $('button').button('reset');
                $('.control-group').removeClass('success');
                $('.control-group').removeClass('error');

            }
        });
        return false;
    });
});
