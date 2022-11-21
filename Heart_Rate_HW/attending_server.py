import logging
from flask import Flask, request, jsonify
import json


app = Flask(__name__)


physiciandb = []


def init_server():
    """ Initialize the server


    This function initializes the server log and can be used 
    to run initial server star-up and connection to online database.


    """
    add_physician_to_db("Mario.C", "DrChen@my_hospital.com", "585-771-0016")
    logging.basicConfig(filename="physician_server.log", level=logging.DEBUG, filemode='w')


def add_physician_to_db(attending_username, attending_email, attending_phone):
    """ Add physician information to physician database


    This function receives information about physician, creates a new dictionary
    containing the physician username, physician email, and physician's phone number
    in the string form and appends the diction to the physician database list.

    :param attending_username: a string of physician's username
    :param attending_email: a string of physician's email address
    :param attending_phone: a string of physician's phone number

    :returns True: a boolean value indicating that the physician's information
    was saved to the databse 
    """
    new_physician = {
        "attending_username": attending_username,
        "attending_email": attending_email,
        "attending_phone": attending_phone
    } 
    physiciandb.append(new_physician)
    return True


@app.route("/api/new_attending", methods = ["POST"])
def new_physician_handler():
    """Handles requests to the /api/new_attending route for adding new physician


    This /api/new_attending is a POST request that receive a JSON-encoded string
    with the following format:
    {
        "attending_username": attending_username,
        "attending_email": attending_email,
        "attending_phone": attending_phone
    } 

    This function then calls function to receive an "answer" and "status code"
    and return them.
 
    :returns answer: a string about if information is add to database successfully
    :returns status_code: an integer about if information is add to database successfully
    """
    in_data = request.get_json()
    answer, status_code = new_physician_driver(in_data)
    return jsonify(answer), status_code


def new_physician_driver(in_data):
    """Implement/new_attending route for adding a new physician to databse


    This /api/new_attending is a POST request that receive a JSON-encoded string
    with the following format:
    {
        "attending_username": attending_username,
        "attending_email": attending_email,
        "attending_phone": attending_phone
    } 

    This function then calls a validation function to ensure the needed keys and data 
    types exist in the dictionary, which will add information to physician databse once
    confirmed and send a status code 0f 200. 

    :param in_data: a json file received from POST request
    
    :returns answer: a string about if information is add to database successfully
    :returns status_code: an integer about if information is add to database successfully
    :returns True: a boolean value indicating that the physician's information
    was saved to the databse
    """
    expected_keys = ["attending_username", "attending_email", "attending_phone"]
    expected_types = [str, str, str]
    answer, status_code = validate_server_input(in_data, expected_keys, expected_types)
    if status_code != 200:
        return answer, status_code
    add_physician_to_db(in_data["attending_username"], in_data["attending_email"], in_data["attending_phone"])
    print(physiciandb)
    return True, 200


def validate_server_input(in_data, expected_keys, expected_types):
    """Validate if the input is correct


    This function validate if the types and contents within in_data are the same
    as the expected types

    :param in_data: a json file received from POST request
    :param expected_keys: a list of needed keys in the input dictionary
    :param expected_types: a list of types for each value in the dictionary
    
    :returns error_message: a string about which parameter is missing/which type is incorrect
    :returns status_code: an integer about if information is add to database successfully
    :returns True: a boolean value indicating that the physician's information
    was saved to the databse
    """
    if type(in_data) is not dict:
        return "The input was not a dictionary.", 400
    for key, expected_types in zip(expected_keys, expected_types):
        if key not in in_data:
            error_message = "Key {} is missing".format(key)
            return error_message, 400
        if type(in_data[key]) is not expected_types:
            error_message = "Value of key {} is not of type {}"\
                .format(key, expected_types)
            return error_message, 400
    return True, 200


if __name__ == "__main__":
    init_server()
    app.run()
    print(physiciandb)
