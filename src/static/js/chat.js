namespace = '/gpt'
var socket = io(namespace);

socket.emit('join');

socket.on('ai_response', function(message) { // 'message' is a dictionary containing the fields 'data', 'grade_msg', 'spelling', and 'grammar'
    addAIResponse(message.data, message.translation, message.grade_msg, message.spelling, message.grammar);
});


// jQuery events


var umsg_count = 0;
var chat_window = document.getElementById("chat-window");
var grade_descs = []

$('#msg-form').submit(function(event) {
    umsg_count++;
    event.preventDefault();

    var msg = $('#msg').val();
    $('#chat-msg').append(`
    <div class="text-row">
        <input type="image" id="grade` + umsg_count + `" class="grade" src="/static/img/loading.gif" data-id="` + umsg_count + `" data-toggle="modal" data-target="#exampleModalCenter">
        <div class="text user">
            ` + msg + `
        </div>
    </div>`); // hehe it says "text user". What a frickin' goober, you use text?
    $('#msg').val('');

    chat_window.scrollTop = chat_window.scrollHeight;

    socket.emit('user_message', {
        data : msg
    });
});


$(document).on("click", ".grade", function() {
    var msg_num = $(this).data('id');
    document.getElementById("mbody").innerHTML = grade_descs[parseInt(msg_num) - 1];
});


// Helper functions


function addAIResponse(text, translation, grade_msg, spelling, grammar) {
    // grade should change the overall letter grade displayed next to the user's message (currently a graph icon, want to change to an image reflecting the letter grade)
    // when the grade is clicked, display the details in a modal (body = grade_msg)
    // add chat bubble for AI response

    grade_descs.push(grade_msg);

    var grade_icon = document.getElementById('grade' + umsg_count)
    switch(Math.floor((spelling + grammar) / 2)) {
        // change grade icon to be image corresponding to grade
        // TODO replace src links with the actual images once obtained
        case 10:
        case 9:
            grade_icon.src = '/static/img/A.jpg';
            break;
        case 8:
            grade_icon.src = '/static/img/B.png';
            break;
        case 7:
            grade_icon.src = '/static/img/C.jpg';
            break;
        case 6:
            grade_icon.src = '/static/img/D.png';
            break;
        default:
            grade_icon.src = '/static/img/F.jpg';
            break;
    }

    $('#chat-msg').append('<div class="text-row"><div class="text" data-container=".text-row" data-toggle="tooltip" data-placement="top" title="' + translation + '">' + text + '</div></div>');
    //$('#chat-msg').append('<div style="background-color: green" class="text" data-container=".text" data-toggle="tooltip" data-placement="top" title="' + getTranslation(data) + '"></div>')
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });

    chat_window.scrollTop = chat_window.scrollHeight;
}