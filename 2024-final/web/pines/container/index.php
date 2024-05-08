$session_id = "_PHPSESSID_";
$db = new SQLite3('/app/data/db.sqlite');
$total = $db->querySingle("SELECT count(*) FROM pines");
$self = $db->querySingle("SELECT count(*) FROM pines WHERE session_id = '$session_id'");

echo <<<HTML
<html>

    <head>
        <title>The Office of Truthful Pine Forest Surveillance and Enforcement Oversight under the Sovereign Authority
            of Iceland</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>

    <div>
        <h1>The Office of Truthful Pine Forest Surveillance and Enforcement Oversight under the Sovereign Authority of Iceland</h1>
        <p>Dear citizen,</p>
        <p>Thank you for your vigilance in reporting pine sightings. Your reports are important to us and help us to
            keep the Pine Forest safe and secure.</p>
        <p>Remember, if you see something, say something!</p>
    </div>

    <div>
        <h2>Pine statistics</h2>
        <p>Total pines sighted: $total</p>
        <p>Your pines: $self</p>
    </div>
    <div>
        <h2>Report pine sighting</h2>
        <p>Report a pine sighting by clicking the button below.</p>

        <form method="POST">
            <input type="submit" value="Report pine sighting" />
        </form>
    </div>
    </div>

</html>
HTML;
