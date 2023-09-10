data = {
    number_of_dice: 0,
    number_of_sides: 0,
    lower_bound: 0,
    upper_bound: 0,
    lowest_success: 0,
    number_of_successes: 0,
};

$('body').terminal({
    echo: function(arg1) {
        this.echo(arg1);
    },
    dice: function(){
        terminal.read('Please Enter the Number of Dice and the Number of Sides in the format 2d6: ').then(function(string) {
            check_dice(string);
        });
    },
    rerolls: function(){
        terminal.read('Please Enter which Dice results you wish to Re-roll once in the format 1-3 as a range, if no Re-rolls are required please enter 0: ').then(function(string){
            check_rerolls(string);
        });
    },
    desire: function(){
        if (data.number_of_dice >= 0 && data.number_of_sides >= 0) {
            terminal.read('Please enter what is the lowest number on the dice that counts as a success: ').then(function(string) {
                const cleaned_string = string.replace(/[^\d]/g, '');

                if (cleaned_string > 0 && cleaned_string <= data.number_of_sides) {
                    data.lowest_success = parseInt(cleaned_string);

                    terminal.read('Please enter the number of desired successes: ').then(function(string){
                        const cleaned_string = string.replace(/[^\d]/g, '');

                        if (cleaned_string > 0 && cleaned_string <= data.number_of_dice) {
                            data.number_of_successes = parseInt(cleaned_string);
                            terminal.echo('Successfully updated. \n');
                        } else {
                            terminal.echo('Please retry with a number greater than 0 and equal to or less than ' + data.number_of_dice + ' .\n');
                        }
                    });
                } else {
                    terminal.echo('Please retry with a number greater than 0 and equal to or less than ' + data.number_of_sides + ' .\n');
                }
            });
        }
        else {
            terminal.echo('Please set your dice first.\n')
        }
    },
    stats : function(){
        axios.post('https://terminal.williamcore.co.uk/stats', data).then((response) =>{
            terminal.echo(response);
        }) 
    }
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
        terminal.echo('Please retry with the given format. Dice have not been updated.\n');
        return false;
    }

    data.number_of_dice = parseInt(dice_array[0].replace(/[^\d]/g, ''));
    data.number_of_sides = parseInt(dice_array[1].replace(/[^\d]/g, ''));

    if (data.number_of_dice == "" || data.number_of_dice == null || data.number_of_dice == NaN) {
        data.number_of_dice = 1;
    }
    if (data.number_of_sides == "" || data.number_of_sides == null || data.number_of_sides == NaN) {
        data.number_of_sides = 1;
    }

    terminal.echo("The number of dice have been updated to " + data.number_of_dice);
    terminal.echo("The number of sides of those dice have been update to " + data.number_of_sides + '\n');
}

function check_rerolls(input) {
    const rerolls = input.toLowerCase();

    if (rerolls == 0) {
        terminal.echo("We will reroll no dice.\n");
        return true;
    }
    const reroll_array = rerolls.split("-", 2);

    if (reroll_array.length != 2) {
        terminal.echo('Please retry with the given format. Rerolls have not been updated.\n');
        return false;
    }

    const lower = parseInt(reroll_array[0].replace(/[^\d]/g, ''));
    const upper = parseInt(reroll_array[1].replace(/[^\d]/g, ''));

    if (lower > data.number_of_sides || upper > data.number_of_sides) {
        terminal.echo('Please enter a reroll list within the boundry of number of sides you have assigned to your dice.\n');
        return false;
    }

    data.lower_bound = lower;
    data.upper_bound = upper;

    terminal.echo("We will reroll all dice between " + data.lower_bound + " and " + data.upper_bound + " (inclusive) once.\n");
}