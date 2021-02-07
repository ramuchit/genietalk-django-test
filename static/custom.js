var secondCount;
$(document).ready(function(){
    $("#convertbtn").on('click', function(){
        let day = $("#day").val()
        if(day == ''){
            alert("Please enter name of days")
            return false
        }
        $.ajax({
            url:'/api/dateconvertor/?day='+day,
            success: function(res){
                $("#converted-output").html("<b>Converted : "+res.day+"</b>")
            }
        });
    });

    $("#startbtn").on('click',function(){
        secondCount=1;
        processFile= false
        $("#audio_link").hide().attr('href','#').text('coming soon...')
        $.ajax({
            url:'/api/stream/',
            method:'post',
            beforeSend: function(xhr, settings) {
                processFile= true
                 function getCookie(name) {
                     var cookieValue = null;
                     if (document.cookie && document.cookie != '') {
                         var cookies = document.cookie.split(';');
                         for (var i = 0; i < cookies.length; i++) {
                             var cookie = jQuery.trim(cookies[i]);
                             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                 break;
                             }
                         }
                     }
                     return cookieValue;
                 }
                 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                     xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                 }

             } ,
            success: function(res){
                processFile= false
                $("#audio_link").show().attr('href',window.location.origin+res).text('Audio file in text')
            }
        });
        $(this).text('Listening...').prop('disabled', true);
        var interval = setInterval(myTimer ,1000);
    })




    $( "#autocomplete" ).autocomplete({
          source: function( request, response ) {
            $.ajax({
              url: "api/autocomplete/",
              dataType: "json",
              data: {
                q: request.term
              },
              success: function( data ) {

                response($.map(data, function (item) {

                    return {
                        label: item.title,
                        value: item.title
                    };
                }));
              }
            });
          },

        select: function( event, ui ) {
           $("#selected").html("<b>Selected: "+ui.item.value+"</b>")
        }
    });
});


function myTimer(){
     if (secondCount > 10){
         $("#startbtn").text('start').prop('disabled', false);
         if(processFile){
             $("#audio_link").show().text('Please wait...')
         }
         return false
     }
     $("#startbtn").text('Listening...'+ secondCount +'')
     secondCount = secondCount+1;


}
