$(document).ready(function() {
    $('.modal-form').submit(function() { // catch the form's submit event
        $('.modal-form-submit').button('loading');

        var successTitle = $(this).attr('data-gritter-title-success');
        var successMsg = $(this).attr('data-gritter-msg-success');
        var errorTitle = $(this).attr('data-gritter-title-error');
        var divUpdate = $(this).attr('data-div-update');

        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success..
                $('.modal').modal('hide');
                $('.modal-form').each(function() {
                    this.reset();
                });
                if(divUpdate){
                    $(divUpdate).hide().html(response).fadeIn("slow");
                };
                $.gritter.add({
                    title: successTitle,
                    text: successMsg,
                    sticky: false
                });
                $('button').button('reset');
                $.getScript('/static/js/unicorn.tables.js');
            },
            error: function(xhr, textStatus, error) {
                $('.modal').modal('hide');
                $.gritter.add({
                    title: errorTitle,
                    text: 'There was an error: ' + xhr.responseText,
                    sticky: false
                });
                $('button').button('reset');
                
            }
        });
        return false;
    });
});
