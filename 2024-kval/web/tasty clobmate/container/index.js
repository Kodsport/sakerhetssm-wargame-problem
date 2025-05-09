const express = require('express');
const bodyParser = require('body-parser');
const crypto = require('crypto');
const helmet = require('helmet');
const cookieParser = require("cookie-parser");
const puppeteer = require("puppeteer");
const bot = require("./bot.js")

const browser = puppeteer.launch({
    pipe: true,
    args: [
        "--no-sandbox",
        "--js-flags=--jitless",
        "--incognito"
    ]
});

const app = express();

app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            upgradeInsecureRequests: null,
        },
    },
}));
app.use(express.static('public'));
app.use(cookieParser());

const PORT = Number(process.env.PORT) || 3000;
const FLAG = process.env.FLAG ?? 'SSM{fake_flag}';
const ADMIN_COOKIE = crypto.randomBytes(32).toString('hex');

let drinks = new Map();

function sleep(ms) {
    return new Promise((res) => setTimeout(res, ms));
}

app.post('/drinks', (req, res) => {
    const { name, flavor, description } = req.body;

    if (typeof name !== 'string' || typeof flavor !== 'string' || typeof description !== 'string') {
        return res.status(400).send({ message: 'Invalid input: name, flavor, and description must be strings' });
    }

    const id = crypto.randomBytes(32).toString('hex');

    const drink = {
        name: name,
        flavor: flavor,
        description: description,
        approved: false
    };

    drinks.set(id, drink);
    res.redirect(`/drinks/${id}`);
});

app.get('/drinks/:id', (req, res) => {
    const id = req.params.id;
    const drink = drinks.get(id);
    if (drink) {
        res.render('drink', { id, ...drink });
    } else {
        res.status(404).send({ message: 'Drink not found' });
    }
});

const isLocalhost = (req) => {
    const ipAddress = req.socket.remoteAddress;
    return ipAddress === '127.0.0.1' || ipAddress === '::1' || ipAddress === '::ffff:127.0.0.1';
};

app.post('/approve/:id', (req, res) => {
    if (!isLocalhost(req)) {
        console.log("auth wrong ip")
        return res.status(403).send({ message: 'You are not coming from the admin ip!' });
    }
    if (req.cookies.admin !== ADMIN_COOKIE) {
        console.log("auth failed no cookie")
        return res.status(403).send({ message: 'You do not have the admin cookie!' });
    }    

    const id = req.params.id;
    const drink = drinks.get(id);
    if (drink) {
        drink.approved = FLAG;
        drinks.set(id, drink);
    }
    res.send({ message: 'Drink approved' });
});

app.get('/', (req, res) => {
    res.render('index');
});


app.get('/admin', (req, res) => {
    res.render('admin', { result: req.query.result });
});

app.post('/admin', async (req, res) => {
    let drinkid = req.body.drinkid;
    let ctx;
    let ret = undefined;
    try {
        ctx = await (await browser).createBrowserContext();
        const prom = Promise.race([
            bot.exec(ctx, drinkid, ADMIN_COOKIE), // Admin bot will visit "http://localhost:3000/drinks/" + drinkid
            sleep(bot.timeout),
        ])
        ret = await prom;
    } catch (err) {
        if (ctx) {
            try {
                await ctx.close();
            } catch (e) { }
        }
        return res.redirect('/admin?result=' + err.message);
    }
    try {
        await ctx.close();
    } catch (e) { }
    res.redirect('/admin?result=Admin has visited your page');
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
