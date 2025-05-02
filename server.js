const express = require('express');
const dotenv = require('dotenv');
const bodyParser = require("body-parser")
const fs = require("fs")
const mongoose = require('mongoose')
dotenv.config();

const app = express();
const port = process.env.service_port_api;

app.use(bodyParser.json({ limit: '10mb' }));

let info_posts = {}

const mongoURI = `mongodb://${process.env.MONGO_USER}:${process.env.MONGO_PASSWORD}@${process.env.MONGO_HOST}:${process.env.MONGO_PORT}`;
mongoose.connect(mongoURI);
const db = mongoose.connection;

db.on('error', console.error.bind(console, 'Error de conexión a MongoDB:', mongoURI));
db.once('open', function () {
    console.log('Conectado a MongoDB');
});

const postSchema = new mongoose.Schema({
    id: String,
    html: String, 
    data: Object, 
    process_1: Boolean,
    process_2: Boolean,
});
const Post = mongoose.model('Post', postSchema);

app.post('/post_html', async (req, res) => {
    console.log('/post_html')//, req.body);
    const ID = req.body.id

    const existingPost = await Post.findOne({ id: ID });
    if (existingPost) {
        console.log("Ya hay un elemento con ese ID", ID)
        res.send('Ya hay un elemento con ese ID');
        return
    }

    console.log(ID, " Agregado")
    const post = new Post({ id: ID, ...req.body, process_1: false, process_2: false })
    try {
        const savedPost = await post.save();
        console.log(ID, " Agregado")
        return res.send('Petición POST procesada con éxito!');
    } catch (err) {
        console.error(err);
        return res.send('Error al guardar el post', err);
    }
})

app.get('/get_process_1', async (req, res) => {
    console.log('/get_process_1')//, req.body);

    const item = await Post.findOne({ process_1: false });
    return res.status(200).send({ "item": item });
})

app.post('/post_process_1_msg', async (req, res) => {
    console.log('/post_process_1_msg')//, req.body);
    const ID_POST = req.body.id_post
    const MSG_ARR = req.body.data

    try {
        const post = await Post.findOne({ id: ID_POST });
        if (!post) {
            return res.status(404).send({ "message": "No se encontró el post" });
        }
        
        let diccio_comments = post?.data?.comentarios ? post.data.comentarios : {}

        for (let i = 0; i < MSG_ARR.length; i++) {
            const COMMENT = MSG_ARR[i]
            diccio_comments[COMMENT.data.thingid] = COMMENT
        }

        post.set({ 'data.comentarios': diccio_comments });
        post['process_1'] = true

        await post.save();

        return res.status(200).send({ "stat": true });
    } catch (error) {
        console.log(error)
        return res.status(200).send({ "stat": false });
    }
});

app.get('/get_process_2', async (req, res) => {
    console.log('/get_process_2')//, req.body);

    const item = await Post.findOne({ $or: [{ process_2: false }, { process_2: null }] })
    if (item) {
        return res.status(200).send({ "item": item });
    } else {
        return res.status(404).send({ "message": "No se encontró un post con process_2 igual a false o no definido" });
    }
})

app.get('/get_results', (req, res) => {
    console.log('/get_results')//, req.body);

    return res.status(200).send({ "data": info_posts });
});

app.post('/post_process_2_msg', async (req, res) => {
    console.log('/post_process_2_msg')//, req.body);

    const MSG_ = req.body
    console.log(MSG_)
    const ID_POST = req.body.id_post

    const post = await Post.findOne({ id: ID_POST });
    if (!post) {
        return res.status(404).send({ "message": "No se encontró el post" });
    }

    try {
        let diccio_comments = post?.data?.comentarios ? post.data.comentarios : {}

        const COMMENT = MSG_
        diccio_comments[COMMENT.data.thingid] = COMMENT

        post.set({ 'data.comentarios': diccio_comments })
        post['process_2'] = true

        await post.save();

        return res.status(200).send({ "stat": true });

    } catch (error) {
        console.log(error)
        return res.status(200).send({ "stat": false });
    }

});

app.listen(port, () => {
    console.log(`Servidor escuchando en puerto ${port}`);
});