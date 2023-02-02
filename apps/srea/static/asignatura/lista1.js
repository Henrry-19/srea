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
            
            {"data": "id"},
            {"data": "nombre"},
            {"data": "detalle"},
            {"data": "imagen"},
            {"data": "nombre"},

        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.imagen + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
                }
            },

            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                        var buttons = '<a href="/srea/a_lista/u_asignatura/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/srea/a_lista/d_asignatura/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i> </a>';
                        //Ingreso al test
                        buttons += ' <a href="/srea/index2/" type="button" class="btn btn-primary btn-xs btn-flat"> <i class="fa fa-search"> Ver</i> </a>';
                    
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});