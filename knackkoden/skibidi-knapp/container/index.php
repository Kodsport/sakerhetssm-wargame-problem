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
            const flagga = strxor("12#\x1a\n\x17>\x02\x18\r\t\x00\n\x04\x1d=\n\x02\x08\r\t\x001\x0c\x07\x05@\x13", "banan")
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
