$('body').terminal({
    echo: function(arg1) {
        this.echo(arg1);
    },
    dice: function(){
        terminal = this;
        terminal.read('Please Enter the Number of Dice and the Number of Sides in the format 2d6: ').then(function(string){
            if (check(string)){
                terminal.echo('Dice have been updated.\n');
            } else {
                terminal.echo('Please retry with the given format. Dice have not been updated.\n');
            } 
        });

    },
    
}, {
    onInit: function() {
        this.echo('Hello, and welcome to my BinomialDice tool.');
        this.echo('There are currently x commands.\n');
        },
    greeting: false,
    prompt: 'diceStats> ' 
});

var isInt;
var number_of_dice;
var number_of_sides;

function check(input) {
    return true;
}