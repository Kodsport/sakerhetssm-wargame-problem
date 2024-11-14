const express = require('express');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;

const SECRET_KEY = "weaksecret";

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'views')));

function authenticateToken(req, res, next) {
    const token = req.query.token;
    if (!token) {
        return res.status(401).json({ message: 'Access Denied' });
    }

    try {
        const decoded = jwt.decode(token, { complete: true });
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(401).json({ message: 'Invalid Token' });
    }
}

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'login.html'));
});

app.post('/login', (req, res) => {
    const { username } = req.body;

    if (username === 'admin') {
        return res.status(403).json({ message: 'Du kan inte skapa en token för användaren "admin" via denna sida.' });
    }

    const payload = {
        username: username
    };

    const token = jwt.sign(payload, SECRET_KEY, { algorithm: 'HS256' });
    res.json({ token });
});

app.get('/admin', authenticateToken, (req, res) => {
    if (req.user.payload.username === 'admin') {
        return res.json({ message: 'Grattis! Här är din flagga: SSM{tack_för_att_jag_fick_låna_din_token}' });
    } else {
        return res.status(403).json({ message: 'Endast administratörer har åtkomst.' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
