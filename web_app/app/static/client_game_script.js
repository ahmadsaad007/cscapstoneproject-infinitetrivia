var socket = io.connect('http://' + document.domain + ":" + location.port);
// connect Join Game button
$("#join_room_button").on("click", join_game);

// connect socket to events
socket.on('display_splash_screen', function(round_number){
    display_splash_screen(round_number);
});

socket.on('display_text_response_prompt', display_text_response_prompt);

var code = undefined;

function join_game(){
    console.log("attempting to join game!");
    let entered_code = $('#room_code').val();
    let entered_name = $('#game_name').val();
    let data = {code: entered_code, name: entered_name};
    console.log(data);
    socket.emit('join_game', data, function(status){
	console.log("in callback!");
	switch(status) {
	case "ERR_INVALID_CODE":
	    console.log("error: invalid game code");
	    display_game_code_error();
	    break;
	case "ERR_INVALID_NAME":
	    console.log("error: invalid name.");
	    display_game_name_error();
	    break;
	case "ERR_COUND_NOT_JOIN":
	    console.log("error: could not join");	    
	    display_join_error();
	    break;
	case "ADDED_TO_LOBBY":
	    console.log("successfully added to lobby");
	    code = entered_code;
	    display_game_lobby();
	    break;
	default:
	    console.log("unknown return value from join_game???");
	    break;
	}
    });
}


function display_game_code_error(){
  console.log("invalid game code.");
  error_div = $( '#code_error_container' );
  error_div.empty();
  error_div.append("Invalid Code!");
  $( '#room_code' ).val("");
};


function display_game_name_error(){
  console.log("invalid name.");
  error_div = $( '#name_error_container' );
  error_div.empty();
  error_div.append("Invalid Name!");
  $( '#game_name' ).val("");
};


function display_join_error(){
    console.log("could not join game.");
  error_div = $( '#name_error_container' );
  error_div.empty();
  error_div.append("Could Not Join Game!");
}


function display_game_lobby(){
    $( '#home_screen_container').remove();
    $( '#game_container' ).append("<h3>Waiting for game to start...</h3>");
}


function display_splash_screen(round_number){
    $('#game_container').empty();
    // TODO update round 
    $('#game_container').append("<h3>Round " + round_number + "<\h3>");
}


function display_text_response_prompt(){
    const prompt = '<b>Answer:</b> <input id="text_answer">';
    const submit = '<button type="button" id="submit">Submit!</button>';
    $('#game_container').empty();
    $('#game_container').append(prompt);
    $('#game_container').append(submit);
    // connect button to submit event
    $('#submit').on('click', submit_text_answer);
}


function submit_text_answer(){
    let answer = $('#text_answer').val();
    console.log(answer);
    // TODO: send answer over to server
    socket.emit('submit_answer', {code: code, answer: answer}, function(status){
	submitted_answer(status);
    });
    // remove answer area
}

function submitted_answer(status){
    if (status){
	$('#game_container').empty();
	$('#game_container').append('<h3>Submitted Response!</h3>');
    } else {
	console.log("failed to submit answer!");
    }
}
