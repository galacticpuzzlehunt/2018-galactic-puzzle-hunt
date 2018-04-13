var REQUEST_URL_UNLOCK = "/puzzle/pride-and-accomplishment/unlock";
var REQUEST_URL_OPEN = "/puzzle/pride-and-accomplishment/open";

var main = function() {
    var doUnlock = function(data){
        $('#lootbox'+data.index).attr('src', data.image);
    };

    var doOpen = function(data){
        $('#loot').html('');
        if(data.num == 1){
            $('#loot').append('<p>You opened a lootbox! It contained the following loot:</p>');
        }else{
            $('#loot').append('<p>You opened '+ data.num + ' lootboxes! They contained the following loot:</p>');
        }
        
        $('#loot').append('<ul id="lootList"></ul>');

        for(var i=0;i<data.num;i++){
            $('<li/>').text(data.boxes[i]).appendTo('#lootList');
        }
    };

    $('#unlock').on('submit', function(){
        $('#unlock-error').html('');
        var requestData = {"code": $('#code').val().trim()};
        $('#code').val('');

        if(requestData.code.length != 0) {
            $.post(REQUEST_URL_UNLOCK, JSON.stringify(requestData),
                function(response){
                    var responseData = $.parseJSON(response);
                    if(responseData.error.length > 0){
                        $('#unlock-error').html(responseData.error);
                    }else{
                        doUnlock(responseData);
                    }
                });
        }

        return false;
    });

    $('#open').on('submit', function(){
        $('#open-error').html('');
        var requestData = {"num": parseInt($('#num').val())};

        $.post(REQUEST_URL_OPEN, JSON.stringify(requestData),
            function(response){
                var responseData = $.parseJSON(response);
                if(responseData.error.length > 0){
                    $('#open-error').html(responseData.error);
                }else{
                    doOpen(responseData);
                }
            });

        return false;
    });};

$(document).ready(main);
