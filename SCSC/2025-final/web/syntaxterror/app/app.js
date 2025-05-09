const express = require('express');
const multer = require('multer');
const extractZip = require('extract-zip');
const fs = require('fs');
const fsp = fs.promises;
const path = require('path');
const crypto = require('crypto');
const jsyaml = require('js-yaml');
const openapiParser = require('@readme/openapi-parser');

const app = express();
const port = process.env.PORT || 3000;

const upload = multer({
    limits: { fileSize: 1 * 1024 * 1024 }, // 1MB
    fileFilter: (req, file, cb) => {
        if (file.mimetype === 'application/zip') {
            cb(null, true);
        } else {
            cb(new Error('Only ZIP files are allowed'), false);
        }
    }
});

const getFlag = function(){
    const { spawnSync } = require( 'child_process' );
    const flag = spawnSync('/flagout', []);
    return `${flag.stdout.toString()} - ${ flag.stderr.toString() }`;
}

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const readfile = function(fileName, type='json'){
    if (type == 'json'){
        return require(fileName);
    }else{
        return fs.readFileSync(fileName, 'utf8');
    }
}

app.post('/upload', upload.single('zipfile'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded or invalid file type' });
    }
    try {
        const tempDir = path.join('/tmp', `upload-${crypto.randomBytes(16).toString('hex')}`);
        const tempZip = path.join(tempDir, 'upload.zip');
        await fsp.mkdir(tempDir, { recursive: true });
        await fsp.writeFile(tempZip, req.file.buffer);
        let codeFiles = [];
        
        try{
            await extractZip(tempZip, {
                dir: tempDir,
                onEntry: (entry) => {
                    const fileName = entry.fileName;
                    const fileExt = path.extname(fileName).toLowerCase();
                    const allowedExtensions = ['.json'];
                    
                    if (!allowedExtensions.includes(fileExt)) {
                        throw new Error(`${fileName} does not match whitelisted extensions [${allowedExtensions}]!`)
                    }
                    if (entry.fileName != 'info.json') {
                        entry.fileName = `files/${entry.fileName}`;
                        codeFiles.push(path.join(tempDir, entry.fileName));
                    }
                }
            });
        }catch(e){
            throw new Error(`zip error in ${tempZip}:\n ${e.stack}`);
        }

        const info = readfile(path.join(tempDir, 'info.json'));
        let message = "";
        for(selectedFilename of info.files){
            selectedFilename = path.join(tempDir, '/files/', selectedFilename);
            for(fileName of codeFiles){
                if (fileName != selectedFilename){
                    continue;
                }
                if (!['json', 'yaml'].includes(info.type)){
                    throw new Error(`Invalid type: ${info.type}`);
                }
                let parsed = "";
                let parseError;
                parsed = readfile(fileName, info.type);
                if (info.type == 'yaml'){
                    try{
                        parsed = jsyaml.load(parsed);
                    }catch(e){
                        parseError = `Invalid YAML: ${parsed}\n ${e.stack}`;
                        parsed = {};
                    }
                }
                const result = await openapiParser.validate(parsed);
                if (result.valid) {
                    message = '☠️ The API is valid! Time to autohack it!!! ☠️';
                    payload = "' or 1=1 --";
                    const api = await openapiParser.parse(parsed);
                    const baseUrl = api.servers?.pop().url || 'https://example.com';
                    for(apiPath in api.paths){
                        let currentPath = api.paths[apiPath];
                        for(method in currentPath){
                            let methodBig = method.toUpperCase();
                            let currentParameters = currentPath[method]['parameters'];
                            let query = "?";
                            let headers = "";
                            let body = "";
                            let jsonparams = {};
                            for(parameterId in currentParameters){
                                let parameter = currentParameters[parameterId];
                                if (parameter['in'] == 'path') {
                                    apiPath = apiPath.replace(`{${parameter["name"]}}`, encodeURIComponent(payload));
                                } else if (parameter['in'] == 'query') {
                                    query += `${parameter["name"]}=${encodeURIComponent(payload)}&`;
                                } else if (parameter['in'] == 'header') {
                                    headers += ` -H $'${parameter['name']}: ${payload.replace(/'/g, "\\'")}'`
                                }
                            }
                            let currentBodyParameters = currentPath[method]['requestBody']?.['content'];
                            for(contentType in currentBodyParameters){
                                if (!/application[/]json/.test(contentType)){
                                    continue; // no support for now! 
                                }
                                for(parameterId in currentBodyParameters[contentType]?.['schema']?.['properties']){
                                    let currentName = parameterId;
                                    let currentValue = currentBodyParameters[contentType]?.['schema']?.['properties'][parameterId];
                                    if (currentValue.type == 'integer'){
                                        jsonparams[currentName] = 1337;
                                    } else if (currentValue.type == 'string'){
                                        jsonparams[currentName] = payload;
                                    } else {
                                        jsonparams[currentName] = {};
                                    }
                                }
                                body = `-H $'Content-Type: application/json' --data $'${JSON.stringify(jsonparams).replace(/'/g, "\\'")}'`;
                            }
                            message += `\ncurl ${headers} ${body} -X ${methodBig} $'${baseUrl}${apiPath.replace(/'/g, "\\'")}${query.replace(/'/g, "\\'")}'`.replace(/  +/g, ' ');
                        }
                    }
                } else {
                    if (parseError){
                        result.errors.push(parseError);
                    }
                    return res.status(500).json({ error: { messages: result.errors} });
                }
            }
        }

        await fsp.unlink(tempZip);
        await fsp.rm(tempDir, {recursive: true, force: true});

        if (message == ""){
            message = 'no files found!';
        }

        res.json({ 
            message: message, 
            extractionPath: tempDir 
        });
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: { messages: [`The API is not valid: \n${error.stack}`]} });
    }
  });

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});