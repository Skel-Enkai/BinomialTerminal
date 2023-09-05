$('body').terminal({
    echo: function(arg1) {
        this.echo(arg1);
    },
    dice: function() {
        function check() {
            return 'Working';
        }
        this.read('Please Enter the Number of Dice and the Number of Sides in the format 2d6', check())
    }
}, {
    onInit: function() {
        this.echo('Hello, to use my binomial dice tool, please type: \'dice\'');
        },
    greeting: false,
    prompt: '>' 
});