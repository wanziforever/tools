


LoginModel = can.Model.extend({
//    findOne: 'POST /api/login?username={username}&password={password}'

    update : function( attrs ){
        return $.ajax({
            type: "POST",
            url: "/api/login",
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

//    checkLogin();

    $(document).ready(function(){
        var rememberName = getCookie("rememberName");
//        var rememberPassword = getCookie("rememberPassword");
        if(rememberName != null&&rememberName != ""){
            $("#rememberCkb")[0].checked = true;
            $("#username").val(rememberName);
//            $("#password").val(rememberPassword);
        }
    })

    $("#signBtn").click(function(){
       LoginHandler();
    })

    $("#username").keydown(function(e){
        var curKey = e.which;
        if(curKey == 13){
            LoginHandler();
        }

    })

    $("#password").keydown(function(e){
        var curKey = e.which;
        if(curKey == 13){
            LoginHandler();
        }

    })
})

function LoginHandler(){
    var username = $("#username").val();
    var password = $("#password").val();
    var password_md5 = hex_md5(password);

    $.when(LoginModel.update({username:username, password:password_md5})).then(
        function(result){
            console.log(result);
            if(result.status == "success"){
                $("#wrongText").hide();
                if($("#rememberCkb")[0].checked){
                    setCookie("rememberName",username,1);
//                    setCookie("rememberPassword",password);
                }else{
                    setCookie("rememberName","",0);
//                    setCookie("rememberPassword","");
                }
                setCookie("currentUsername",result.nickname,1);
                window.location.href = "/device/";
            }
        },

        function (error) {
            console.log(error);
//            alert("Error: "+error.responseJSON.error);
            $("#wrongText").show();
        }
    )
}

function checkLogin(){
    if(getCookie("X-JAMDEO-TOKEN")){
        window.location.href = "/device/";
        return;
    }
}