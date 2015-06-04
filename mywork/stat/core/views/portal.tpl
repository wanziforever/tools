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
    <div class="jumbotron">
      <div class="container">
        <h1>聚好看线上性能数据分析Portal
          <a class="btn btn-xs btn-primary" href="history">更新2014-12-16</a></h1>
        <p>聚好看是海信电视的视频服务，这个页面用来展示聚好看系统中的一些关键的数据统计报表。</p>
      </div>
    </div>

    <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-4">
          <h2>各接口访问频度趋势</h2>
          <p>统计聚好看系统中终端访问的性能数据，包括按照每天的小时展示</p>
          <p><a class="btn btn-default" href="charts/trends" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>各接口访问峰值</h2>
          <p>统计聚好看系统中终端访问各个接口的峰值数据，按照天来展示</p><br>
          <p><a class="btn btn-default" href="charts/tops" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>各个接口处理时延统计</h2>
          <p>统计聚好看系统中终端访问各个接口中，系统端处理时延情况，统计每个小时最大时延数，按照天来展示</p>
          <br>
          <p><a class="btn btn-default" href="charts/latency" role="button">View details &raquo;</a></p>
        </div>
      </div>
      <hr>
  </body>
</html>
