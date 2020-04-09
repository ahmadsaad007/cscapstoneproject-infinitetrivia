// todo set timer via message
var counter = 30;

function timer() {
    counter--;
    postMessage(counter);
    setTimeout('timer()', 1000);
}

timer();
