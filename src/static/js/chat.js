$('#msg-form').submit(function(event) {
    event.preventDefault();

    var msg = $('#msg').val();
    $('#chat-msg').append('<div class="text-row"><img class="grade" src="../static/img/grade.png"><div class="text user">' + msg + '</div></div>'); // hehe it says "text user". What a frickin' goober, you use text?
    $('#msg').val('');

    var chat_window = document.getElementById("chat-window");
    chat_window.scrollTop = chat_window.scrollHeight;
});