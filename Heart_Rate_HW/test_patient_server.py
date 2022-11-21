import pytest
from flask import jsonify
from datetime import datetime


db = [{'patient_id': 12345,
       'attending_username': "Junyu.N",
       'heart_rate': [99, 98, 100, 101],
       'patient_age': 23},
      {'patient_id': 23456,
       'attending_username': "Mario.C",
       'heart_rate': [150, 151, 152, 154],
       'patient_age': 50},
      {'patient_id': 34567,
       'attending_username': "Mario.C",
       'heart_rate': [123, 123, 125, 125],
       'patient_age': 10}]


@pytest.mark.parametrize("input, expected", [
    (123, 123),
    ("123", 123),
    ])
def test_check_int_formate(input, expected):
    from patient_server import check_int_formate
    answer = check_int_formate(input)
    assert answer == expected


@pytest.mark.parametrize("input", [
    ("45a"),
    ("ab3")
    ])
def test_check_int_formate_error(input):
    from patient_server import check_int_formate
    with pytest.raises(ValueError):
        check_int_formate(input)


@pytest.mark.parametrize("input, db, expected", [
    (12345, db, {'patient_id': 12345,
                 'attending_username': "Junyu.N",
                 'heart_rate': [99, 98, 100, 101],
                 'patient_age': 23}),
    (23456, db, {'patient_id': 23456,
                 'attending_username': "Mario.C",
                 'heart_rate': [150, 151, 152, 154],
                 'patient_age': 50})
    ])
def test_find_patient_from_db(input, db, expected):
    from patient_server import find_patient_from_db
    answer = find_patient_from_db(input, db)
    assert answer == expected


@pytest.mark.parametrize("input, db, expected", [
    ("Junyu.N", db, [
        {'patient_id': 12345,
         'attending_username': "Junyu.N",
         'heart_rate': [99, 98, 100, 101],
         'patient_age': 23}]),
    ("Mario.C", db, [
        {'patient_id': 23456,
         'attending_username': "Mario.C",
         'heart_rate': [150, 151, 152, 154],
         'patient_age': 50},
        {'patient_id': 34567,
         'attending_username': "Mario.C",
         'heart_rate': [123, 123, 125, 125],
         'patient_age': 10}])
    ])
def test_find_patient_with_doc(input, db, expected):
    from patient_server import find_patient_with_doc
    answer = find_patient_with_doc(input, db)
    assert answer == expected


@pytest.mark.parametrize("age, heart_rate, expected", [
    (2, 155, "tachycardic"),
    (4, 155, "tachycardic"),
    (7, 130, "not tachycardic"),
    (11, 120, "not tachycardic"),
    (15, 133, "tachycardic"),
    (20, 90, "not tachycardic"),
    ])
def test_check_status(age, heart_rate, expected):
    from patient_server import check_status
    answer = check_status(age, heart_rate)
    assert answer == expected


@pytest.mark.parametrize("input, expected", [
    ({'patient_id': 12345,
      'attending_username': "Junyu.N",
      'patient_age': 23},
     {'patient_id': 12345,
      'attending_username': "Junyu.N",
      'patient_age': 23,
      'heart_rate': [],
      'time_stamp': []})
    ])
def test_load_patient(input, expected):
    from patient_server import load_patient
    answer = load_patient(input)
    assert answer == expected
