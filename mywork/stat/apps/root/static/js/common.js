
var testCustomer_id = 0;


function messageDialog(title, content){
    var keys = ["Close"];
    $.teninedialog({
        title: title,
        content: content,
        showCloseButton:false,
        otherButtons:keys,
        otherButtonStyles:['btn'],
        clickButton:function(sender,modal,index){
            $(this).closeDialog(modal);
        }
    });
}

function confirmDialog(title, content, callback){
    var keys = ["Yes","Cancel"];
    $.teninedialog({
        title:title,
        content:content,
        showCloseButton:false,
        otherButtons:keys,
        otherButtonStyles:['btn-primary',''],
        bootstrapModalOption:{keyboard: false},
        dialogShow:function(){},
        dialogShown:function(){},
        dialogHide:function(){},
        dialogHidden:function(){},
        clickButton:function(sender,modal,index){
            if(callback) callback(keys[index]);
            $(this).closeDialog(modal);
        }
    })
}

/*** @vPos vertical position, in percent, like 0.5, 0.33, 0 ***/
function centerDialog(e, vPos){
//    vPos = typeof vPos !== "undefined" ? vPos : 0.33;
//    var comp = $(e.target).children(".modal-dialog");
//    comp.css(
//        {
//            'margin-top' : function () {
//                return (($(window).height() - comp.height()) * vPos);
//            },
//            paddingTop : 0
//        }
//    )
}


function cloneObj(from, to){
    from.each(function(v, k){
        to.attr(k, v)
//        console.log(k);
    })
}

function getItemById(arr, id){
    for(var i=0; i<arr.length; i++){
        if(arr[i].id == id)
            return arr[i];
    }
    return null;
}

function getIndexById(arr, id){
    for(var i=0; i<arr.length; i++){
        if(arr[i].id == id)
            return i;
    }
    return null;
}

/* @comp string for jquery.
 * @type 'text'. later: 'email' ...
 */
function validateMyComp(comp, type){
    type = typeof type === "undefined" ? "text" : type;
    var target = $(comp);
    var result = false ;
    if(type == "text" && target.val().trim() != ""){
        result = true ;
//    }else if(type == "email" &&){
    }
    if(!result)
        target.parent().addClass("has-error");
    else
        target.parent().removeClass("has-error");
    return result ;
}

/*  e.g. :
    renderPagi('#dg_devices_pagi',
        devices.count,
        devicePerPage,
        curDevicePage,
        function(e,originalEvent,type,page){
            curDevicePage = page;
            showDevices();
        }
    )
 */
function renderPagi(target, count, perPage, curPage, pageClickHandler){
    var maxPage = Math.ceil(count / perPage);
    if(maxPage == 0) maxPage = 1;
    if(curPage > maxPage) curPage = maxPage;
    var options = {
        currentPage: curPage,
        numberOfPages: 5,
        totalPages: maxPage,
        size: "small",
        alignment: "right",
        listContainerClass: "pagination pagination-sm pagi",
        onPageClicked: pageClickHandler
    };
    $(target).bootstrapPaginator(options);
    $(target).css({"text-align":"right", "width":"100%", "padding-right":"20px", "margin":0});
}

function setCurrentUsername(){
    $("#currentUsername").text(getCookie("currentUsername"));
}



function setCookie(c_name,value,expiredays,path)
{
    var exdate=new Date()
    exdate.setDate(exdate.getDate()+expiredays)
    document.cookie=c_name+ "=" +escape(value)+
        ((expiredays==null) ? "" : ";expires="+exdate.toGMTString())+ ((path==null)?"": ";path="+path)
}


function getCookie(c_name)
{
    if (document.cookie.length>0)
    {
        var c_start=document.cookie.indexOf(c_name + "=")
        if (c_start!=-1)
        {
            c_start=c_start + c_name.length+1
            var c_end=document.cookie.indexOf(";",c_start)
            if (c_end==-1) c_end=document.cookie.length
            return unescape(document.cookie.substring(c_start,c_end))
        }
    }
    return ""
}


$(function(){
    $("[data-tar]").click(function(e){
        var tar = $($(this).attr("data-tar"));
        if($(this).hasClass("glyphicon-minus")){
            tar.hide();
            $(this).removeClass("glyphicon-minus")
            $(this).addClass("glyphicon-plus")
        }else{
            tar.show();
            $(this).addClass("glyphicon-minus")
            $(this).removeClass("glyphicon-plus")
        }
    })
})

/***** device groups api *****/ //TODO: why this does not work?
//DeviceGroupsCommonModel = can.Model.extend({
//    // !!! api return {status:"ok", data:[...]}, canjs findAll will turn it to [...] with a property "status".
//    findAll : '/device/api/groups/list?start={start}&length={length}&customer_id={customer_id}',
//    findOne : '/device/api/groups/{id}?customer_id={customer_id}'
//},{});
//
//ConfigsCommonModel = can.Model.extend({
//    // !!! api return {status:"ok", data:[...]}, canjs findAll will turn it to [...] with a property "status".
//    findAll : '/ota/api/configuration/list?start={start}&length={length}&customer_id={customer_id}',
//    findOne : '/ota/api/configuration/{id}?customer_id={customer_id}'
//},{});