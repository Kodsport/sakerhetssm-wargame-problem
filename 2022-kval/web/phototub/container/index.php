<?php
ini_set('upload_max_filesize', 1024*1024*3);

if (array_key_exists('source', $_GET)) {
    highlight_file(__FILE__);
    die();
}

$error = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (!array_key_exists('file', $_FILES)) {
        $error = 'File not found!';
        goto end;
    }

    if (!in_array($_FILES['file']['type'], ['image/png', 'image/jpeg'])) {
        $error = 'Only JPEGs and PNGs are allowed!';
        goto end;
    }

    $filename = bin2hex(random_bytes(8)) . '_' . basename($_FILES['file']['name']);
    $uploadfile = '/var/www/html/uploads/' . $filename;

    if (!$error && move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)) {
        header('Location: /uploads/' . $filename);
        die();
    }
}

end:
?>

<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

    <title>Phototub</title>
    <style>
        .center {
            text-align: center;
        }
        form {
            width: 25rem;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
  </head>
  <body>
    <div class="center">
        <h1>Phototub</h1>
        <h3>The best newest photo sharing site!</h3>

        <img src="/phototub.jpg" alt="A photo tub" class="mb-5">

        <form enctype="multipart/form-data" method="POST">
            <?php if ($error) { ?>
                <div class="alert alert-danger"><?= $error?></div>
            <?php } ?>
            <div class="mb-3">
                <input type="file" class="form-control" name="file" required>
                <div id="emailHelp" class="form-text">Only JPEGs and PNGs <= 3MB</div>
            </div>
            <div class="mb-3">
                <button class="btn btn-primary" type="submit">Upload image</button>
            </div>
        </form>

        <a href="/?source">Source</a>
    </div>
  </body>
</html>
