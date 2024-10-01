const express = require('express');
const dotenv = require('dotenv');
const bodyParser = require("body-parser")
const fs = require("fs")
dotenv.config();

const app = express();
const port = process.env.service_port_api;

app.use(bodyParser.json({ limit: '10mb' }));

let info_posts = {}
let cola_process = {'process_1':[], 'process_2':[]}
let diccio_process = {'process_1':{}, 'process_2':{}}
let diccio_comments = {}

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
    cola_process['process_1'].push(info_posts[ID])
    diccio_process['process_1'][ID] = info_posts[ID]

    console.log(ID, " Agregado")
    res.send('Petición POST procesada con éxito!');
})

app.get('/get_process_1', (req, res) => {
    console.log('/get_process_1')//, req.body);

    let item = cola_process['process_1'].pop()
    diccio_process['process_1'][item.id] = item
    let data = (item) ? item : ''
    return res.status(200).send({ "item": data });
});

app.post('/post_process_1_msg', (req, res) => {
    console.log('/post_process_1_msg')//, req.body);
    const ID_POST = req.body.id_post
    const MSG_ARR = req.body.data

    let post = info_posts[ID_POST]
    try {
        if (!post.data?.comentarios)
            post.data['comentarios'] = {}
        
        //console.log('pd', post)
        
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
    delete diccio_process['process_1'][ID_POST]
    
    return res.status(200).send({ "stat": true });
});

app.get('/get_process_2', (req, res) => {
    console.log('/get_process_2')//, req.body);

    let item = cola_process['process_2'].pop()
    console.log(item)
    diccio_process['process_2'][item.id] = item
    let data = (item) ? item : ''
    return res.status(200).send({ "item": data });
});

app.post('/post_process_2_msg', (req, res) => {
    console.log('/post_process_2_msg')//, req.body);

    const MSG_    = req.body
    console.log(MSG_)
    const ID_POST = req.body.id_post

    let post = info_posts[ID_POST]
    try {
        if (!post.data?.comentarios)
            post.data['comentarios'] = {}
        
        const COMMENT = MSG_
        diccio_comments[COMMENT.data.thingid] = COMMENT
        if (COMMENT.data.parentid != null)
            diccio_comments[COMMENT.data.parentid].respuestas.push(COMMENT)
        else
            post.data.comentarios[COMMENT.data.thingid] = diccio_comments[COMMENT.data.thingid]
        
        
    } catch (error) {
        console.log(error)
        return res.status(200).send({ "stat": false });
    }
    
    post['process_2'] = true
    delete diccio_process['process_2'][ID_POST]
    
    return res.status(200).send({ "stat": true });
});


app.listen(port, () => {
    console.log(`Servidor escuchando en puerto ${port}`);
});

const HOY = new Date()
const fecha = '2024830'
//const fecha = String(HOY.getFullYear())+String(HOY.getMonth())+String(HOY.getDate())
const ARCHIVO_RUNTIME = "./resultados/runtime"+fecha+".json"
const ARCHIVO_DICCIO = "./resultados/runtime"+fecha+"_diccio.json"
setInterval(async () => {
    try {
        fs.writeFile(ARCHIVO_RUNTIME, JSON.stringify(info_posts), err => {
            console.log("Done writing"); // Success
        })
    } catch (error) {
        console.log("error al guardar archivo", error)
    } 
    
    try {
        fs.writeFile(ARCHIVO_DICCIO, JSON.stringify(diccio_comments), err => {
            console.log("Done writing"); // Success
        })
    } catch (error) {
        console.log("error al guardar archivo", error)
    }
}, process.env.INTERVALO_GUARDADO)

const PROCESOS = ['process_1', 'process_2']

if (fs.existsSync(ARCHIVO_RUNTIME)) {
    try {
        console.log("Se encontro archivo runtime, procesando")
        fs.readFile(ARCHIVO_RUNTIME, function(err, data) {
            info_posts = JSON.parse(data);

            let keys_ = Object.keys(info_posts)
            for (let i=0; i < keys_.length; i++){
                for (let j=0; j < PROCESOS.length; j++){

                    if (info_posts[keys_[i]][PROCESOS[j]] === undefined)
                        info_posts[keys_[i]][PROCESOS[j]] = false
    
                    if (info_posts[keys_[i]][PROCESOS[j]] == false) {
                        cola_process[PROCESOS[j]].push(info_posts[keys_[i]])
                        diccio_process[PROCESOS[j]][keys_[i]] = info_posts[keys_[i]]
                        console.log(keys_[i], ' agregado a lista ',PROCESOS[j])
                    }

                }
                
            }
        });
    } catch (error) {
        console.log(error)
    }
} else {
    console.log("no hay archivo runtime encontrado")
}

if (fs.existsSync(ARCHIVO_DICCIO)) {
    try {
        console.log("Se encontro archivo diccionario")
        fs.readFile(ARCHIVO_DICCIO, function(err, data) {
            diccio_comments = JSON.parse(data);
        });
    } catch (error) {
        console.log(error)
    }
} else {
    console.log("no hay archivo runtime encontrado")
}