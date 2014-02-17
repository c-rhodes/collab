$(".textarea").wysihtml5({
    "font-styles": true, //Font styling, e.g. h1, h2, etc. Default true
    "emphasis": true, //Italics, bold, etc. Default true
    "lists": true, //(Un)ordered lists, e.g. Bullets, Numbers. Default true
    "html": false, //Button which allows you to edit the generated HTML. Default false
    "link": false, //Button to insert a link. Default true
    "image": false, //Button to insert an image. Default true,
    "color": true //Button to change color of font  
});
var mousePos = {top:100, left:100};
var currentReplyID = {};
var TYPE = {
    DEFAULT : 0,
    S : 1,
    R : 2
};
$(document).ready(function() {
    $("#closeReply").click(function(){
        $("#replyBox").fadeOut();
    });
    $("#submitReply").click(function(){
        if (currentReplyID == {} || 
            currentReplyID['sid'] == null || currentReplyID['rid'] == null) {
            alert("Please click reply on an item before submitting a reply.");
            return;
        }
        var encodeHTML = encodeURIComponent($(".textarea").val());
        $.ajax({
            dataType: "json",
            type: "get",
            url: "/ogidni/reply",
            data:"story_id="+currentReplyID['sid']+"&reply_id="+currentReplyID['rid']+
                "&editor_data="+encodeHTML,
            success: function(data){
                    if (data['loggedIn']){
                        if (data['posted']){
                            location.reload(true);
                        } else {
                            alert("Something went wrong, please try again!");
                        }
                    } else {
                        showLogin();
                    }
                },
            statusCode: {
                400: function() {
                    alert("E: Bad syntax");
                },
                404: function() {
                    alert("E: Page not found");
                }
            }
        });
        var reset = $("#replyBox").css("border");
        $("#replyBox").css("border: 1px solid green");
        $("#replyBox").fadeOut({complete:function(){
            $("#replyBox").css("border", reset);
        }});
    });
    $("#replyBox").hide();
    //$("#replyBoxTextArea").wysihtml5();
    /*{
            "font-styles": true, //Font styling, e.g. h1, h2, etc. Default true
            "emphasis": true, //Italics, bold, etc. Default true
            "lists": false, //(Un)ordered lists, e.g. Bullets, Numbers. Default true
            "html": false, //Button which allows you to edit the generated HTML. Default false
            "link": false, //Button to insert a link. Default true
            "image": false, //Button to insert an image. Default true,
            "color": true //Button to change color of font  
        }
    */
});
$(document).mousemove(function(e){
    mousePos = {top:e.pageY, left:e.pageX};
});
function replyclick(s_id ,r_id) {
    currentReplyID = {sid:s_id, rid:r_id};
    console.log(currentReplyID);
    var compT = mousePos.top;
    var compL = mousePos.left-$("#replyBox").width();
    $("#replyBox").offset({top:compT, left:compL});
    $("#replyBox").fadeIn();
}