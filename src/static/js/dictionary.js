var myWords2 = u2;
var myWords3 = u3;
var myWords = myWords2.concat(myWords3)

myWords.sort((a, b) => {
    const nameA = a.Front.toUpperCase(); // ignore upper and lowercase
    const nameB = b.Front.toUpperCase(); // ignore upper and lowercase
    if (nameA < nameB) {
      return -1;
    }
    if (nameA > nameB) {
      return 1;
    }
  
    // names must be equal
    return 0;
  });

var nounContainer = document.getElementById('words');
  
generateWords(myWords, nounContainer);
  
function generateWords(words, xContainer, ){
    function showWords(words, xContainer){
    var output = [];
    var defs;
    for(var i=0; i<words.length; i++){
        // add words + defs
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
  
  