const express = require('express');
const dotenv = require('dotenv');
const cheerio = require('cheerio');

dotenv.config();

const app = express();
const port = process.env.service_port_api;

app.use(express.json({ limit: '10mb' }));

let info_posts = {}


app.post('/post_html', (req, res) => {
    //console.log('Petición POST recibida:', req.body);

    info_posts[req.body.id] = req.body

    //const $ = cheerio.load(info_posts[req.body.id]);
    //const posts = $('shreddit-post');

    console.log(info_posts)
    res.send('Petición POST procesada con éxito!');
});

app.listen(port, () => {
    console.log(`Servidor escuchando en puerto ${port}`);
});