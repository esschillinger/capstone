namespace = '/gpt'
var socket = io(namespace);

socket.emit('join');

socket.on('ai_response', function(message) { // 'message' is a dictionary containing the fields 'data', 'grade_msg', 'spelling', and 'grammar'
    addAIResponse(message.data, message.translation, message.grade_msg, message.spelling, message.grammar, message.vocab, message.relevance);
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


function addAIResponse(text, translation, grade_msg, spelling, grammar, vocab, relevance) {
    // grade should change the overall letter grade displayed next to the user's message (currently a graph icon, want to change to an image reflecting the letter grade)
    // when the grade is clicked, display the details in a modal (body = grade_msg)
    // add chat bubble for AI response

    var explanation = "";
    explanation += "<p>Spelling: " + spelling + "/10</p>";
    explanation += "<p>Grammar: " + grammar + "/10</p>";
    explanation += "<p>Vocab: " + vocab + "/10</p>";
    //explanation += "<p>Relevance: " + relevance + "/10</p>";
    explanation += "<p>" + grade_msg + "</p>";

    grade_descs.push(explanation);

    var grade_icon = document.getElementById('grade' + umsg_count);
    switch (Math.floor((parseInt(spelling) + parseInt(grammar) + parseInt(vocab)) / 3)) {
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


// on-screen keyboard

var input = document.getElementById("msg");
var keyboard = document.querySelectorAll(".key");
var admin_keys = [ // administrative, aka non-text
    "←",
    "Пробел"
];

keyboard.forEach(function(key) {
    key.addEventListener("click", function() {

    var key_pressed = key.innerHTML;
    var text = input.value;

    for (var i = 0; i < admin_keys.length; i++) {
        if (key_pressed == admin_keys[i]) {
            if (key_pressed == "←") {
                input.value = input.value.substring(0, input.value.length - 1);
            } else if (key_pressed == "Пробел") {
                input.value += " ";
            }
            document.getElementById("msg").focus();
            return;
        }
    }
    input.value = text + key_pressed;
    document.getElementById("msg").focus();
    });
});

var show = 0;
$('.keyboard-container').css("display", "none");


$(document).on("click", "#kb", function() {
    show = !show;
    if (show) {
        $('.keyboard-container').css("display", "flex");
        $('.container-chat').css("height", "310px");
    } else {
        $('.keyboard-container').css("display", "none");
        $('.container-chat').css("height", "500px");
    }
});