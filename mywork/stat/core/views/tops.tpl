<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <title>vod_performance_portal</title>
    <link href="../../static/css/bootstrap/3.0.0/bootstrap.min.css" rel="stylesheet">
    <script src="../../static/js/jquery-1.11.1.min.js"></script>
    <script src="../../static/js/bootstrap/3.0.0/bootstrap.min.js"></script>
    <script type="text/javascript" src="../../static/js/Chart.js"></script>
  </head>

  <body onLoad="init()">
    <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-3">
          <h2>vidaa2首页</h2>
          <p><a class="btn btn-default" href="tops_api?api=frontpage2" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>vidaa3首页</h2>
          <p><a class="btn btn-default" href="tops_api?api=frontpage3" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>详情页</h2>
          <p><a class="btn btn-default" href="tops_api?api=media_detail" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>分类页</h2>
          <p><a class="btn btn-default" href="tops_api?api=category" role="button">View details &raquo;</a></p>
        </div>
      </div>
      <hr>
      <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-3">
          <h2>播放历史</h2>
          <p><a class="btn btn-default" href="tops_api?api=history" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>搜索</h2>
          <p><a class="btn btn-default" href="tops_api?api=search_result" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>专题详情</h2>
          <p><a class="btn btn-default" href="tops_api?api=topic_detail" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>专题列表</h2>
          <p><a class="btn btn-default" href="charts/latency" role="button">View details &raquo;</a></p>
        </div>
      </div>
      <hr>
      <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-3">
          <h2>7天更新</h2>
          <p><a class="btn btn-default" href="charts/trends" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>大家正在看</h2>
          <p><a class="btn btn-default" href="charts/tops" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>相关视频</h2>
          <p><a class="btn btn-default" href="charts/latency" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>猜你喜欢</h2>
          <p><a class="btn btn-default" href="charts/latency" role="button">View details &raquo;</a></p>
        </div>
      </div>
      <hr>
  </body>
</html>
