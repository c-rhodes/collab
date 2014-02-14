$(document).ready(function() {

});
var DIR = {
	DEFAULT : 0,
	UP : 1,
	DOWN : 2
}
var TYPE = {
	DEFAULT : 0,
	S : 1,
	R : 2
}
function replyvote(DIR_, TYPE_, id) {
	switch (Number(TYPE_)){
		case TYPE.S:
			$.ajax({
				url: "/odigni/vote_story/?dir="+Number(DIR_)+"&id="+id,
				statusCode: {
					204: function() {
						alert("No content");
					},
					400: function() {
						alert("Bad syntax");
					},
					404: function() {
						alert("Page not found");
					},
					501: function() {
						alert("Not implemented");
					}
				}
			});
			break;
		case TYPE.R:
			$.ajax({
				url: "/odigni/vote_reply?dir="+Number(DIR_)+"&id="+id,
				statusCode: {
					204: function() {
						alert("No content");
					},
					400: function() {
						alert("Bad syntax");
					},
					404: function() {
						alert("Page not found");
					},
					501: function() {
						alert("Not implemented");
					}
				}
			});
			break;
		default:
			alert("Malformed request");
			break;
	}
}