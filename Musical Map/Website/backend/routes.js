const express = require('express')
const controller = require("./controller.js") // contain functions
const multer = require('multer');
const bodyParser = require('body-parser')
const app = express()
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const session = require('express-session')
const port = 3001

const Storage = multer.diskStorage({
     destination: function(req, file, callback) {
         callback(null, "./Images");
     },
     filename: function(req, file, callback) {
         callback(null, file.fieldname + "_" + req.body.lat + "_" + req.body.lon + '.jpg');
     }
});

var locImage = multer({
     storage: Storage
}).array("locImage", 1);

var insImage = multer({
	storage:Storage
}).array("insImage",1);


app.use(session({
	secret  : '2C44-4D44-WppQ786',
	resave : true,
	saveUninitialized : true
}));
var auth = function(req,res,next){
	if (req.session && req.session.user === 'amy' && req.session.admin){
		console.log(req.session)
		return next()
	}
	else
		res.sendStatus(401);
} 

app.get('/', function(req,res){
	controller.usermap(req,res); // render map to client side
})
 
app.get('/blog/', function(req,res){
	controller.blog(req,res); // return the blog	
})

///////  admin routing starts now //////
app.get('/admin/', function(req, res){
	controller.admin(req,res);	// login page
});

app.post('/admin/login/',function(req,res){
	controller.adminlogin(req,res) //admin authentication
});

app.post('/admin/add/',auth ,function(req, res){
	controller.adminadd(req,res); // add data
});

app.get('/admin/add/blog',auth ,function(req,res){
	controller.blogadd(req,res); // blog maker	
});

app.get('/admin/edit/',auth ,function(req,res){
	controller.adminedit(req,res); //edit data
});

app.get('/admin/delete/',auth ,function(req,res){
	controller.admindelete(req,res); //delete data
});

app.get('/admin/logout/',auth ,function(req,res){
	controller.adminlogout(req,res); //logout data
});

app.listen(port, () => console.log(`The app is listening on port ${port}!`))
