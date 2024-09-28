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
    info_posts[ID]['process_1'] = false
    cola_process_1_pend.push(info_posts[ID])
    diccio_process_1_pend[ID] = info_posts[ID]

    console.log(ID, " Agregado")
    res.send('Petición POST procesada con éxito!');
})

app.get('/get_process_1', (req, res) => {
    console.log('/get_process_1')//, req.body);

    let item = cola_process_1_pend.pop()
    diccio_process_1_pend[item.id] = item
    let data = (item) ? item : ''
    return res.status(200).send({ "item": data });
});

function asignar_comentario(post_comments, comment, lvl = 0){
    if (comment.data['parentid'] == null){
        post_comments[comment.data['thingid']] = comment
        return
    } else 
    if (comment.data.depth < lvl)
        asignar_comentario()
}

app.post('/post_process_1_msg', (req, res) => {
    console.log('/post_process_1_msg')//, req.body);
    const ID_POST = req.body.id_post
    const MSG_ARR = req.body.data

    let post = info_posts[ID_POST]
    try {
        if (!post.data?.comentarios)
            post.data['comentarios'] = {}
        
        //console.log('pd', post)
        let diccio_comments = {}
        for (let i=0; i < MSG_ARR.length; i++){
            const COMMENT = MSG_ARR[i]
            diccio_comments[COMMENT.data.thingid] = COMMENT
            if (COMMENT.data.parentid != null)
                diccio_comments[COMMENT.data.parentid].respuestas.push(COMMENT)
            else
                post.data.comentarios[COMMENT.data.thingid] = diccio_comments[COMMENT.data.thingid]
        }
        
    } catch (error) {
        console.log(error)
        return res.status(200).send({ "stat": false });
    }
    
    post['process_1'] = true
    delete diccio_process_1_pend[ID_POST]
    
    return res.status(200).send({ "stat": true });
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

            let keys_ = Object.keys(info_posts)
            for (let i=0; i < keys_.length; i++){

                if (info_posts[keys_[i]]['process_1'] === undefined)
                    info_posts[keys_[i]]['process_1'] = false

                if (info_posts[keys_[i]]['process_1'] == false) {
                    cola_process_1_pend.push(info_posts[keys_[i]])
                    diccio_process_1_pend[keys_[i]] = info_posts[keys_[i]]
                    console.log(keys_[i], ' agregado a lista proceso 1')
                }
            }
        });
    } catch (error) {
        console.log(error)
    }
} else {
    console.log("no hay archivo runtime encontrado")
}