
/*
$(document).ready(function(){
   $('.like').on('click',function(){


    let id = $(this).attr('memberid');
    req = $.ajax({
        type: "POST",
        url:  '/like/new/'+id
    });

    req.done(function(data) {
            $('[memberid ='+ id + ']').text('Likes (' + data.number_of_likes + ')');
            var audio = {};
            audio["walk"] = new Audio();
            audio["walk"].src = "/static/sound/like.mp3";
            audio["walk"].play();
            
      });

   })

   $('#postcomment').on('click',function(){

            var audio = {};
            audio["walk"] = new Audio();
            audio["walk"].src = "/static/sound/sent.mp3";
            audio["walk"].play();



   });

 

});
*/

