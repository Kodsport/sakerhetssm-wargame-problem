<?php
function validate_xml($url) {
    $parsed_url = parse_url($url);
    if($parsed_url === false) {
      echo "Invalid URL provided.";
      return false;
    }

    if(!($parsed_url['scheme'] === 'http' || $parsed_url['scheme'] === 'https')) {
      echo "Only HTTP and HTTPS protocols supported.";
      return false;
    }

    $xml_data = @file_get_contents($url, false, stream_context_create(["ssl"=>["verify_peer"=>false,"verify_peer_name"=>false]]));

    if($xml_data === false) {
        echo "Failed to fetch XML from URL: " . $url . "\n";
        return false;
    }

    @libxml_disable_entity_loader(false);
    libxml_use_internal_errors(true);
    $xml = simplexml_load_string($xml_data, 'SimpleXMLElement', LIBXML_NOENT);

    if($xml === false) {
        echo "<p>Errors while parsing URL:</p>\n<ul class=\"collection\">\n";
        foreach(libxml_get_errors() as $error) {
            //var_dump($error);
            echo "<li  class=\"collection-item\">Error line " . $error->line . ", column " . $error->column . ": " . $error->message . "</li>\n";
        }
        echo "</ul>\n";
    } else {
        echo "Congratulations, the XML is valid!";
        //var_dump($xml);
    }

    return true;
}
?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>XML Validator</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style>
      #wrapper {
        width: 800px;
        margin: 40px auto;
      }
    </style>
    <script>
      function set_url(url) {
        let url_input = document.getElementById('xml_url');
        url_input.value = url;
        return false;
      }
    </script>
  </head>
  <body>
    <div id="wrapper">
      <h1>XML Validator</h1>
    <?php
    if(isset($_POST['url'])) {
      ?>
      <p><a href="/">&lt; Back</a></p>
      <?php
        validate_xml($_POST['url']);
    } else {
        ?>
        <p>Welcome to the XML validator! Please provide a URL below to the XML file you want to validate.</p>
        <p>You can test the service with one of our example XML files: <a href="#" onclick="return set_url('https://<?=$_SERVER['HTTP_HOST']; ?>/example.xml');">/example.xml</a> and <a href="#" onclick="return set_url('https://<?=$_SERVER['HTTP_HOST']; ?>/broken.xml');">/broken.xml</a>. </p>
        <form action="" method="post">
          <label for="url">URL:</label><input id="xml_url" name="url" type="text" placeholder="https://<?=$_SERVER['HTTP_HOST']; ?>/example.xml">
          <button class="btn waves-effect waves-light" type="submit" name="action">
          Validate <i class="material-icons right">send</i>
          </button>
        </form>
        <?php
    }
    ?>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
  </body>
</html>
