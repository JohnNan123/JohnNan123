import requests

server = "http://127.0.0.1:5000"


new_physician = {"attending_username": "Mario.C", "attending_email": "DrChen@my_hospital.com", "attending_phone": "585-771-0017"}
r = requests.post(server + "/api/new_attending", json = new_physician)
print(r.status_code)
print(r.text)


email_server = "http://vcm-7631.vm.duke.edu:5007/hrss/send_email"

patient_id = 2233,
email_info = {
    "from_email": "DrChen@my_hospital.com",
    "to_email": "DrNan@my_hospital.com",
    "subject": "Patient_report",
    "content": "Patient {} is tachycardiac".format(patient_id)
}
e = requests.post(email_server, json = email_info)
print(e.status_code)
print(e.text)