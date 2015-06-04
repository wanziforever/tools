<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <title>聚好看用户统计</title>
    <script type="text/javascript" src="../../static/js/Chart.js"></script>
    <script src="../../static/js/jquery-1.11.1.min.js"></script>
    <link href="../../static/css/bootstrap/3.0.0/bootstrap.min.css" rel="stylesheet">
    <script src="../../static/js/bootstrap/3.0.0/bootstrap.min.js"></script>
  </head>

  <body onLoad="init()">
    <script type="text/javascript">

      window.onLoad = function() {
      init();
      };

      function init() {
          init_active_users()
          init_play_users()
      }

      function init_active_users() {
          var act_ctx = $("#ActUserChart").get(0).getContext("2d");

          var actdata = {
              labels: [
                      % for day in actdays[:-1]:
                  '{{day}}',
                      % end
                  '{{actdays[-1]}}'  
              ],
              datasets: [
                  {
                      fillColor: "rgba(220,220,220,0.5)",
                      strokeColor: "rgba(220,220,220,1)",
                      pointColor: "rgba(220,220,220,1)",
                      pointStrokeColor: "#fff",
                      data: {{actdata}}
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

          var actChart = new Chart(act_ctx).Line(actdata);
      }

      function init_play_users() {
          var play_ctx = $("#PlayUserChart").get(0).getContext("2d");

          var playdata = {
              labels: [
                      % for day in playdays[:-1]:
                  '{{day}}',
                      % end
                  '{{playdays[-1]}}'  
              ],
              datasets: [
                  {
                      fillColor: "rgba(220,220,220,0.5)",
                      strokeColor: "rgba(220,220,220,1)",
                      pointColor: "rgba(220,220,220,1)",
                      pointStrokeColor: "#fff",
                      data: {{playdata}}
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

          var playChart = new Chart(play_ctx).Line(playdata);
      }

    </script>
    <div>
      <section>
        <article>
          <span class="label label-default">活跃用户</span>
          <canvas id="ActUserChart" width="1400" height="300">
          </canvas>
          <span class="label label-default">点播用户</span>
          <canvas id="PlayUserChart" width="1400" height="300">
          </canvas>
        </article>
      </section>
    </div>
  </body>
</html>
