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
            {"data": "titulo"},
            {"data": "descripcion"},
            {"data": "fecha"},
            {"data": "unidad"},
            {"data": "position"}

        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.unidad, function (key, value) {
                        html += '<span class="badge badge-success">' + value.nombre + '</span> ';
                    });
                    return html;
                }
            },

            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    buttons += '<a href="/srea/pregunta/" type="button" class="btn btn-accent-blue btn-accent-gray"><i class="fa fa-plus-square">Agregar pregunta</i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});