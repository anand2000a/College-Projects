var mysql = require('mysql')
var fs = require('fs');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'map',
  password : 'musicmaps',
  database : 'data'
});
connection.connect()


module.exports = {
	place : function(res) {
		var place_data;
		connection.query('SELECT * FROM location', function (err, rows, fields) {
			place_data = rows;		  	
			res.send(place_data);
		});
	},
	deleteplace : function(req,res){
		if(req.query.lat!=undefined || req.query.lon!=undefined)
		connection.query('DELETE FROM location WHERE latitude LIKE $req.query.lat AND longitude LIKE $req.query.lon', function (err){
			if(err) throw err;
			res.send('done')
			//fs.unlink('/blog/$req.query.lat_$req.query.lon',function(err))
		});
		else
			res.send('enter lon and lat to delete')
	}
}



