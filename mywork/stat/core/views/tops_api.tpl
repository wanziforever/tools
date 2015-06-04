<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <title>聚好看接口性能趋势</title>
    <link href="../../static/css/bootstrap/3.0.0/bootstrap.min.css" rel="stylesheet">
    <script src="../../static/js/jquery-1.11.1.min.js"></script>
    <script src="../../static/js/bootstrap/3.0.0/bootstrap.min.js"></script>
    <script type="text/javascript" src="../../static/js/Chart.js"></script>
  </head>

  <body onLoad="init()">
    <div class="container">
      聚好看接口性能峰值
      <button type="button" class="btn btn-info">{{api}}</button>
      <br>
    </div>
    
    <script type="text/javascript">

      window.onLoad = function() {
      init();
      };

      function init() {
      var ctx = $("#myChart").get(0).getContext("2d");

      var data = {
      labels: [
      % for d in days[:-1]:
      '{{d}}',
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
          <canvas id="myChart" width="1400" height="300">
          </canvas>
        </article>
      </section>
    </div>
    <div class="container">
      <a class="btn btn-primary" href="tops_api?to={{pre_to_day}}&api={{api}}">向前{{interval}}天</a>
      <a class="btn btn-primary" href="tops_api?to={{next_to_day}}&api={{api}}">向后{{interval}}天</a>
      <a class="btn btn-default" href="tops">返回全部接口页面</a>

    </div>
  </body>
  </html>
