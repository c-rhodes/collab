$(document).ready(function() {
	var DIRECTION = {
		DEFAULT : 0,
		UP : 1,
		DOWN : 2
	}
	var TYPE = {
		DEFAULT : 0,
		S : 1,
		R : 2
	}
	function replyvote(DIRECTION_, TYPE_, id) {
		switch (number(TYPE_)){
			case TYPE.STORY:
				$.get({
					url: "/odigni/vote_story?dir="+number(DIRECTION_)+"&id="+id,
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
			case TYPE.REPLY:
				$.get({
					url: "/odigni/vote_reply?dir="+number(DIRECTION_)+"&id="+id,
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
});