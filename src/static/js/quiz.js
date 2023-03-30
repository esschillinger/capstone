var myQuestions = quizQuestions;
var submitButton = document.getElementById('submit');
var quizContainer = document.getElementById('quiz');
var resultsContainer = document.getElementById('results');
  
generateQuiz(myQuestions, quizContainer, resultsContainer, submitButton);
  
function generateQuiz(questions, quizContainer, resultsContainer, submitButton){
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
        '<div class="question">' + questions[i].question + '</div>'
        + '<div class="choices" font-weight="100">' + choices.join('') + '</div>' + '<br>'
    );
    }
      // make one string and put on page
    //choices.style.font-weight = "100";
    quizContainer.innerHTML = output.join('');
}
  
  
function showResults(questions, quizContainer, resultsContainer){
    var choiceContainers = quizContainer.querySelectorAll('.choices');
    var userChoice = '';
    var numCorrect = 0;
    for(var i=0; i<questions.length; i++){
    userChoice = (choiceContainers[i].querySelector('input[name=question'+i+']:checked')||{}).value;
    if(userChoice===questions[i].correctAnswer){ //if correct
        numCorrect++;
        choiceContainers[i].style.color = 'lightgreen';
    }
    else{ //else (incorrect)
        choiceContainers[i].style.color = 'red';
    }
    }
    resultsContainer.innerHTML = numCorrect + ' correct.<br>' + questions.length + ' total.';
      // total correct
}
showQuestions(questions, quizContainer);
submitButton.onclick = function(){ //show results on submission
    showResults(questions, quizContainer, resultsContainer);
}
}
  
  