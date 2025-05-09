var http = require('http');
const fs = require('fs');

const file = fs.readFileSync('./huvudaxlarkna.m4a')

http.createServer(function (req, res) {
  
  if (req.url.includes("mp3")) {
    res.setHeader("X-Flag", "erer_kneer_t0e3r}");
    res.write(file, 'binary');
    res.end(null, 'binary');
    return
  }
  
  
  res.write(`
  <html>
    <head>
      <meta charset="UTF-8"> 
        <title>Huvud, axlar, knä och tå</title>
        <!--- SSM{header_should --->
        <!--- finns det flera huvud:er? -->
    </head>
    <body>
      <h1> huvud, axlar, knä, tå </h1>
      <audio controls onplay="gif.style = ''">
        <source src="/x.mp3" type="audio/mp3">
        </audio>
        <br>
        <img id="gif" style="display: none"  src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXE4bXBxdWgyaTFrYXMyaHRzcGc5ODVvMmMyMzhmYnp1bmd1bGV0MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FIyOndr9jvel8vTHLH/giphy.gif">
      </body>
  </html>
  
  `);
  res.end();
}).listen(8080);
