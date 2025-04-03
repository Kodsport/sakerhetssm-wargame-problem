<?
    include_once("jwt.php");

    // really logged in?
    if (!isset($_COOKIE["s"]) ||
        !verify_jwt($_COOKIE["s"])) {
            // Invalid token, send to logout
            header("Location: logout.php");
            die();
    }

    $token = $_COOKIE["s"];
    $username = get_user($token);
    $isadmin = is_admin($token);
?>

<html>
    <head>
    <title>Flag exchange manager</title>
    </head>
    <body>
        Logged in as <? echo($username); ?>
        <br>
        <br>
        <?
            if ($isadmin) {
                echo("cratectf{th0se_t0ken_s3cre7ts_ar3_pr3c1ou5}");
            }
            else {
                echo("No flags to show.");
            }
        ?>

        <br><br>
        <a href="logout.php">Logout</a>
    </body>
</html>
