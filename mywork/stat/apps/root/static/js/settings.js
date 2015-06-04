
ResetPasswordModel = can.Model.extend({
    update : function( attrs ){
        return $.ajax({
            type: "POST",
            url: "/api/reset-password",
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

var ResetPasswordControl = can.Control.extend({
    init : function(element){
        element.html(can.view("resetPasswordContent"));
    },

    "a.ResetBtn click" : function(el,e){
        console.log("reset click");
        resetPassword();
    }
})


$(function(){

    $(document).ready(function(){
        setCurrentUsername();
    })

    $("#leftNav li a").click(function(){
        var section = this.href.substring(this.href.indexOf("#") + 1);
        toSection(section);
    })

    toSection("ResetPassword");

})

function toSection(sec) {
    $("#leftNav li").removeClass("active");
    $("#leftNav li a[href=#" + sec + "]").parent().addClass("active");

    switch (sec) {
        case "ResetPassword" :
            new ResetPasswordControl('#SettingsContainer');
            break;

    }
}

function resetPassword(){
    $("#resetSuccess").hide();
    if(!validateMyComp("#inputOldPassword")||
       !validateMyComp("#inputNewPassword")||
        !validateMyComp("#inputReNewPassword")){
        return;
    }
    var oldPassword = $("#inputOldPassword").val();
    var newPassword = $("#inputNewPassword").val();
    var reNewPassword = $("#inputReNewPassword").val();
    if(newPassword != reNewPassword){
        $("#UnSameText").show();
    }else{
        $("#UnSameText").hide();
        $.when(ResetPasswordModel.update({old_password:hex_md5(oldPassword),new_password:hex_md5(newPassword)})).then(
            function(result){
                $("#resetSuccess").show();
                clear();
            },

            function (error) {
                console.log(error);
                messageDialog("Error",error.responseJSON.message);
            }
        )
    }
}

function clear(){
    $("#inputOldPassword").val("");
    $("#inputNewPassword").val("");
    $("#inputReNewPassword").val("");
    $("#UnSameText").hide();
}