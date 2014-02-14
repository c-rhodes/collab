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
				type: "GET",
				url: "/ogidni/vote_story",
				data:"dir="+Number(DIR_)+"&story_id="+id,
				statusCode: {
					400: function() {
						alert("Bad syntax");
					},
					404: function() {
						alert("Page not found");
					},
					501: function() {
						alert("Not implemented");
					}
				},
				success: function(data){
						updatePost(TYPE.S, id, data);
					}
				}
			});
			break;
		case TYPE.R:
			$.ajax({
				type: "GET",
				url: "/ogidni/vote_reply",
				data:"dir="+Number(DIR_)+"&reply_id="+id,
				statusCode: {
					400: function() {
						alert("Bad syntax");
					},
					404: function() {
						alert("Page not found");
					},
					501: function() {
						alert("Not implemented");
					}
				},
				success: function(data){
						updatePost(TYPE.R, id, data);
					}
				}
			});
			break;
		default:
			alert("Malformed request");
			break;
	}
}