var DIR = {
    DEFAULT : 2,
    UP : 1,
    DOWN : 0
};
var TYPE = {
    DEFAULT : 0,
    S : 1,
    R : 2
};
function replyvote(DIR_, TYPE_, id) {
    $.ajax({
        dataType: "json",
        type: "GET",
        url: "/ogidni/vote",
        data:"par="+Number(TYPE_)+"&dir="+Number(DIR_)+"&object_id="+id,
        success: function(data){
                if (data['loggedIn']){
                    updatePost(TYPE_, id, data);
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
            },
            501: function() {
                alert("E: Internal server error (object_id probably not found)");
            }
        }
    });
}
function updatePost(TYPE_, id, jsonData) {
    var votes = jsonData['votes'];
    switch (Number(TYPE_)){
        case TYPE.S:
            $(".s-panel").find("#s-"+id).find("h3").find("span")
                .html(votes["upvotes"]+" | "+votes["downvotes"]);
            break;
        case TYPE.R:
            $("#r-panel").find("#r-"+id).find(".badge")
                .html(votes["upvotes"]+" | "+votes["downvotes"]);
            break;
        default:
            break;
    }
}
function showLogin() {
    $("#loginModal").modal('show')
}
function showStory(sURL) {
    window.location.replace("/ogidni/"+sURL);
}
function userLogin() {
    window.location.replace("/ogidni/login");
}