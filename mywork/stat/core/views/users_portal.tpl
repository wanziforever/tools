<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <title>vod_statistic_user_portal</title>
    <link href="../../static/css/bootstrap/3.0.0/bootstrap.min.css" rel="stylesheet">
    <script src="../../static/js/jquery-1.11.1.min.js"></script>
    <script src="../../static/js/bootstrap/3.0.0/bootstrap.min.js"></script>
    <script type="text/javascript" src="../../static/js/Chart.js"></script>
  </head>

  <body>
    <div class="jumbotron">
      <div class="container">
        <h3>聚好看用户数据统计</h3>
        <a class="btn btn-default" href="/charts">返回首页</a>
      </div>
    </div>

    <div class="container">
      <div class="row">
        
        <div class="list-group">
          <a href="allusers" class="list-group-item"><h3>总联网用户统计</h3>
            <p>统计标准：所有对聚好看发出过启动请求的用户数，注: VIDAA终端的聚好看随整机而启动</p>
          </a>
          <a href="actusers" class="list-group-item"><h3>活跃用户统计</h3>
            <p>统计标准：对聚好看进行过任何点击行为的用户，对聚好看切换过导航的用户</p>
          </a>
          <a href="playusers" class="list-group-item"><h3>总体点播用户统计</h3>
            <p>统计标准：对聚好看进行过任何点播行为的用户数</p>
          </a>
          <a href="playusers?vender=cntv" class="list-group-item"><h3>iCNTV点播用户统计</h3>
            <p>统计标准：在聚好看系统中点播过iCNTV片源的用户数</p>
          </a>
          <a href="playusers?vender=iqiyi" class="list-group-item"><h3>爱奇艺点播用户统计</h3>
            <p>统计标准：在聚好看系统中点播过爱奇艺片源的用户数</p>
          </a>
        </div>
      </div>
    </div>
  </body>
</html>
