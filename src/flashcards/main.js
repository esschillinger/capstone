// import json, first is default
const unitsJSON = [u1, u2];

// Card Elem
let card = document.querySelector(".card")
let question = document.querySelector(".question");
let solution = document.querySelector(".solution");


// Buttons
let checkAnswerBUTTON = document.querySelector(".check_answer");
let newWordBUTTON = document.querySelector(".new_word");
let correctBUTTON = document.querySelector(".correct");
let wrongBUTTON = document.querySelector(".wrong");
let reloadBUTTON = document.querySelector(".reload");
let returnBUTTON = document.querySelector(".return");

// unitlist
const cardDeckOptions = [
    "u1",
    "u2",
];

// Text below the Cards
let remainingCards = document.querySelector(".remaining");
let knownCards = document.querySelector("#known");
let knownCardsCounter = 0;
let nextCards = document.querySelector("#next");

// define unit set
// global questionSet
let questionSet = unitsJSON[0];
let nextRound = [];
// set a questionSet to start with
function defineQuestionSet(set) {
    questionSet = set;
}


let lastDeckIDX = 0;
let deckOptions = document.querySelector("#decks");
deckOptions.addEventListener("change", (e) => {
    let selectedDeck = deckOptions.value;
    let lastDeckIDX = cardDeckOptions.indexOf(selectedDeck);

    defineQuestionSet(unitsJSON[lastDeckIDX]);
    newCard();
    });

// flip Card back to front
returnBUTTON.addEventListener("click", () => card.classList.remove("flipped"));


// load random F/B pair
function getQuestionPair(dict) {
    let rand = Math.floor(Math.random() * dict.length);
    return Object.entries(dict)[rand][1];
}

// innitial card on load
let randomPair = getQuestionPair(questionSet);

// display first card front
displayQuestion(randomPair);

// write text on front
function displayQuestion(rP) {
    // turn card to front-side
    card.classList.remove("flipped");
    // write on front
    question.innerHTML = rP["Front"];
    // add hidden to the back so card size scales with front text not back (most likely not going to matter anyway, card content should be short)
    solution.classList.add("hidden");
    // display stats
    remainingCards.innerHTML = `There are ${questionSet.length} Cards left`
    knownCards.innerHTML = `Total correct: ${knownCardsCounter}`; 
    nextCards.innerHTML = `Total Incorrect: ${nextRound.length}`; 
}

// used inside of "flipBackAndDisplayAnswer" to split multiple answers
function splitPhraseIfSeveralNumbers(phrase) {
    let re = /\d\.\s.+\;/;
    if (re.test(phrase)) {
        phrase = phrase.split(";");
    }
    return phrase;
}

// flip card to back-side and display/render text
function flipBackAndDisplayAnswer() {
    // display text on the back of the card
    card.classList.add("flipped");
    // unhide text
    solution.classList.remove("hidden");
    newWordBUTTON.classList.add("hidden");
    // create List of possible multiple-answer
    let answerList = splitPhraseIfSeveralNumbers(randomPair["Back"]);
    if (typeof answerList == "string") solution.innerHTML = randomPair["Back"];
    else {
        solution.innerHTML = "";
        let answerListDOM = document.createElement("ol");
        solution.appendChild(answerListDOM);
        answerList.forEach(a => {
            // check if a number is in front and delete it so the ordered list tag provides numbers;
            let numRegEx = /^\s*\d+\.\s/g;
            a = a.replace(numRegEx, "");
            let listElement = document.createElement("li");
            answerListDOM.appendChild(listElement);
            listElement.innerHTML = a;
        });
    }
}

// get a new card
function newCard() {
    if (questionSet.length === 0 && nextRound.length > 0) {
        questionSet = nextRound;
        unitsJSON[lastDeckIDX] = nextRound;
        nextRound = [];
    }
    // create new randomPair
    randomPair = getQuestionPair(questionSet);
    displayQuestion(randomPair);
}

// removes current randomPair 
function removeCardFromSet(correct) {
    let idx = questionSet.findIndex(qa => qa["Front"] == randomPair["Front"]);
    let card = questionSet[idx];
    if (correct) {
        questionSet.splice(idx, 1);
        knownCardsCounter += 1;
    } else {
        nextRound.push(card);
        questionSet.splice(idx, 1);
    }
    if (questionSet.length > 0 || nextRound.length > 0) newCard();
}

// attache the show-result function to the button on frontside of card
checkAnswerBUTTON.addEventListener("click", flipBackAndDisplayAnswer);

// attache newWord-function to button on backside of card
newWordBUTTON.addEventListener("click", newCard);

// attache functionality "newCard" to wrong-button
wrongBUTTON.addEventListener("click", () => {
    removeCardFromSet(false);
});
correctBUTTON.addEventListener("click", () => {
    removeCardFromSet(true);
});

// reload the page / begin from the beginning
reloadBUTTON.addEventListener("click", () => location.reload());




