console.log("Create Room JS successfully loaded.");

var socket = io.connect('http://' + document.domain + ":" + location.port);

// connect create room button to function
$( "#create_room_button" ).on("click", create_room);


function create_room(){
    let game_options = get_game_options();
    let code = create_room_code();
    game_options.code = code;

    $( '#create_room_options').remove();
    
    // ask server to create game session
    socket.emit('create_game', game_options, function(code) {
	add_lobby_html(code);
    });
}


function get_game_options(){
    var game_opts = Object();

    // get game mode
    var ele = $("input[name='game_mode']");
    var mode;
    for (i = 0; i < ele.length; i++){
	if (ele[i].checked){
	    mode = ele[i].value;
	    break;
	}
    }
    game_opts.mode = mode;

    return game_opts;
}

function create_room_code(){
  var alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var code = "";
  for (i = 0; i < 4; i++){
    index = Math.floor(Math.random() * alphabet.length);
    code += alphabet[index];
  }
  return code;
}


function add_lobby_html(code){
    room_container = $( "#room_container" );
    room_container.append('<h2 id="room_id">Room ID: </b2>');
    room_container.append('<p>Connected Players:</p>');
    room_container.append('<ul id="player_list"/>');
    $("#room_id").append(code);
}
