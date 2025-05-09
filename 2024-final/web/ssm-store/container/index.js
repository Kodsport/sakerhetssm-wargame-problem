const express = require('express');
const bodyParser = require('body-parser');
var cookieParser = require('cookie-parser')
const path = require('path');
const fs = require('fs');
require('dotenv').config() // needed for stripe key
const stripe = require('stripe')(process.env.STRIPE_KEY);
var crypto = require("crypto");

const app = express();


app.use(cookieParser())


app.post('/stripe_webhook', express.raw({type: "*/*"}), (req, res) => {
    const sig = req.headers['stripe-signature'];

    let event;
  
    try {
      event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET); // TODO: test with generateTestHeaderString?
    } catch (err) {
      console.error('Webhook error:', err.message);
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }
    console.log(event)
    if (!event.livemode) {
      res.json({ nah: "no dev env" });
        return;
    }
    
    console.log(event)
  
    // Handle the event based on its type
    switch (event.type) {
      case 'payment_intent.succeeded':
        // Handle successful payment
        console.log('PaymentIntent was successful!');

        const hexRegex = /^[0-9a-fA-F]{64}$/;
        if (!hexRegex.test(event.client_reference_id)) {
          res.json({ nah: "bruh" });
          return;
        }

        fs.writeFileSync('./carts/' + event.client_reference_id, process.env.FLAG)

        break;
      case 'payment_intent.payment_failed':
        // Handle failed payment
        console.log('PaymentIntent failed!');
        break;
      // Add more cases to handle other event types as needed
      default:
        console.log(`Unhandled event type: ${event.type}`);
    }
  
    // Return a response to acknowledge receipt of the event
    res.json({ received: true });
})

app.use(bodyParser.json());


app.get('/flag', (req, res)=>{
  res.setHeader('Content-Type', 'text/html')
  res.sendFile(path.join(__dirname, 'carts', path.normalize('/'+req.cookies['shop_session'])))
})

app.post('/buy-flag', async (req, res) => {


  const id = crypto.randomBytes(32).toString('hex');
  res.cookie('shop_session', id);

  fs.writeFileSync(__dirname + '/carts/' + id, "Cart is not paid for yet")

    const session = await stripe.checkout.sessions.create({
      line_items: [
        {
          price: 'price_1OwmABGQEtULAKKdgZCy4Fp7',
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOW9pYzF1N2JzNml2cWR0a2s2dGE3OXkzeHptM3VqYWsycWo0eGMyZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Od0QRnzwRBYmDU3eEO/giphy.gif`,
      cancel_url: `https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGx1dndjOXhoMzhiNzVkaGpjMnIzaHE2aDh0MzNsbjY0bjJtMzZ4ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KOUp2nbwHm7vy/giphy.gif`,
      client_reference_id: id,
    });
  
    res.redirect(303, session.url);
});

app.get('*', (req, res) => {
    var filename = req.path;
    
    if (filename == '/') {
        filename = 'index.html'
    }
    
    const filePath = __dirname + path.join('/public/' + filename);
    
    
    fs.readFile(filePath, (err, data) => {
      if (err) {
        console.error('Error reading file:', err);
        res.status(404).send('File not found');
      } else {
        // Determine the content type based on the file extension
        let contentType = 'text/plain';
        if (filename.endsWith('.html')) {
          contentType = 'text/html';
        } else if (filename.endsWith('.css')) {
          contentType = 'text/css';
        } else if (filename.endsWith('.js')) {
          contentType = 'text/javascript';
        }
  
        // Set the appropriate content type header
        res.setHeader('Content-Type', contentType);
        // Send the file content
        res.send(data);
      }
    });
  });


// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});


function makeid(length) {
  let result = '';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
}
