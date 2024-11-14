const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static('public')); // Serves static files from the "public" folder (where your HTML, CSS, JS files are stored)

app.post('/validate', (req, res) => {
    const { vector1, vector2 } = req.body;
    const treasurePoint = { x: 5, y: 8 };

    // Check if the treasure point can be represented as an integer combination of vector1 and vector2
    let found = false;
    for (let i = -15; i <= 15; i++) {
        for (let j = -15; j <= 15; j++) {
            if (i * vector1.x + j * vector2.x === treasurePoint.x && i * vector1.y + j * vector2.y === treasurePoint.y) {
                found = true;
                break;
            }
        }
        if (found) break;
    }

    if (found) {
        res.json({ success: true, message: "✨ Grattis! Du har hittat skatten! Här är din flagga: SSM{vilken_dr0m_med_en_reducerad_skatt} ✨" });
    } else {
        res.json({ success: false, message: "Ingen skatt hittades. Försök att justera vektorerna." });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
