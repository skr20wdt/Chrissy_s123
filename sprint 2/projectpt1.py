import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
import random

app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True

#shows diners and their status
#i am using this to show each diner status in the random select page so users can see if they would like to change their status
@app.route('/api/showdiners', methods = ['GET'])
def showdiners():
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    #diner information
    query = "SELECT * FROM diners"
    diners = execute_read_query(conn,query)
    return jsonify(diners)

@app.route('/api/adduser', methods = ['POST'])
def adduser():
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    request_data = request.get_json()
    #diner information
    newfirstname = request_data['firstname']
    newlastname = request_data['lastname']
    newstatus = request_data['status']
    query = "INSERT INTO diners (firstname, lastname, status) VALUES ('%s','%s','%s')" % (newfirstname,newlastname,newstatus)
    execute_query(conn,query)
    return 'Diner added'


#add restaurant using first and last name as tokens
@app.route('/api/addrestaurants/<firstname>/<lastname>', methods = ['POST'])
def add_restaurants(firstname,lastname):
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    #counts how many entries
    name_query = "SELECT * FROM restaurant"
    select_name = execute_read_query(conn,name_query)
    #checks to see if there are any prior entries
    #allows entries if less than 10
    for names in select_name:
        if firstname == names['firstname'] and lastname == names['lastname']:
            restaurant_clause = "SELECT * FROM restaurant WHERE firstname = '%s' AND lastname = '%s'" % (firstname, lastname)
            restaurant_query = execute_read_query(conn, restaurant_clause)
            if len(restaurant_query)<11:
                request_data = request.get_json()
                restaurantname = request_data['restaurantname']
                query = "INSERT INTO restaurant (firstname, lastname,restaurantname) VALUES ('%s','%s','%s')" % (firstname,lastname,restaurantname)
                execute_query(conn, query)
            if len(restaurant_query) == 9:
                #warning
                return "Last entry successful. You've reached the max."
                #checks entries after new input
            count = 4 - len(restaurant_query)
            if count < 5 and count > 0:
                #warning if not enough entries
                amount = len(restaurant_query) + 1
                count_statement = "Entry added. You have %s restaurants.Enter %s more to meet minimum." % (amount,count)
                return count_statement
            elif len(restaurant_query) >= 10:
            #warning that 10 entries is max
                return "Entry unsucceful. You have 10 entries already."
            else:
                count = len(restaurant_query) + 1
                #statement if requirements met
                count_statement = "%s entries to choose from" % (count)
                return count_statement
    request_data = request.get_json()
    restaurantname = request_data['restaurantname']
    query = "INSERT INTO restaurant (firstname, lastname,restaurantname) VALUES ('%s','%s','%s')" % (firstname,lastname,restaurantname)
    execute_query(conn, query)
    return "First entry added"
    

#edit users information
#not sure why i got points off, I made no changes to this function and it works fine
@app.route('/api/edit/diner', methods = ['POST'])
def edit_diners():
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    request_data = request.get_json()
    #asking for original info
    orig_first_name = request_data['firstname']
    orig_last_name = request_data['lastname']
    #enter new info
    newfirst = request_data['newfirst']
    newlast = request_data['newlast']
    #update statement
    update_query = """UPDATE diners SET firstname = '%s', lastname = '%s' WHERE firstname = '%s' and lastname = '%s'""" % (newfirst,newlast,orig_first_name,orig_last_name)
    execute_query(conn, update_query)
    update_rest = """UPDATE restaurant SET firstname = '%s', lastname = '%s' WHERE firstname = '%s' and lastname = '%s'""" % (newfirst,newlast,orig_first_name,orig_last_name,)
    execute_query(conn,update_rest)
    return "Update successful."

#function for diners to change if they wanna be considered for the pick
#using this criteria for random pick later on
#this determines if theyre gonna be in the final list of the selection
@app.route('/api/edit/diner/status', methods = ['POST'])
def status_update():
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    request_data = request.get_json()
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    #status change
    status = request_data['status']
    update_query = """UPDATE diners SET status = '%s' WHERE firstname = '%s' and lastname = '%s'""" % (status, firstname,lastname)
    execute_query(conn,update_query)
    return 'status changed'


@app.route('/api/edit/restaurants/<firstname>/<lastname>', methods = ['POST'])
#using first and last name for where clause
def edit_restaurants(firstname,lastname):
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    request_data = request.get_json()
    #asking for set and where clause
    orig_restaurant = request_data['restaurantname']
    new_restaurant = request_data['newrestaurant']
    update_query = """UPDATE restaurant SET restaurantname = '%s' WHERE firstname = '%s' and lastname = '%s' and restaurantname = '%s'""" % (new_restaurant,firstname,lastname,orig_restaurant)
    execute_query(conn,update_query)
    return 'Update successful'

@app.route('/api/delete/diners', methods = ['POST'])
def delete_diner():
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    request_data = request.get_json()
    #asking for set and where clause
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    #deleting user and all restaurants with that user
    delete_query = "DELETE FROM diners WHERE firstname = '%s' and lastname = '%s' " % (firstname,lastname)
    execute_query(conn,delete_query)
    delete_rest = "DELETE FROM restaurant WHERE firstname = '%s' and lastname = '%s' " % (firstname,lastname)
    return 'successful'

@app.route('/api/delete/restaurants/<firstname>/<lastname>', methods = ['POST'])
def delete_restaurant(firstname,lastname):
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    #asking for set and where clause
    request_data = request.get_json()
    restaurantname = request_data['restaurantname']
    #deleting that restaurant
    delete_query = "DELETE FROM restaurant WHERE firstname = '%s' and lastname = '%s' and restaurantname = '%s'" % (firstname,lastname,restaurantname)
    execute_query(conn,delete_query)
    return "successful"

#random select based on users status
#i did take into account which users are going, that's why i had the status variable with each user
#no changes made
@app.route('/api/randomselect',methods=['GET'])
def random_select():
    conn = create_connection("cis3368fa21.cjnvtg4r4aqh.us-east-2.rds.amazonaws.com", "admin","cis3368kani","CIS3368fall21")
    query = "SELECT * FROM diners WHERE status = 'yes'"
    yes_diners = execute_read_query(conn,query)
    #select first 10 of each user
    #put in list
    results = []
    for diners in yes_diners:
        diner_query = "SELECT * FROM restaurant WHERE firstname = '%s' and lastname = '%s' LIMIT 10" % (diners['firstname'],diners['lastname'])
        diner_list = execute_read_query(conn,diner_query)
        #adding restaurants to list that meet yes criteria based on first and last name
        for restaurant in diner_list:
            results.append(restaurant)
    limit = len(results)
    #using random function, selection based on index
    num_gen = random.randint(0,limit - 1)
    chosen = results[num_gen]
    #jsonify random chosen index
    return jsonify(chosen)




app.run()