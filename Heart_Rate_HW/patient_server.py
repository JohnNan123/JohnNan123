import logging
import numpy as np
import ssl
from flask import Flask, request, jsonify
from datetime import datetime
from datetime import timedelta
import json
import requests

# Define variable to contain Flask class for server
app = Flask(__name__)

# Create list for database to contain patient data
db = []

# Add physiciandb
physiciandb = []

# logging config
logging.basicConfig(filename="hr_sential_server.log",
                    level=logging.INFO, filemode="w",)


# initial server with logging Config
def init_server():
    """ Initialize the server


    This function initializes the server log and can be used
    to run initial server star-up and connection to online database.


    """
    add_physician_to_db("Mario.C", "DrChen@my_hospital.com", "585-771-0016")


# check if the input id is in good foramte (int or str(int))
def check_int_formate(input):
    try:
        output = int(input)
    except ValueError:
        error_input = "Patient id should only contains numbers\n"
        print(error_input)
        raise ValueError
    return output


def find_patient_from_db(input, database):
    for patient in database:
        if patient["patient_id"] == input:
            return patient
    answer = "Patient_id {} was not found\n".format(input)
    print(answer)
    return 0


def find_patient_with_doc(input, database):
    doctors_patient = []
    for patient in database:
        if patient["attending_username"] == input:
            doctors_patient.append(patient)
    return doctors_patient


def get_time_as_string():
    time_now = datetime.now()
    str_time_now = datetime.strftime(time_now, "%m-%d-%y %H:%M:%S")
    return str_time_now


def check_status(age, heart_rate):
    rg = np.arange
    if age in rg(0, 3) and heart_rate > 151:
        x = 1
    elif age in rg(3, 5) and heart_rate > 137:
        x = 1
    elif age in rg(5, 8) and heart_rate > 133:
        x = 1
    elif age in rg(8, 12) and heart_rate > 130:
        x = 1
    elif age in rg(12, 16) and heart_rate > 119:
        x = 1
    elif age > 15 and heart_rate > 100:
        x = 1
    else:
        x = 0
    if x == 1:
        status = "tachycardic"
    else:
        status = "not tachycardic"
    return status


def load_patient(in_data):
    new_patient = {
        'patient_id': check_int_formate(in_data['patient_id']),
        'attending_username': in_data['attending_username'],
        'patient_age': check_int_formate(in_data['patient_age']),
        'heart_rate': [],
        'time_stamp': []
    }
    return new_patient


@app.route("/api/new_patient", methods=["POST"])
def new_patient_handler():
    in_data = request.get_json()
    new_patient = load_patient(in_data)
    if new_patient["patient_id"] == in_data['patient_id']:
        db.append(new_patient)
        logging.info("patient {} has been added to data\
                      base.\n".format(new_patient['patient_id']))
        answer = 'data load in successfully\n'
        return jsonify(answer), 200
    else:
        answer = 'patient fail to load into database'
        return jsonify(answer), 400


@app.route("/api/heart_rate", methods=["POST"])
def new_patient_heart_rate():
    in_data = request.get_json()
    input_id = check_int_formate(in_data['patient_id'])
    the_patient = find_patient_from_db(input_id, db)
    the_patient['heart_rate'].append(check_int_formate(in_data['heart_rate']))
    time_now = get_time_as_string()
    the_patient['time_stamp'].append(time_now)
    answer = 'add heart rate and time stamp to\
               patient {} successfully \n'.format(input_id)
    return jsonify(answer), 200


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def calc_average_heart_rate():
    in_data = request.get_json()
    input_id = check_int_formate(in_data['patient_id'])
    time_since_str = in_data['heart_rate_average_since']
    ds = datetime.strptime
    time_since_datetime = ds(time_since_str, "%m-%d-%y %H:%M:%S")
    the_patient = find_patient_from_db(input_id, db)
    # calculate the average heart rate since the given time
    for index, time_str in enumerate(the_patient['time_stamp']):
        time_datetime = datetime.strptime(time_str, "%m-%d-%y %H:%M:%S")
        if time_since_datetime <= time_datetime:
            average_hr = np.average(the_patient['heart_rate'][index:])
            str_ave_hr = str(int(average_hr))
            return jsonify(str_ave_hr), 200
    answer = 'there is no data with the datetime given\n'
    return jsonify(answer), 400


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    # find the patient and determine the status
    patient_id = check_int_formate(patient_id)
    the_patient = find_patient_from_db(patient_id, db)
    the_heart_rate = the_patient['heart_rate'][-1]
    the_age = the_patient['patient_age']
    status = check_status(the_age, the_heart_rate)
    if status == "tachycardic":
        send_email(the_patient)
    time_stamp = get_time_as_string()
    patient_status = {}
    patient_status['heart_rate'] = the_heart_rate
    patient_status['status'] = status
    patient_status['time_stamp'] = time_stamp
    # prepare output json file
    file_name = "{}_status.json".format(patient_id)
    js_file = open(file_name, 'w')
    json.dump(patient_status, js_file)
    js_file.close()
    answer = "patient {} status print successfully\n".format(patient_id)
    return jsonify(answer), 200


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rate_list(patient_id):
    patient_id = check_int_formate(patient_id)
    the_patient = find_patient_from_db(patient_id, db)
    heart_rate_record = the_patient['heart_rate']
    file_name = "{}_hr_record.json".format(patient_id)
    js_file = open(file_name, 'w')
    json.dump(heart_rate_record, js_file)
    js_file.close()
    answer = "patient {} heart rate\
              record print successfully\n".format(patient_id)
    return jsonify(answer), 200


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_average_heart_rate(patient_id):
    patient_id = check_int_formate(patient_id)
    the_patient = find_patient_from_db(patient_id, db)
    hr_list = the_patient['heart_rate']
    ave_hr = np.average(hr_list)
    file_name = "{}_hr_average.json".format(patient_id)
    js_file = open(file_name, 'w')
    json.dump(ave_hr, js_file)
    js_file.close()
    answer = "patient {} average heart\
              rate print successfully\n".format(patient_id)
    return jsonify(answer), 200


