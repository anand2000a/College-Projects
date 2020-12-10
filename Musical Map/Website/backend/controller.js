var model = require('./model.js');
module.exports = {
	usermap : function(req,res){
		//model.place(res)
		var filename =  "/home/snowman/Desktop/project/GROUP_F_PROJECT-13/backend/index.html"
		res.sendFile(filename,{dotfiles:'deny'},function(err){
			if(err)
				res.send('some error')
			else
				console.log('sent')
		})
	},
	
	blog : function(req,res){
		var filename  = "/home/snowman/Desktop/project/GROUP_F_PROJECT-13/backend/blog/" + req.query.lat + "_" + req.query.lon + ".html";
		res.sendFile(filename,{dotfiles: 'deny'},function(err){
			if(err)
				res.send("no such blog")
			else
				console.log("sent")
		})
	},

	admin : function(req,res){
		var filename =  "/home/snowman/Desktop/project/GROUP_F_PROJECT-13/backend/logIn.html"
		res.sendFile(filename,{dotfiles:'deny'},function(err){
			if(err)
				res.send('some error')
			else
				console.log('sent')
		})
	},

	adminlogin : function(req, res){
		if (req.body.username==undefined  || req.body.password==undefined) {
			var filename =  "/home/snowman/Desktop/project/GROUP_F_PROJECT-13/backend/logIn.html"
			res.sendFile(filename,{dotfiles:'deny'},function(err){
				if(err)
					res.send('some error')
				else
					console.log('sent')
			})
  		}
		else if(req.body.username === "amy" && req.body.password === "amyspassword") {
    			req.session.user = "amy";
    			req.session.admin = true;
			var filename =  "/home/snowman/Desktop/project/GROUP_F_PROJECT-13/backend/admin.html"
			res.sendFile(filename,{dotfiles:'deny'},function(err){
				if(err)
					res.send('some error')
				else
					console.log('sent')
			})
  		}
		else{
			res.send("wrong credentials");
		}
	},
	
	adminadd : function(req, res){
		insImage(req, res, function(err) {
        		if (err) {
             			return res.end("Something went wrong!");
         		}
         		return res.end("File uploaded sucessfully!.");
    	 	});
		locImage(req, res, function(err) {
         		if (err) {
            			return res.end("Something went wrong!");
        		}
        		return res.end("File uploaded sucessfully!.");
     		});
		res.send("add data") // return the file that will add the blog
	},

	blogadd : function(req,res){
		res.send('add blog')
		// image storer
	},

	adminedit : function(req, res){
		res.send("edit data")
	},

	admindelete : function(req, res){
		model.deleteplace(req,res);
	},
	
	adminlogout : function(req,res){
		req.session.admin=false;
		console.log(req.session)
		res.send("logout success")
	}
}
