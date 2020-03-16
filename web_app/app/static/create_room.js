console.log("Create Room JS successfully loaded.");

var socket = io.connect('http://' + document.domain + ":" + location.port);

// connect create room button to function
$( "#create_room_button" ).on("click", create_room);

socket.on('add_player_to_lobby', (name) => {
    console.log("added player!");
    add_player_to_lobby(name);
});

socket.on('remove_player_from_lobby', (name) => {
    remove_player_from_lobby(name);
});


function create_room(){
    let game_options = get_game_options();
    let code = create_room_code();
    game_options.code = code;

    $( '#create_room_options').remove();
    
    // ask server to create game session
    socket.emit('create_game', game_options, function(val) {
	add_lobby_html(val);
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

function add_player_to_lobby(name){
    console.log("added  player:", name);
    $('#player_list').append("<li>" + name + "</li>");
}

function remove_player_from_lobby(name){
    console.log("removing player from lobby!");
    console.log("name:", name);
    var ele = $("#player_list");
    for (i = 0; i < ele.length; i++){
	console.log(ele[i].innerText);
	if (ele[i].innerText === name){
	    console.log("found it!");
	    ele[i].remove();
	}
    }

}
