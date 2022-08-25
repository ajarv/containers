var Minio = require('minio');
var morgan = require('morgan')

var client = new Minio.Client({
    endPoint: process.env.MINIO_HOST,
    port: parseInt(process.env.MINIO_PORT),
    useSSL: false,
    accessKey: process.env.MINIO_ACCESS_KEY ,
    secretKey: process.env.MINIO_SECRET_KEY,
})
// express is a small HTTP server wrapper, but this works with any HTTP server
const server = require('express')()
server.use(morgan('combined'))

server.get('/presignedUrl', (req, res) => {
    client.presignedPutObject('images', req.query.name, (err, url) => {
        if (err) throw err
        res.end(url)
    })
})

server.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
})

const port = 8080
server.listen(port,'0.0.0.0', () => {
    console.log(`Example app listening at http://localhost:${port}`)
  })