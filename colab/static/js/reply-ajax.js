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
    $("#submitReply").button();
    $("#replyBoxTextArea").wysihtml5();
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
    //$("#replyBox").hide();
});
$(document).mousemove(function(e){
    mousePos = {top:e.pageY, left:e.pageX};
});
function replyclick(TYPE_, id) {
    currentReplyID = {type:TYPE_, id:id};
    console.log(currentReplyID);
    var compT = mousePos.top;
    var compL = mousePos.left-$("#replyBox").width();
    $("#replyBox").offset({top:compT, left:compL});
    $("#replyBox").fadeIn();
}