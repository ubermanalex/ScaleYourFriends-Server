/** checks input **/

function checkInputLength(String, Integer) {
	var length = (String.length);
	return (length > Integer);
}

function check(String, Integer, id) {

	//TODO: return und enter
	var allowedchars = new Array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T',
	'U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
	'v','w','x','y','z','_','-','0','1','2','3','4','5','6','7','8','9','ä','ü','ö','Ä','Ü','Ö');
	 
	var key = window.event.keyCode;

    // If the user has pressed enter
    if (key == 13) {
    	senduser(usernameinput.value)
		}
    
	
	if (checkInputLength(String, Integer)) {
		alert("Zeichen auf " + Integer + " begrenzt!");
		id.value = String.substr(0, Integer);
	}
	if (allowedchars.indexOf(String[String.length - 1]) == -1 && key != 13 && key != 8){
		alert("Unerlaubtes Zeichen!");
		id.value = String.substr(0, String.length - 1);
	}
}