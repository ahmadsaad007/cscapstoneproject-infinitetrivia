$(function() {
	$(".btn").click(function() {
		$(".form-signin").toggleClass("form-signin-left");
    $(".form-signup").toggleClass("form-signup-left");
    $(".frame").toggleClass("frame-long");
    $(".signup-inactive").toggleClass("signup-active");
    $(".signin-active").toggleClass("signin-inactive");
    $(".forgot").toggleClass("forgot-left");   
    $(this).removeClass("idle").addClass("active");
	});
});

$(function new_registration() {
	$(".submit").click(function() {
    //history.replaceState(null, "", "/signup");
    $(".nav").toggleClass("nav-up");
    $(".form-signup-left").toggleClass("form-signup-down");
    $(".success").toggleClass("success-left"); 
    $(".frame").toggleClass("frame-short");
	});
});

$(function() {
	$(".submit").click(function() {
    $(".btn-animate").toggleClass("btn-animate-grow");
    $(".welcome").toggleClass("welcome-left");
    $(".cover-photo").toggleClass("cover-photo-down");
    $(".frame").toggleClass("frame-short");
    $(".profile-photo").toggleClass("profile-photo-down");
    $(".btn-goback").toggleClass("btn-goback-up");
    $(".forgot").toggleClass("forgot-fade");
	});
});