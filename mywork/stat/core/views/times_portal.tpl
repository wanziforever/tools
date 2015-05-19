<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <title>vod_statistic_frequency_portal</title>
    <link href="../../static/css/bootstrap/3.0.0/bootstrap.min.css" rel="stylesheet">
    <script src="../../static/js/jquery-1.11.1.min.js"></script>
    <script src="../../static/js/bootstrap/3.0.0/bootstrap.min.js"></script>
    <script type="text/javascript" src="../../static/js/Chart.js"></script>
  </head>

  <body>
    <div class="jumbotron">
      <div class="container">
        <h3>聚好看频次数据统计</h3>
        <a class="btn btn-default" href="/charts">返回首页</a>
      </div>
    </div>

    <div class="container">
      <div class="row">
        
        <div class="list-group">
          <a href="playtimes" class="list-group-item"><h3>总体点播频次统计</h3>
            <p>统计标准：对聚好看系统中所有的视频点播次数</p>
          </a>
          <a href="playtimes?vender=cntv" class="list-group-item"><h3>iCNTV点播频次统计</h3>
            <p>统计标准：在聚好看系统中点播过iCNTV片源的次数</p>
          </a>
          <a href="playtimes?vender=iqiyi" class="list-group-item"><h3>爱奇艺点播频次统计</h3>
            <p>统计标准：在聚好看系统中点播过爱奇艺片源的次数</p>
          </a>
          <a href="playtimes?vender=other" class="list-group-item"><h3>其他点播频次统计</h3>
            <p>统计标准：在聚好看系统中点播过其他片源的次数</p>
          </a>
        </div>
      </div>
    </div>
  </body>
</html>
