var number_of_dice;
var number_of_sides;

var lower_bound = 0;
var upper_bound = 0;

var lowest_success;
var number_of_successes;

$('body').terminal({
    echo: function(arg1) {
        this.echo(arg1);
    },
    dice: function(){
        terminal.read('Please Enter the Number of Dice and the Number of Sides in the format 2d6: ').then(function(string) {
            if (check_dice(string)) {
                terminal.echo('\n');
            } else {
                terminal.echo('Please retry with the given format. Dice have not been updated.\n');
            } 
        });
    },
    rerolls: function(){
        terminal.read('Please Enter which Dice results you wish to Re-roll once in the format 1-3 as a range, if no Re-rolls are required please enter 0: ').then(function(string){
            if (check_rerolls(string)) {
                terminal.echo('\n');
            } else {
                terminal.echo('Please retry with the given format. Rerolls have not been updated.\n');
            } 
        });
    },
    desire: function(){
        terminal.read('Please enter what is the lowest number on the dice that counts as a success: ').then(function(string) {
            const cleaned_string = string.replace(/[^\d]/g, '');
            if (cleaned_string > 0) {
                lowest_success = cleaned_string;
                terminal.read('Please enter the number of desired successes: ').then(function(string){
                    const cleaned_string = string.replace(/[^\d]/g, '');
                    if (cleaned_string > 0) {
                        number_of_successes = cleaned_string;
                        
                    } else {
                        terminal.echo('Please retry with a number greater than 0.\n');
                    }
                });
            } else {
                terminal.echo('Please retry with a number greater than 0.\n');
            }
        });
    },
}, {
    onInit: function() {
        this.echo('Hello, and welcome to my BinomialDice tool.\nThere are currently x commands.\n'+'[[b;#34c23e;]dice]' 
        +' :Sets the number of dice and the number of sides of those dice.\n');
        terminal = this;
        },
    greeting: false,
    prompt: '[[b;#34c23e;]diceStats> ]' 
});

function check_dice(input) {
    const lower = input.toLowerCase();
    const dice_array = lower.split("d", 2);

    if (dice_array.length != 2) {
        return false;
    }

    number_of_dice = dice_array[0].replace(/[^\d]/g, '');
    number_of_sides = dice_array[1].replace(/[^\d]/g, '');

    if (number_of_dice == "" || number_of_dice == null || number_of_dice == NaN) {
        number_of_dice = 1;
    }
    if (number_of_sides == "" || number_of_sides == null || number_of_sides == NaN) {
        number_of_sides = 1;
    }

    terminal.echo("The number of dice have been updated to " + number_of_dice);
    terminal.echo("The number of sides of those dice have been update to " + number_of_sides);

    return true;
}

function check_rerolls(input) {
    const lower = input.toLowerCase();

    if (lower == 0) {
        terminal.echo("We will reroll no dice.");
        return true;
    }
    const reroll_array = lower.split("-", 2);

    if (reroll_array.length != 2) {
        return false;
    }

    lower_bound = reroll_array[0].replace(/[^\d]/g, '');
    upper_bound = reroll_array[1].replace(/[^\d]/g, '');

    terminal.echo("We will reroll all dice between " + lower_bound + " and " + upper_bound + " (inclusive) once.");

    return true;
}