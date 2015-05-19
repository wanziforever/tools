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

  <body>
    <div class="container">
      <div class="row">

        <div class="list-group">
          % for row in rows:
          {{!row}}
          % end
        </div>
      </div>
    </div>
  </body>
</html>
