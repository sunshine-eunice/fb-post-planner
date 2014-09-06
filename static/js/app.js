

$(document).ready(function() {
    
    $('#btn-post').click(function() {

    var data={
        method: 'post',
        message: $('#fb-message').val(),
        access_token:
        'CAACEdEose0cBAG89exf4k7b9HOzXNOLrseGBGMsbIIbznjGaH4W4HOCMjuTtAKTY5OZCyWRRCDcLJtFh0ZAoIYmCBHSsLS2ZBkR2FjrHyqgtGxngdvz5VhZBWJ8ckMckdwS23R8mlKuIBjUeFvZAO81IImxFnBZBZAiPg1RiuoS8vQ5GbxaCMZBc0N7fM6eydOYoZBn1JEQ25YxmD2oV32LFSyCZCIyTil8ZBkZD'
    };

    $.get('https://graph.facebook.com/v2.1/me/feed', data);
    });

});
