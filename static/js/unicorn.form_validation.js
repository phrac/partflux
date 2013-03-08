/**
 * Unicorn Admin Template
 * Diablo9983 -> diablo9983@gmail.com
 **/
$(document).ready(function(){


    $('select').select2();

    // Form Validation
    $("#flag-form").validate({
        rules:{
            reason:{
                required:true,
        minlength:10
            },
        },
        errorClass: "help-inline",
        errorElement: "span",
        highlight:function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $("#buylink-form").validate({
        rules:{
            url:{
                required: true,
        url: true
            },
        company:{
            required: true,
        maxlength: 64,
        minlength: 2
        },
        price:{
            required: true,
        number: true,
        min: .0001
        }
        },
        errorClass: "help-inline",
        errorElement: "span",
        highlight:function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $("#attribute-form").validate({
        rules:{
            key:{
                required: true,
                minlength:4,
                maxlength:64
            },
            value:{
                required:true,
                minlength:2,
                maxlength:128,
            }
        },
        errorClass: "help-inline",
        errorElement: "span",
        highlight:function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $("#image-form").validate({
        rules:{
            file:{
                required: true,
                accept: "png|jpe?g|gif"
            }
        },
        errorClass: "help-inline",
        errorElement: "div",
        highlight:function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $("#xref-form").validate({
        rules:{
            part:{
                required: true,
                minlength: "2",
                maxlength: 64
            },
            company:{
                required: true,
                minlength: 2,
                maxlength: 64
            },
            desc:{
                required: true,
                minlength: 10,
                maxlength: 256
            }
        },
        errorClass: "help-inline",
        errorElement: "div",
        highlight:function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $('.modal-form').bind('change keyup', function() {
        if($(this).validate().checkForm()) {
            $('.modal-form-submit').attr('disabled', false);
        } else {
            $('.modal-form-submit').attr('disabled', true);
        }
    });
});
