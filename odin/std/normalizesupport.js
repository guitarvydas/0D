_ = {
    encodews : function (s) { return _.encodequotes (encodeURIComponent (s)); },
    encodequotes : function (s) { 
	rs= s.replace (/"/g, '%22').replace (/'/g, '%27');
	return rs;
    }
},

