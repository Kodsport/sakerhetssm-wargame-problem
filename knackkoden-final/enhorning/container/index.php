<?php
session_start();

$host = '127.0.0.1';  // Use 127.0.0.1 for a TCP connection
$user = 'root';
$pass = 'password';
$dbname = 'unicorn_magic';

$conn = new mysqli($host, $user, $pass, $dbname);
$conn->set_charset("utf8");  // Set charset to utf8 for åäö support
if ($conn->connect_error) {
    die("Anslutning misslyckades: " . $conn->connect_error);
}

// Visa alla enhörningar utom "FlagUnicorn" när sidan öppnas via GET-förfrågan
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    // Hämta endast enhörningar som inte är "FlagUnicorn"
    $sql = "SELECT * FROM unicorns WHERE name != 'FlagUnicorn'";
    $result = $conn->query($sql);

    echo "<!DOCTYPE html>
    <html lang='sv'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Enhörningstränarportalen - Glittrande Enhörningar!</title>
        <style>
            body {
                background: linear-gradient(to bottom right, #ffccff, #ff99ff);
                color: #4b0082;
                text-align: center;
                font-family: 'Comic Sans MS', cursive, sans-serif;
            }
            .unicorn-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                margin-top: 20px;
            }
            .unicorn {
                border: 3px solid pink;
                padding: 15px;
                margin: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: transform 0.2s;
                background: #fff0f5;
            }
            .unicorn:hover {
                transform: scale(1.1);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            }
            .sparkly-button {
                padding: 10px 20px;
                border: none;
                border-radius: 15px;
                background: #ff66cc;
                color: white;
                cursor: pointer;
                font-size: 16px;
                margin-top: 15px;
            }
            .sparkly-button:hover {
                background: #ff3399;
            }
            .search-form {
                margin-top: 20px;
            }
            .search-input {
                padding: 10px;
                margin-right: 5px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
        </style>
    </head>
    <body>
        <h1>🦄 Välkommen till den Glittrande Enhörningstränarportalen! 🦄</h1>
        <p>Skriv namnet på en enhörning för att hitta mer information eller avslöja gömda hemligheter!</p>
        <form method='post' class='search-form'>
            <input type='text' name='unicorn_name' placeholder='Skriv enhörningens namn' class='search-input'>
            <button type='submit' class='sparkly-button'>Sök efter Enhörning</button>
        </form>
        <p style='color: red;'>Tips: Specialtecken eller fraser som ', #, ;, -, or, kan avslöja gömda hemligheter!</p>
        <div class='unicorn-container'>";

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            echo "<div class='unicorn'>
                <h3>✨ " . htmlspecialchars($row['name']) . " ✨</h3>
                <p><strong>Färg:</strong> " . htmlspecialchars($row['color']) . "</p>
                <p><strong>Kraft:</strong> " . htmlspecialchars($row['power']) . "</p>
            </div>";
        }
    } else {
        echo "<p>Inga magiska enhörningar hittades! Försök att lägga till några nya vänner!</p>";
    }

    echo "</div></body></html>";
}

// Hantera POST-förfrågningar för att interagera med en specifik enhörning
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Grundläggande SQL-fråga som är sårbar för injektion för demonstrationssyfte
    $unicorn_name = $_POST['unicorn_name'];
    $sql = "SELECT * FROM unicorns WHERE name = '$unicorn_name'"; // Sårbar fråga för inlärningsändamål

    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        echo "<h2>Välkommen, modiga Enhörningstränare!</h2>";
        echo "<p>Här är den magiska informationen om din enhörning:</p>";
        while ($row = $result->fetch_assoc()) {
            echo "<div style='border: 2px solid pink; padding: 10px; margin: 10px;'>";
            echo "<strong>Namn:</strong> " . htmlspecialchars($row['name']) . "<br>";
            echo "<strong>Färg:</strong> " . htmlspecialchars($row['color']) . "<br>";
            echo "<strong>Kraft:</strong> " . htmlspecialchars($row['power']) . "<br>";
            echo "</div>";
        }
    } else {
        echo "<p style='color: red;'>Ingen enhörning hittades! Försök igen, eller är det ett trick av de Busiga Trollen?</p>";
    }
}
?>
