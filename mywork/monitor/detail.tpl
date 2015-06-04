<!DOCTYPE html>
<html lang="en">
  <head>
    <title>《{{title}}》详情</title>
    <meta charset="utf-8" />
    <link href="../../css/bootstrap.css" rel="stylesheet">
    <script src="../../js/jquery-1.8.0.min.js" type="text/javascript"></script>
    <script src="../../js/bootstrap.js" type="text/javascript"></script>
    <style>
      .spacer {
      margin-top: 40px; /* define margin as you see fit */
      }
    </style>
  </head>
  <body>
    <script>
      function GetRequest() {
          var url = location.search; 
          var theRequest = new Object();
          if (url.indexOf("?") != -1) {
              var str = url.substr(1);
              strs = str.split("&");
              for(var i = 0; i < strs.length; i ++) {
                  theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
              }
          }
          return theRequest;
      }  
    </script>
    <div class="container-fluid">
      <div class="row-fluid">
        <div class="col-md-6">
          [snapshot generated at {{create_time}}]
        </div>
        <div class="col-md-6">
          <button class="btn btn-defaault pull-right" onclick="window.history.go(-1)">返回</button>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="col-md-9">
        <div style="text-align:center"><h3>{{title}}</h3></div>
      </div>
    </div>

    <div class="container">
      <div class="row-fluid">
        <div class="col-md-3">
          <div><img src="{{pic}}" style="width:240px;height:300px"></div>
        </div>
        <div class="col-md-6">
          <br>
          <div class="container-fluid" style="padding-left:0px">
            <div class="row-fluid" style="padding-left:0px">
              <div class="col-md-6" style="padding-left:0px">影片详情:</div>
              <div class="col-md-6"><span class="pull-right">共{{num}}集</span></div>
            </div>
          </div>
          <br>
          <div>
            <p>{{content}}</p>
          </div>
          <br>
          <div>
            <p>演员：{{actors}}</p>
            <p>类型：{{category}}   <{{tag}}></p>
          </div>
        </div>
      </div>
    </div>
    <br>
    <div class="container">
      <div class="row-fluid">
        <div class="col-md-3">
          <a id="play" class="btn btn-primary" style="width:240px" href="#">点播消息模拟</a>
        </div>
      </div>  
    </div>
    <script>
      var Request = new Object();
      Request = GetRequest();
      uuid = Request['uuid']
      url = "{{history_url}}"
      x = document.getElementById("play")
      x.href = url
    </script>
  </body>
</html>
