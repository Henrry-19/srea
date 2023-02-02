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
            {"data": "full_name"},
            {"data": "username"},
            {"data": "date_joined"},
            {"data": "imagen"},
            {"data": "groups"},
            {"data": "position"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.imagen + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
                }
            },


            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.groups, function (key, value) {
                        html += '<span class="badge badge-success">' + value.name + '</span> ';
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
                        var buttons = '<a href="/user/user_list/u_user/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/user/user_list/d_user/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
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