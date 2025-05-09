const fs = require('fs');
const readline = require('readline');
const process = require('process');

const FLAG = fs.readFileSync('/home/ctf/flag.txt', 'utf8');

// var NUMBERS = [];
// for (var i = 0; i < 1000; i++) {
//     NUMBERS.push(Math.random());
// }

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

const STATE_INIT = 0;
const STATE_GUESSING = 1;
const STATE_TRY_AGAIN = 2;

const N_GUESSES = 1; // för svårt? neeeeeej...

var current_number_to_guess;
var current_attempt

function init_guess() {
    state = STATE_GUESSING;
    // current_number_to_guess = NUMBERS[0];
    // NUMBERS = NUMBERS.slice(1);
    current_number_to_guess = Math.random()

    console.log("Alright! Jag tänker på ett tal mellan 0 och 1. Vad är din gissning?");
    current_attempt = 0;
}

var state = STATE_INIT;

console.log("Välkommen till Extreme Guessing. Vill du spela? [J/n]");


rl.on('line', line => {
    if (state === STATE_INIT || state === STATE_TRY_AGAIN) {
        if (line.toLowerCase() == "j") {
            init_guess();
        } else {
            console.log("Hej då.");
            process.exit();
        }
    } else if (state === STATE_GUESSING) {
        guess = parseFloat(line);
        if (isNaN(guess)) {
            console.log("För ???");
        } else if (guess > current_number_to_guess) {
            console.log("För högt!");
        } else if (guess < current_number_to_guess) {
            console.log("För lågt!");
        } else {
            console.log("Du vann! Här är flaggan: " + FLAG);
            process.exit();
        }
        current_attempt += 1;
        if (current_attempt < N_GUESSES) {
            console.log("Gissa igen!");
        } else {
            console.log("Du har slut på försök. Tyvärr förlorade du");
            console.log("Spela igen? [J/n]");
            state = STATE_TRY_AGAIN;
        }
    }
});


