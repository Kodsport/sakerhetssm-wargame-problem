<html>

<head>
    <meta charset="UTF-8">
    <title>Avstängd knapp</title>
    <style>
           body { font-family: Courier; background-color: black; } 
           h1 { color: #00FF00; }
           button { color: #0000FF; }
    </style>
    <script>
        document.cookie = 'admin=false'
        function strxor(enc, key)
        {
            var ret = '';
            for (var i = 0; i < enc.length; i++)
                ret += String.fromCharCode(enc.charCodeAt(i) ^ key.charCodeAt(i % key.length));
            return ret;
        }
        function fåFlagga()
        {
            if (!document.cookie.toLowerCase().includes('admin=true'))
                return
            const flagga = strxor("2#(\x17\x17\x1c1\r\t\x06\x07\x12\r\x0b\x12/\x07\x00\x1a6\x0f\x05\x1d\x0c\x02R\x14", "apelsin")
            console.log(flagga)
            document.getElementById('b').innerHTML += "<h1>Grattis! Flaggan är " + flagga + "</h1>"
        }
        </script>
</head>
<body id="b">
    <h1>Välkommen till min jättesäkra sida!</h1>
    <button onclick="fåFlagga()">Hemlig knapp som bara adminen får klicka...</button>
</body>

</html>
