var tblClient;

$(function () {

    $('.btnAdd').on('click', function(){
        // $('#myModalMensaje').modal('show');
    });

    $('#data tbody').on('click','a[rel="edit"]',function(){
        var data=tblClient.row($(this).parents('tr')).data();
        console.log(data)
    });
});