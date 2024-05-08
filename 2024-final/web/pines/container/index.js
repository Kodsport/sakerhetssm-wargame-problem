const express = require('express');
const cookieParser = require("cookie-parser");
const escape = require('escape-html');
const fs = require('fs');
const process = require('child_process');

const app = express();
app.use(cookieParser());
app.use(express.static('public'));

app.use((req, res, next) => {
    if (!req.cookies['PHPSESSID']) {
        req.session_id = process.execSync('php -r "session_start();echo session_id();"');
        res.setHeader('Set-Cookie', `PHPSESSID=${req.session_id}; path=/`);
    } else {
        req.session_id = escape(req.cookies['PHPSESSID']);
    }
    next();
});


app.get('/', (req, res) => {
    res.send(process.execFileSync('php', ['-r', fs.readFileSync('index.php').toString().replace('_PHPSESSID_', req.session_id)], { timeout: 3000 }).toString());
});

app.post('/', (req, res) => {
    process.execFileSync('php', ['-r', fs.readFileSync('update.php').toString().replace('_PHPSESSID_', req.session_id)], { timeout: 3000 });
    res.redirect('/');
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});