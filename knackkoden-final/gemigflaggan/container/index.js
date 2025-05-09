const express = require('express');
const fileUpload = require('express-fileupload');
const path = require('path');
const exifParser = require('exif-parser');

const app = express();
const PORT = 3000;

app.use(fileUpload());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/upload', (req, res) => {
    if (!req.files || !req.files['image-file']) {
        return res.json({ success: false, message: 'Ingen bildfil uppladdad. Vänligen försök igen.' });
    }

    const fileBuffer = req.files['image-file'].data;

    try {
        // Läs och extrahera EXIF-data
        const parser = exifParser.create(fileBuffer);
        const result = parser.parse();

        // Kontrollera om EXIF-data innehåller den önskade texten "gemigflaggan"
        const exifData = JSON.stringify(result.tags);
        if (exifData.includes('gemigflaggan')) {
            res.json({ success: true, message: 'Grattis! Du hittade den dolda EXIF-texten.', flag: 'SSM{377_v41d1gt_d4117_pr070k011}' });
        } else {
            res.json({ success: false, message: 'Den nödvändiga texten "gemigflaggan" hittades inte i EXIF-datan. Försök igen!' });
        }
    } catch (error) {
        res.json({ success: false, message: 'Fel vid läsning av EXIF-data. Vänligen försök med en giltig bildfil.' });
    }
});

app.listen(PORT, () => {
    console.log(`Servern körs på http://localhost:${PORT}`);
});

