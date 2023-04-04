var myWords = u;
var nounContainer = document.getElementById('nouns');
var adjContainer = document.getElementById('adjs');
var verbContainer = document.getElementById('verbs');
var advContainer = document.getElementById('adverbs');
var prepContainer = document.getElementById('preps');
var phraseContainer = document.getElementById('phrases');
  
generateWords(myWords, nounContainer, "noun");
generateWords(myWords, adjContainer, "adj");
generateWords(myWords, verbContainer, "verb");
generateWords(myWords, advContainer, "adv");
generateWords(myWords, prepContainer, "prep");
generateWords(myWords, phraseContainer, "phrase");
  
function generateWords(words, xContainer, type){
    function showWords(words, xContainer){
    var output = [];
    var defs;
    for(var i=0; i<words.length; i++){
        // add words + defs
    if(words[i].Type == type)
    output.push(
        '<div class="question">' + words[i].Front + ' -- ' + words[i].Back + '</div>' 
    );
    }
      // make one string and put on page
    //choices.style.font-weight = "100";
    xContainer.innerHTML = output.join('');
}
showWords(words, xContainer);
}
  
  