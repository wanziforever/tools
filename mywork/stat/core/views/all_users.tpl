<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <title>聚好看活跃用户数统计</title>
    <link href="../../static/css/bootstrap/3.0.0/bootstrap.min.css" rel="stylesheet">
    <script src="../../static/js/jquery-1.11.1.min.js"></script>
    <script src="../../static/js/bootstrap/3.0.0/bootstrap.min.js"></script>
    <script type="text/javascript" src="../../static/js/Chart.js"></script>
  </head>

  <body onLoad="init()">
    <div class="container">
      <div class="jumbotron">
        <h2>聚好看联网用户数统计</h2>
        <a class="btn btn-default" href="users">返回用户首页</a>
      </div>
    
    <script type="text/javascript">

      window.onLoad = function() {
      init();
      };

      function init() {
      var ctx = $("#myChart").get(0).getContext("2d");

      var data = {
      labels: [
      % for day in days[:-1]:
      '{{day}}',
      % end
      '{{days[-1]}}'  
      ],
      datasets: [
      {
      fillColor: "rgba(220,220,220,0.5)",
      strokeColor: "rgba(220,220,220,1)",
      pointColor: "rgba(220,220,220,1)",
      pointStrokeColor: "#fff",
      data: {{data}}
      },
      //{
      //fillColor: "rgba(151,187,205,0.5)",
      //strokeColor: "rgba(151,187,205,1)",
      //pointColor: "rgba(151,187,205,1)",
      //pointStrokeColor: "#fff",
      //data: [28, 48, 40, 19, 96, 27, 100]
      //}
      ]
      }

      var myNewChart = new Chart(ctx).Line(data);
      }

    </script>
    <div>
      <section>
        <article>
          <canvas id="myChart" width="1100" height="300">
          </canvas>
        </article>
      </section>
      <a class="btn btn-primary" href="allusers?to={{pre_to_day}}&intvl={{intvl}}">向前30天</a>
      <a class="btn btn-primary" href="allusers?to={{next_to_day}}&intvl={{intvl}}">向后30天</a>
    </div>
    </div>
  </body>
  </html>
