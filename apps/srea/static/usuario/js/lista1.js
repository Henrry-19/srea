$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false, //Respete los anchos de las columnas que yo especifique
        destroy: true,
        deferRender: true,//Agilita la carga de los datos
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata' //Envío mi parámetro
            },
            dataSrc: "" //No envío ninguna variable por esa razón está en blanco
        },
        columns: [
            {"data": "id"},
            {"data": "nombres"},
            {"data": "apellidos"},
            {"data": "birthday"},
            {"data": "email"},
            {"data": "genero"}, //[-1]
            {}
        ],
        columnDefs: [//Personalizar cada una de las columnas que se vayan creando
            {
                targets: [-1],//Cual es la columna que yo quiero manejar
                class: 'text-center',//Puedo agragar clases
                orderable: false,//puedo decirle que no se ordene
                render: function (data, type, row) {
                    var buttons = '<a href="/srea/u_lista/u_usuario/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/srea/u_lista/d_usuario/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});