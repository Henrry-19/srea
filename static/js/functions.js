function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}


function ajax_alert_jqueryconfirm(url, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: 'Confirmación',
        icon: 'fa fa-info',
        content: '¿Estás seguro de realizar la siguiente acción?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {

                    $.ajax({
                        url: url,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json'
                    }).done(function (data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });

                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }

    })


}