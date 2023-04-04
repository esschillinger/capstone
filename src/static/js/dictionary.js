var myQuestions = u;
var quizContainer = document.getElementById('quiz');
  
generateQuiz(myQuestions, quizContainer);
  
function generateQuiz(questions, quizContainer){
    function showQuestions(questions, quizContainer){
    var output = [];
    var choices;
    for(var i=0; i<questions.length; i++){
    choices = [];
    for(letter in questions[i].choices){
        choices.push(
        '<label>'
            + '<input type="radio" name="question'+i+'" value="'+letter+'">'
            + letter + ': '
            + questions[i].choices[letter]
            + '&nbsp'
        + '</label>'
        );
    }
        // add question + choices
    output.push(
        '<div class="question">' + questions[i].Front + '</div>'
        + '<div class="choices" font-weight="100">' + questions[i].Back + '</div>' + '<br>'
    );
    }
      // make one string and put on page
    //choices.style.font-weight = "100";
    quizContainer.innerHTML = output.join('');
}
showQuestions(questions, quizContainer);
}
  
  