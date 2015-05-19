

LogoutModel = can.Model.extend({
    update : function( attrs ){
        return $.ajax({
            type: "POST",
            url: "/api/logout",
            data: JSON.stringify(attrs),
            async: false,
            contentType:"application/json;utf-8",
            dataType:"json",
            success: function(msg){
                return msg;
            }
        });
    }
},{})

$(function(){
    $("#logoutBtn").click(function(e){
        LogoutHandler();
    })
})

function LogoutHandler(){

    $.when(LogoutModel.update()).then(
        function(result){
            console.log(result);
            if(result.status == "ok"){
                $("#wrongText").hide();
                setCookie("currentUsername","",0,"/");
                window.location.href = "/";
            }
        },

        function (error) {
            console.log(error);
//            alert("Error: "+error.responseJSON.error);
            messageDialog("Error",error.responseJSON.message);
        }
    )
}