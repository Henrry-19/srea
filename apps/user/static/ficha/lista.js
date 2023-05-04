$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "dni"},
            {"data": "user"},        //[-6]
            {"data": "birthday"},
            {"data": "genero"},
            {"data": "direccion"},
            {"data": "estado_civil"},
            {"data": "position"},
        ],
        columnDefs: [ 
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    html += '<span class="badge badge-success">' + row.user + '</span> ';
                    return html;
                }
            },          
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/user/ficha_list/u_ficha/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/user/ficha_list/d_ficha/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    buttons += ' <a href="/user/ficha_list/pdf/' + row.id + '/" target="_blank" type="button" class="btn btn-info btn-xs btn-flat"><i class="fa fa-file-pdf"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});