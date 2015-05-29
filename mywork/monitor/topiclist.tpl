<html>
  <head>
    <meta charset="utf-8" />
    <title>vod poster showup</title>
    <style class="overlay-style">
      div {
      margin:  0 auto;
      padding: 0 auto;
      }
      div img {
      --webkit-transition: all 0.5s; -moz-transition: all 0.5s; -o-transition: all  0.5s; display:block
      }
      .info p {margin: 0 auto; padding: 0 auto;}
      .info {width:{{width}};height:{{info_height}};padding-left:5;padding-top:8;background:#EAEAEA;}
      .poster {width:{{width}};height:{{height}};position:absolute;z-index:1;visibility:show;}
      div.info > p.title {font-family:微软雅黑;font-size:14px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;}
      div.info > p.desc {color:#999;font-size:10px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;}
      img{padding:0; border:0;}
    </style>
    <link href="../../css/bootstrap.min.css" rel="stylesheet">
    <script src="../../js/jquery-2.1.1.js"></script>
    <script src="../../js/bootstrap.min.js"></script>
  </head>
  <body>
    <script type="text/javascript" src="poster_list.js"></script>
    <nav class="navbar navbar-default" role="navigation">
      <div class="navbar-header">
        <a class="navbar-brand" href="#">聚好看 {{page_title}} 模拟页面<small><small>(只展示第一页的数据，更多请进入聚好看查看)[snapshot generated at {{create_time}}]</small></small></a>
      </div>
    </nav>
    {{content}}
    
  </body>
</html>
