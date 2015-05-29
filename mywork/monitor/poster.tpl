<html>
  <head>
    <meta charset="utf-8" />
    <title>vod poster showup</title>
    <style class="overlay-style">
      div {
          margin:  0 auto
      }
      div img {
          --webkit-transition: all 0.5s; -moz-transition: all 0.5s; -o-transition: all  0.5s; display:block
      }
      .divcss5{ position:relative;width:554px; height:346px; margin:0 auto}
      .divcss5 a,.divcss5 span{display:none; text-decoration:none}
      .divcss5:hover{cursor:pointer}
      .divcss5:hover a.now{cursor:pointer; position:absolute; top:0; width:100%; height:100%; z-index:100; left:0; display:block;}
      .divcss5:hover span{ display:block;position:absolute; bottom:0; left:0;color:#FFF;width:554px; z-index:10;height:36px; line-height:36px; background:#000;filter:alpha(opacity=60);-moz-opacity:0.5;opacity: 0.5;}
      img{padding:0; border:0;}
    </style>
    <link href="../css/bootstrap.min.css" rel="stylesheet">
    <script src="../js/jquery-2.1.1.js"></script>
    <script src="../js/bootstrap.min.js"></script>
  </head>
  <body>
    <script type="text/javascript" src="poster_list.js"></script>
    <nav class="navbar navbar-default" role="navigation" style="margin:0">
      <div class="navbar-header">
        <a class="navbar-brand" href="#">聚好看首页模拟页面<small><small>[snapshot generated at {{create_time}}]</small></small></a>
      </div>

      <div class="navbar-nav navbar-right">
        <a href="#" class="dropdown-toggle navbar-nav" data-toggle="dropdown">
          ALL_POSTERS<b class="caret"></b>
        </a>
        <ul class="dropdown-menu">
          <script>
            var posterNames = getPosters();
            var i = 0, len = posterNames.length;
            for (; i< len; i++) {
                var name = posterNames[i];
                document.write("<li><a href="+name+">"+name+"</a></li>");
            }
          </script>
        </ul>
      </div>
      <div class="navbar-nav">
         <span class="icon-bar"></span>
      </div>
    </nav>
      
    {{content}}
    <script type='text/javascript'>
      $(document).ready(function() {
      $('.carousel').carousel({
      interval: 5000
      })
      });
    </script>
  </body>
</html>