@app.route("/api/patients/<attending_username>", methods=["GET"])
def get_docs_all_patient(attending_username):
    patient_list = find_patient_with_doc(attending_username, db)
    patient_summary_list = []
    for patient in patient_list:
        print(patient['patient_age'])
        print(patient['heart_rate'][-1])
        p_age = patient['patient_age']
        p_hr = patient['heart_rate']
        status = check_status(p_age, p_hr[-1])
        summary = {}
        summary['patient_id'] = patient['patient_id']
        summary['last_heart_rate'] = patient['heart_rate'][-1]
        summary['last_time'] = patient['time_stamp'][-1]
        summary['status'] = status
        patient_summary_list.append(summary)

    file_name = "{}'s_patient.json".format(attending_username)
    js_file = open(file_name, 'w')
    json.dump(patient_summary_list, js_file)
    js_file.close()
    answer = "{}'s patient file \
              generate successfully\n".format(attending_username)
    return jsonify(answer), 200


def add_physician_to_db(attending_username, attending_email, attending_phone):
    """ Add physician information to physician database


    This function receives information about physician, creates
    a new dictionary containing the physician username,
    physician email, and physician's phone number in the
    string form and appends the diction to the physician database list.

    :param attending_username: a string of physician's username
    :param attending_email: a string of physician's email address
    :param attending_phone: a string of physician's phone number

    :returns True: a boolean value indicating that the physician's information
    was saved to the databse
    """
    new_physician = {
        "attending_username": attending_username,
        "attending_email": attending_email,
        "attending_phone": attending_phone}
    physiciandb.append(new_physician)
    logging.info("a new physician has been added to database.\n \
             attending username: {} \n\
             email: {} \n".format(new_physician['attending_username'],
                                  new_physician["attending_email"]))
    return True


@app.route("/api/new_attending", methods=["POST"])
def new_physician_handler():
    """Handles requests to the /api/new_attending route for
       adding new physician


    This /api/new_attending is a POST request that receive a
    JSON-encoded string with the following format:
    {
        "attending_username": attending_username,
        "attending_email": attending_email,
        "attending_phone": attending_phone
    }

    This function then calls function to receive an
    "answer" and "status code" and return them.

    :returns answer: a string about if information is
    add to database successfully
    :returns status_code: an integer about if
    information is add to database successfully
    """
    in_data = request.get_json()
    answer, status_code = new_physician_driver(in_data)
    return jsonify(answer), status_code


def new_physician_driver(in_data):
    """Implement/new_attending route for adding a
    new physician to databse


    This /api/new_attending is a POST request that
    receive a JSON-encoded string with the following format:
    {
        "attending_username": attending_username,
        "attending_email": attending_email,
        "attending_phone": attending_phone
    }

    This function then calls a validation function to
    ensure the needed keys and data types exist in the
    dictionary, which will add information to physician databse once
    confirmed and send a status code 0f 200.

    :param in_data: a json file received from POST request

    :returns answer: a string about if information is
    add to database successfully
    :returns status_code: an integer about if information
    is add to database successfully
    :returns True: a boolean value indicating that the
    physician's information was saved to the databse
    """
    expected_keys = ["attending_username",
                     "attending_email", "attending_phone"]
    expected_types = [str, str, str]
    answer, status_code = validate_server_input(
                          in_data, expected_keys, expected_types)
    if status_code != 200:
        return answer, status_code
    add_physician_to_db(in_data["attending_username"],
                        in_data["attending_email"], in_data["attending_phone"])
    print(physiciandb)
    return True, 200


def validate_server_input(in_data, expected_keys, expected_types):
    """Validate if the input is correct


    This function validate if the types and contents within
    in_data are the same as the expected types

    :param in_data: a json file received from POST request
    :param expected_keys: a list of needed keys in the
     input dictionary
    :param expected_types: a list of types for each
     value in the dictionary

    :returns error_message: a string about which
     parameter is missing/which type is incorrect
    :returns status_code: an integer about if information
     is add to database successfully
    :returns True: a boolean value indicating that
     the physician's information was saved to the databse
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


def find_physician_from_db(input):
    for physician in db:
        if physician["attending_username"] == input:
            return physician
    answer = "Patient_id {} was not found\n".format(input)
    print(answer)
    return 0


def email_request(to_email, the_patient):
    email_server = "http://vcm-7631.vm.duke.edu:5007/hrss/send_email"
    patient_id = the_patient["patient_id"]
    email_info = {
                  "from_email": "DrChen@my_hospital.com",
                  "to_email": "{}".format(to_email),
                  "subject": "Patient_report",
                  "content": "Patient {}\
                   is tachycardiac".format(patient_id)}
    e = requests.post(email_server, json=email_info)
    print(e.status_code)
    print(e.text)


def send_email(the_patient):
    attending_username = the_patient["attending_username"]
    the_physician = find_physician_from_db(attending_username)
    to_email = the_physician["attending_email"]
    email_request(to_email, the_patient)
    logging.info("A heart rate is posted that is tachycardic.\
    the patient id is {}, the patient heart rate is {},\
    the attending email is {}".format(the_patient["patient_id"],
                                      the_patient["heart_rate"][-1],
                                      to_email))


if __name__ == "__main__":
    app.run()
