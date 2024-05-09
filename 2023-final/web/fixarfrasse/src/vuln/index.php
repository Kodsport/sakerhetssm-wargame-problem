<?php
ob_start();

$db = new SQLite3(':memory:');
$db->query('CREATE TABLE contacts (id INT PRIMARY KEY, name TEXT NOT NULL, phone TEXT, address TEXT)');
$db->query('INSERT INTO contacts VALUES
            (1, "Bamse", "0800-DUNDER-HONUNG", "Bamses Hus"),
            (2, "Lille Skutt", NULL, "Gammal Stubbe"),
            (3, "Skalman", "+46-1337-1337", "Egendomligt Hus"),
            (4, "Vargen", "[HEMLIGT]", "Skogen"),
            (5, "Farmor", NULL, "Höga Berget");');

$db->query('CREATE TABLE recept (id INT PRIMARY KEY, name TEXT NOT NULL, recept TEXT)');
$db->query('INSERT INTO recept VALUES (1, "Dunderhonung", "[EXTREMT HEMLIGT]");');

function page_404() {
    echo "404";
}

function page_index() {
  ?>
  <div>
    <h1>My Cool Page</h1>
    <p>Welcome to my cool page</p>
    <form method="get" action="">
      Ping host: <input type="text" name="host">
      <input name="submit" type="submit" value="Ping">
      <input name="p" type="hidden" value="ping">
    </form>
    <form method="get" action="">
      Search contacts: <input type="text" name="contact">
      <input name="submit" type="submit" value="Search">
      <input name="p" type="hidden" value="search">
    </form>
    <form method="get" action="">
      Check stocks data: <input type="text" name="stocks">
      <input name="submit" type="submit" value="Search">
      <input name="p" type="hidden" value="stocks">
    </form>
  </div>
  <?php
}

function page_ping() {
  ?>
  <div>
    <h1>Ping Results</h1>
    <pre>
      <?=system("ping -c1 " . $_GET['host']); ?>
    </pre>
  </div>
  <?php
}

function page_stocks() {
  ?>
  <div>
    <h1>Todays stocks</h1>
    <?php
    $url = $_GET['stocks'] ? $_GET['stocks'] : "https://hoga.berget.se/stocks/dunderhonung.json";
    // Assume "allow_url_fopen=true"
    $stocks_data = file_get_contents($url);
    echo $stocks_data;
    ?>
  </div>
  <?php
}

function page_search($db) {
    ?>
    <div>
      <h1>Search results for "<?=$_GET['contact']; ?>"</h1>
      <?php
      $s = $_GET['contact'];
      $results = $db->query('SELECT * FROM contacts WHERE name LIKE "%' . $s . '%" OR phone LIKE "%' . $s . '%" OR address LIKE "%' . $s . '%";');
      while ($row = $results->fetchArray()) {
        ?><li><?=$row['name'];?>, <?=$row['phone'];?>, <?=$row['address'];?></li><?php
      }
      ?>
      <ul>
      </ul>
    </div>
    <?php
}

function page_admin() {
  if($_SERVER['REMOTE_ADDR'] != '127.0.0.1') { die("Access denied!"); }
  ?>
  <div>
    <h1>Admin page</h1>
    <p>
      Hemlig plan för att stjäla dunderhonungen: [KRYPTERAT]
    </p>
  </div>
  <?php
}

$page = isset($_GET['p']) ? $_GET['p'] : 'index';
switch ($page) {
    case 'index':
      page_index();
      break;
    case 'ping':
      page_ping();
      break;
    case 'search':
      page_search($db);
      break;
    case 'stocks':
      page_stocks();
      break;
    case 'admin':
      page_admin();
      break;
    default:
      page_404();
      break;
}

$body = ob_get_clean();
?>
<!DOCTYPE html>
<html>
  <head>
    <title>My really cool website</title>
  </head>
  <body>
  <?=$body; ?>
  <span>Current time: <?=time(); ?></span>
  </body>
</html>
