<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <title>vod_statistic_duration_portal</title>
    <link href="../../static/css/bootstrap/3.0.0/bootstrap.min.css" rel="stylesheet">
    <script src="../../static/js/jquery-1.11.1.min.js"></script>
    <script src="../../static/js/bootstrap/3.0.0/bootstrap.min.js"></script>
    <script type="text/javascript" src="../../static/js/Chart.js"></script>
  </head>

  <body>
    <div class="jumbotron">
      <div class="container">
        <h3>聚好看时长数据统计</h3>
        <a class="btn btn-default" href="/charts">返回首页</a>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <p><span class="label label-default">总点播时长</span></p>
          <div class="list-group">
            <a href="playduration" class="list-group-item"><h3>总体点播时长统计</h3>
              <p>统计标准：对聚好看系统中所有的视频点播时长数，单位：分钟</p>
            </a>
            <a href="playduration?vender=cntv" class="list-group-item"><h3>iCNTV点播时长统计</h3>
              <p>统计标准：在聚好看系统中点播过iCNTV片源的点播时长数，单位，分钟</p>
            </a>
            <a href="playduration?vender=iqiyi" class="list-group-item"><h3>爱奇艺点播时长统计</h3>
              <p>统计标准：在聚好看系统中点播过爱奇艺片源的点播时长数，单位：分钟</p>
            </a>
            <a href="playduration?vender=other" class="list-group-item"><h3>其他点播时长统计</h3>
              <p>统计标准：在聚好看系统中点播过其他片源的点播时长数，单位：分钟</p>
            </a>
          </div>
        </div>
        <div class="col-md-6">
          <p><span class="label label-default">人均点播时长</span></p>
          <div class="list-group">
            <a href="playdurationrate" class="list-group-item"><h3>总体人均点播时长</h3>
              <p>统计标准：对聚好看系统中所有的视频点播时长数，单位：分钟</p>
            </a>
            <a href="playdurationrate?vender=cntv" class="list-group-item"><h3>iCNTV人均点播时长统计</h3>
              <p>统计标准：在聚好看系统中点播过iCNTV片源的点播时长数，单位，分钟</p>
            </a>
            <a href="playdurationrate?vender=iqiyi" class="list-group-item"><h3>爱奇艺人均点播时长统计</h3>
              <p>统计标准：在聚好看系统中点播过爱奇艺片源的点播时长数，单位：分钟</p>
            </a>
            <a href="playdurationrate?vender=other" class="list-group-item"><h3>其他人均点播时长统计</h3>
              <p>统计标准：在聚好看系统中点播过其他片源的点播时长数，单位：分钟</p>
            </a>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
