<?php
error_reporting(0);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $users = [
        'admin' => '00e9115554617769276224983939931756498863',
        'hare'  => '0e92477519284007915582397909940677463532'
    ];
    
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    if (hash('haval160,5', $password) == $users[$username]) {
        $authenticated = true;
    } else {
        $authenticated = false;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>rätt så cool sida</title>
	<link rel="stylesheet" href="https://unpkg.com/sakura.css/css/sakura.css" type="text/css">
</head>
<body>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username">
        <label>Password:</label>
        <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (empty($username) || empty($password)) {
            echo 'Make sure you\'ve filled in your username and/or password.';
        }
        else if ($authenticated) {
            echo 'Well done! Harald tells me to give you this flag: ' . file_get_contents('/flag.txt');
        } else {
            echo 'Invalid login credentials.';
        }
    }
    ?>
    <br>
    <a href="/source.php">
        <img border="0" alt="sauce" src="/sauce.png">
    </a>
</body>
</html>
