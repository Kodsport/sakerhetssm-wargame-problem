$session_id = "_PHPSESSID_";
$db = new SQLite3('/app/data/db.sqlite');
$db->query('CREATE TABLE IF NOT EXISTS "pines" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "session_id" STRING,
    "amount" INTEGER)');
$db->query("INSERT INTO pines (session_id, amount) VALUES ('$session_id', 1)");
