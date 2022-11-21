import requests


server = "http://127.0.0.1:5000"


new_physician = {"attending_username": "Mario.C", "attending_email": "DrChen@my_hospital.com", "attending_phone": "585-771-0017"}
r = requests.post(server + "/api/new_attending", json = new_physician)
print(r.status_code)
print(r.text)


new_patient = {"patient_id":"2233", "attending_username":"Mario.C", "patient_age":23}
r = requests.post(server + "/api/new_patient", json = new_patient)
print(r.status_code)
print(r.text)


new_heartrate1 = {"patient_id":2233, "heart_rate": 99}
new_heartrate2 = {"patient_id":2233, "heart_rate": 98}
x = requests.post(server + "/api/heart_rate", json = new_heartrate1)
y = requests.post(server + "/api/heart_rate", json = new_heartrate2)
print(x.status_code)
print(x.text)
print(y.status_code)
print(y.text)


patient_id = 2233
heart_status = requests.get(server + "/api/status/{}".format(patient_id))
print(heart_status)
print(heart_status.status_code)
print(heart_status.text)


patient_id = 2233
all_heartrate = requests.get(server + "/api/heart_rate/{}".format(patient_id))
print(all_heartrate)
print(all_heartrate.status_code)
print(all_heartrate.text)


patient_id = 2233
average_heartrate = requests.get(server + "/api/heart_rate/average/{}".format(patient_id))
print(average_heartrate)
print(average_heartrate.status_code)
print(average_heartrate.text)


patient_time_stamp = {"patient_id":2233, "heart_rate_average_since": "03-21-22 16:36:30"}
b = requests.post(server + "/api/heart_rate/interval_average", json = patient_time_stamp)
print(b)
print(b.status_code)
print(b.text)


attending_username = "Mario.C"
c = requests.get(server + "/api/patients/{}".format(attending_username))
print(c)
print(c.status_code)
print(c.text)
