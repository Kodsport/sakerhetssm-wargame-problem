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
            const flagga = strxor("\x12\x03\b\x06\x01\x12\n\x14/\t\x15\x10\x02\x0F\x05\x15\x163\x11\x05\x07>\x11\x01\x01\x1A\x07O\x1C", "apelsin")
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
