console.log("reporting!")
var socket = io.connect('http://' + document.domain + ":" + location.port);

$('#dislike_button').on('click', () => update_rank('dislike'));
$('#meh_button').on('click', () => update_rank('meh'));
$('#like_button').on('click', () => update_rank('like'));

get_next_trivia();


function update_rank(rank){
    console.log('rank received: ', rank);
    socket.emit('update_rank', rank, () => get_next_trivia());
}

function get_next_trivia(){
    socket.emit('request_trivia', ' ', trivia => update_trivia(trivia));
}

function update_trivia(trivia){
    $('#trivia').text(trivia);
    console.log('updated trivia!');
}
