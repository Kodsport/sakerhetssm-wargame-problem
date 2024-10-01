<html>

<head>
    <meta charset="UTF-8">
    <title>Skibidi knapp</title>
    <style>
           body { font-family: Courier; background-color: black; } 
           h1 { color: #00FF00; }
           button { color: #0000FF; }
    </style>
    <script>
        function strxor(enc, key)
        {
            var ret = '';
            for (var i = 0; i < enc.length; i++)
                ret += String.fromCharCode(enc.charCodeAt(i) ^ key.charCodeAt(i % key.length));
            return ret;
        }
        function fåFlagga() {
            const flagga = strxor("\x11\x12\x03\x0b\x1c\x19\x05\x1b\x3e\x02\x1b\x02\x05\x00\x0a\x07\x12\x31\x0a\x02\x0b\x02\x05\x00\x31\x0f\x08\x09\x40\x13", "banan")
            console.log(flagga)
            document.getElementById('b').innerHTML += "<h1>Grattis! Flaggan är " + flagga + "</h1>"
        }
        </script>
</head>
<body id="b">
    <h1>Varsågod och ta en flagga!</h1>
    <button disabled onclick="fåFlagga()">Klicka här för att få flaggan!</button>
</body>

</html>
