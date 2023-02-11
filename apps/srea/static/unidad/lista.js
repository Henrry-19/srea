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
            {"data": "nombre"},
            {"data": "descripcion"},
            {"data": "asignaturas"},
            {"data": "test"},
            {"data": "position"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.asignaturas, function (key, value) {
                        html += '<span class="badge badge-success">' + value.nombre + '</span> ';
                    });
                    return html;
                }
            },

            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.test, function (key, value) {
                        html += '<span class="badge badge-success">' + value.titulo + '</span> ';
                    });
                    return html;
                }
            },

            /*{
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    html += '<span class="badge badge-success">' + row.curso + '</span> ';
                    return html;
                }
            },*/
            
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    //if (row.is_staff) {//
                        var buttons = '<a href="/srea/u_unidad/act_unidad/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/srea/u_unidad/d_unidad/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                   /* } else{
                        var buttons = '<span class="badge badge-accent-dark">' + row.email + '</span> ';
                    }*/
                    
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});