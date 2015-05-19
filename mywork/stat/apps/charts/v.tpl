<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <title>Become a member</title>
    <script type="text/javascript" src="Chart.js"></script>
    <script src="jquery-1.11.1.min.js"></script>
  </head>

  <body onLoad="init()">
    <script type="text/javascript">

      window.onLoad = function() {
      init();
      };

      function init() {
      var ctx = $("#myChart").get(0).getContext("2d");

      var data = {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
      {
      fillColor: "rgba(220,220,220,0.5)",
      strokeColor: "rgba(220,220,220,1)",
      pointColor: "rgba(220,220,220,1)",
      pointStrokeColor: "#fff",
      data: [65, 59, 90, 81, 56, 55, 40]
      },
      {
      fillColor: "rgba(151,187,205,0.5)",
      strokeColor: "rgba(151,187,205,1)",
      pointColor: "rgba(151,187,205,1)",
      pointStrokeColor: "#fff",
      data: [28, 48, 40, 19, 96, 27, 100]
      }
      ]
      }

      var myNewChart = new Chart(ctx).Line(data);
      }

    </script>
    <div>
      <section>
        <article>
          <canvas id="myChart" width="400" height="400">
          </canvas>
        </article>
      </section>
    </div>
  </body>
  </html>
