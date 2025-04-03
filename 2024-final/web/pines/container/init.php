<?php
$db = new SQLite3('/app/data/db.sqlite');
$db->query('CREATE TABLE IF NOT EXISTS "pines" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "session_id" STRING,
    "amount" INTEGER)');
