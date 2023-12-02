//load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');

var selectedID = "";
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

// set the view engine to ejs
// creating all the pages I need
app.set('view engine', 'ejs');

app.get('/', function(req, res) {
    res.render('pages/home');
});
app.get('/newuser', function(req, res) {
    res.render('pages/newuser');
});
app.get('/newrestaurant', function(req, res) {
    res.render('pages/newrestaurant');
});

app.get('/editdiner', function(req, res) {
    res.render('pages/editdiner');
});

app.get('/editrestaurant', function(req, res) {
    res.render('pages/editrestaurant');
});

app.get('/deletediners', function(req, res) {
    res.render('pages/deletediners');
});


//creating all functions I need

//function for adding a new diner using post
app.post('/adduser', function(req, res){
    var newfirstname = req.body.newfirstname;
    var newlastname = req.body.newlastname;
    var status = req.body.status;
    axios.post('http://127.0.0.1:5000/api/adduser', {
        firstname: newfirstname,
        lastname: newlastname,
        status: status
    }).then(response => {
        var tagline = response.data;
        res.render('pages/thanks.ejs',{
            tagline: tagline 
        });
        
    });
    
})

//function for adding a new restaurant
//using post
app.post('/addrestaurant', function(req, res){
    var firstname = req.body.firstname;
    var lastname = req.body.lastname;
    var restaurantname = req.body.restaurantname;
    axios.post(`http://127.0.0.1:5000/api/addrestaurants/${firstname}/${lastname}`, {
        restaurantname : restaurantname
    }).then(response => {
        var tagline = response.data;
        res.render('pages/thanks.ejs',{
            tagline: tagline 
        });
        
    });
    
})

//function for editing diner info
//using post
app.post('/editdiner', function(req, res){
    var orig_first_name = req.body.orig_first_name;
    var orig_last_name = req.body.orig_last_name;
    var newfirst = req.body.newfirst;
    var newlast = req.body.newlast;
    axios.post(`http://127.0.0.1:5000/api/edit/diner`, {
        firstname : orig_first_name,
        lastname: orig_last_name,
        newfirst: newfirst,
        newlast: newlast
    }).then(response => {
        var tagline = response.data;
        res.render('pages/thanks.ejs',{
            tagline: tagline 
        });
        
    });
    
})
//function for editing a restaurant
//using post
app.post('/editrestaurant', function(req, res){
    var firstname = req.body.firstname;
    var lastname = req.body.lastname;
    var orig_restaurant = req.body.orig_restaurant;
    var new_restaurant = req.body.new_restaurant;
    axios.post(`http://127.0.0.1:5000/api/edit/restaurants/${firstname}/${lastname}`, {
        restaurantname : orig_restaurant,
        newrestaurant : new_restaurant
    }).then(response => {
        var tagline = response.data;
        res.render('pages/thanks.ejs',{
            tagline: tagline 
        });
        
    });
    
})
//function for deleting diners
//using post
app.post('/deletediners', function(req, res){
    var firstname = req.body.firstname;
    var lastname = req.body.lastname;
    axios.post(`http://127.0.0.1:5000/api/delete/diners`, {
        firstname: firstname,
        lastname: lastname
    }).then(response => {
        var tagline = response.data;
        res.render('pages/thanks.ejs',{
            tagline: tagline 
        });
        
    });
    
})

//function for changing diner status
//using post
app.post('/changestatus', function(req, res){
    var firstname = req.body.firstname;
    var lastname = req.body.lastname;
    var status = req.body.status;
    axios.post(`http://127.0.0.1:5000/api/edit/diner/status`, {
        firstname: firstname,
        lastname: lastname,
        status: status
    }).then(response => {
        var tagline = response.data;
        res.render('pages/thanks.ejs',{
            tagline: tagline 
        });
        
    });
    
})
//showing all of the diners and their status so user can see who is going and who needs to change their status
app.get('/randomselect', function(req, res){
    axios.get(`http://127.0.0.1:5000/api/showdiners`)
    .then(response => {
        var diners = response.data;
        res.render('pages/randomselect',{
            diners: diners
        });
        
    });
    
});

//activates the random selection, renders to a different page
app.post('/selection', function(req, res){
    axios.get(`http://127.0.0.1:5000/api/randomselect`)
    .then(response => {
        var chosen = response.data;
        res.render('pages/chosen.ejs',{
            chosen: chosen
        });
        
    });
    
})

app.listen(8080);
console.log('8080 is the magic port');``