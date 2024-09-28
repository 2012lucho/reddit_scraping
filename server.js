const express = require('express');
const dotenv = require('dotenv');
const bodyParser = require("body-parser")
const fs = require("fs")
dotenv.config();

const app = express();
const port = process.env.service_port_api;

app.use(bodyParser.json({ limit: '10mb' }));

let info_posts = {}
let cola_process_1_pend = []
let diccio_process_1_pend = []

app.post('/post_html', (req, res) => {
    console.log('/post_html')//, req.body);
    const ID = req.body.id

    if(info_posts[ID]) {
        console.log("Ya hay un elemento con ese ID", ID)
        res.send('Ya hay un elemento con ese ID');
        return
    }

    info_posts[ID] = req.body
    cola_process_1_pend.push(info_posts[ID])
    diccio_process_1_pend[ID] = info_posts[ID]

    console.log(info_posts)
    res.send('Petición POST procesada con éxito!');
})

app.get('/get_process_1', (req, res) => {
    console.log('/get_process_1')//, req.body);

    let item = cola_process_1_pend.pop()
    diccio_process_1_pend[item.id] = item
    let data = (item) ? item : []

    return res.status(200).send({ "item": data });
});

app.listen(port, () => {
    console.log(`Servidor escuchando en puerto ${port}`);
});

const HOY = new Date()
const fecha = String(HOY.getFullYear())+String(HOY.getMonth())+String(HOY.getDate())
const ARCHIVO_RUNTIME = "./resultados/runtime"+fecha+".json"

setInterval(async () => {
    try {
        fs.writeFile(ARCHIVO_RUNTIME, JSON.stringify(info_posts), err => {
            console.log("Done writing"); // Success
        })
    } catch (error) {
        console.log("error al guardar archivo", error)
    }   
}, process.env.INTERVALO_GUARDADO)

if (fs.existsSync(ARCHIVO_RUNTIME)) {
    try {
        console.log("Se encontro archivo runtime, procesando")
        fs.readFile(ARCHIVO_RUNTIME, function(err, data) {
            info_posts = JSON.parse(data);
        });
    } catch (error) {
        console.log(error)
    }
} else {
    console.log("no hay archivo runtime encontrado")
}