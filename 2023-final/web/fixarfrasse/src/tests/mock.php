<?php
function file_get_contents($path) {
    if(str_starts_with($path, "file:/")) {
        die("EXPLOITED!");
    }
    if(str_starts_with($path, "php:/")) {
        die("EXPLOITED!");
    }
    if(str_starts_with($path, "http://127.0.0.1")) {
        die("EXPLOITED!");
    }

    if(str_contains($path, "dunderhonung")) {
        return "SECRET_CONTENT_784839078123643675";
    }

    if(str_contains($path, "potatis")) {
        return "SECRET_CONTENT_879123867345451236";
    }
}

chdir($_GET['testfile']);
unset($_GET['testfile']);
unset($_REQUEST['testfile']);

include 'index.php';