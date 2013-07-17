/** initialiser **/

function initializeall() {

	var users = new Array();
	var songs = new SongDatabase();
}

/** loads home content **/

function loadhome(username) {

	/*TEST:*/
	var users = new Array();
	users.push('Heide');
	users.push('Frauberg');
	alert(users);
	/*:TEST*/
	if (username == "") {
		alert("Bitte einen Nutzernamen eingeben.");
	} else if (users.indexOf(username) != -1) {
		alert("Nutzername bereits vergeben.");
	} else {
		//alert("yo");
		/*$("#content").load("home.html", function() {
		 });*/
		/*$.get('home.html', function (response){
		 //var myHtml = $('#homecontent', response);
		 $('#content').html(response);
		 });*/
		$("#content").load("home.html", function() {
		});
	}
}

/*** SongDatabase ***/

/** Songobject **/

function Song(interpret, songtitle) {
	this.interpret = interpret;
	this.songtitle = title;
}

/** SongDatabase **/

function SongDatabase() {

	this.database = new Array();

	this.addSong = function(interpret, songtitle) {
		newsong = new Song(interpret, songtitle);
		this.database.push(newsong);
	};

	/*this.getSongsByInterpret = function(interpret) {
	 var result = '';
	 for (var i = 0; i < this.database.length; i++) {
	 if (this.database[i].interpret === interpret) {
	 result = result + this.database[i].titel + '\n';
	 }
	 }
	 var res = interpret + ':\n' + result;
	 ergebnisse.value = "von " + res;
	 };

	 this.getSongsByAlbum = function(album) {
	 var result = '';
	 for (var i = 0; i < this.database.length; i++) {
	 if (this.database[i].album === album) {
	 result = result + this.database[i].titel + '\n';
	 }
	 }
	 var res = album + ':\n' + result;
	 ergebnisse.value = "aus dem Album " + res;
	 };*/
}