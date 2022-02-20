$(document).ready(function(){
    $(function(){
    $.ajax({
        type : "GET",
        url : '/suggest',
        success: function(data){
            $('#textsearch').autocomplete({
                source: data,
                minLength: 0
            });
        }
    })

 });
});
