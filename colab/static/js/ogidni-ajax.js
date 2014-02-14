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
  				dataType: "json",
				type: "GET",
				url: "/ogidni/vote_story",
				data:"dir="+Number(DIR_)+"&story_id="+id,
				success: function(data){
						updatePost(TYPE.S, id, data);
					},
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
				}
			});
			break;
		case TYPE.R:
			$.ajax({
  				dataType: "json",
				type: "GET",
				url: "/ogidni/vote_reply",
				data:"dir="+Number(DIR_)+"&reply_id="+id,
				success: function(data){
						updatePost(TYPE.R, id, data);
					},
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
				}
			});
			break;
		default:
			alert("Malformed request");
			break;
	}
}
function updatePost(TYPE_, id, jsonData) {
	switch (Number(TYPE_)){
		case TYPE.S:
			$("#s-panel").find("#s-"+id).find("h3").find("span")
				.html(jsonData["upvotes"]+" | "+jsonData["downvotes"]);
			break;
		case TYPE.R:
			$("#r-panel").find("#r-"+id).find(".badge")
				.html(jsonData["upvotes"]+" | "+jsonData["downvotes"]);
			break;
		default:
			break;
	}
}