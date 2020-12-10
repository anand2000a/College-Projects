var http = require('http');
var url = require('url');
var fs = require('fs');
var mysql=require("mysql");
const PATH = require('path');
var express = require('express');
var app = express();
var fileToLoad;

var publicDir=require('path').join(__dirname,'/public');
app.use(express.static(publicDir));


app.use(express.static(__dirname+'public'));
var server=app.listen(5000);

var con=mysql.createConnection({
	host:'localhost',
	user:'root',
	password:'1MySql_!',
	database:'mydb'
});

con.connect(function(err){
	if(err) throw err;
	console.log("Connected...!!");
});

http.createServer(function (req, res) {
	var q = url.parse(req.url);
	var d = url.parse(req.url,true).query;
	var file="."+q.pathname;
	var isImage=0,contentType;
	var dirs=q.pathname.split('/');
	var extension=q.pathname.split(',').pop();

	if(q.pathname=="/") {
		file="index.html";
		contentType="text/html";
		isImage=2;
	}
	else if(dirs[1]!="admin" && q.pathname!="backend.js") {
		switch(extension) {
			case "jpg":
				contentType="image/jpg";
				isImage=1;
				break;
			case "jpg":
				contentType="image/jpg";
				isImage=1;
				break;
			case "js":
				contentType="text/javascript";
				isImage=2;
				break;
			case "html":
				contentType="text/html";
				isImage=2;
				break;
			case "css":
				contentType="text/css";
				isImage=2;
				break;	
			default :
				contentType="text/html";
				isImage=2;
				break;		
		}
	}
	else if(q.pathname=='/admin'){
			if(q.query==null) {
				fs.readFile('add.html', function(err, data) {
					if(err) throw err;
					res.writeHead(200, {'Content-Type': 'text/html'});
					res.write(data);
					res.end();
				});
			}
			else if(q.query!=null) {
				var sql="INSERT INTO markers (name,lat,lng) VALUES ('"+d.place+"','"+d.lat+"','"+d.lng+"')";
				con.query(sql,function(err, result) {
					if(err) throw err;
					console.log("Rows affected : "+result.affectedRows);
				});

				con.query("SELECT * FROM markers",function(err, result){
					console.log(result);
					var mark=JSON.stringify(result);

					fs.writeFile('markers.js',"var data="+mark+";",function(err){
						if(err) throw err;
					})
				});

				res.writeHead(302, {'Location':'http://'+req.headers['host']+'/admin'});
				return res.end();
			}
	}

	if(isImage==1) {
		fileToLoad=fs.readFileSync(file);
		res.writeHead(200,{'Content-Type':contentType});
		res.end(fileToLoad,'binary');
	}
	else if(isImage==2) {
		    fs.readFile(file, function(err,data) {
				if(err) throw err;

				res.writeHead(200, {'Content-Type':  contentType });
				res.write(data);
				res.end();
			});
	}

}).listen(8080);