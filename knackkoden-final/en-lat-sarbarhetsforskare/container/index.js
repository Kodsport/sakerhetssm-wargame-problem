const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());
app.use(express.static('views'));

// Kontrollera om länken innehåller en giltig kommentar
app.post('/check', async (req, res) => {
    const { lineUrl } = req.body;

    if (!lineUrl || !lineUrl.startsWith('https://github.com/')) {
        return res.json({ success: false, message: 'Ogiltig URL till GitHub. Ange en giltig URL.' });
    }

    // Kontrollera om URL:n följer rätt format
    const match = lineUrl.match(/^https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/blob\/(master|[0-9a-f]*)\/(.+)#L(\d+)$/);
    if (!match) {
        return res.json({ success: false, message: 'URL:en måste peka till en specifik rad i master-branchen.' });
    }

    const user = match[1];
    const repo = match[2];
    const filePath = match[4];
    const lineNumber = parseInt(match[5], 10);

    try {
        // Hämta innehållet i filen
        const response = await axios.get(`https://raw.githubusercontent.com/${user}/${repo}/master/${filePath}`);
        const fileContent = response.data.split('\n');

        // Kontrollera om raden innehåller den önskade kommentaren
        if (lineNumber > 0 && lineNumber <= fileContent.length) {
            const lineContent = fileContent[lineNumber - 1];
            if (/FIXME.*buffer overflow/.test(lineContent)) {
                return res.json({ success: true, message: 'Grattis! Du hittade en matchande kommentar.', flag: 'SSM{h4ck4_pl4n373n}' });
            } else {
                return res.json({ success: false, message: 'Ingen matchande kommentar på den angivna raden.' });
            }
        } else {
            return res.json({ success: false, message: 'Den angivna raden finns inte i filen.' });
        }
    } catch (error) {
        console.error(error);
        res.json({ success: false, message: 'Fel vid åtkomst av GitHub. Kontrollera att länken är korrekt och att repositoryn är offentlig.' });
    }
});

app.listen(PORT, () => {
    console.log(`Servern körs på http://localhost:${PORT}`);
});
