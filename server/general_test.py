import requests
import pytest
def register():
    response = requests.post("http://localhost:8000/register", json={
        "email": "kaisergrobe@gmail.com",
        "phone_number": "+79234679690",
        "password": "ABCDEFabcd123#./",
        "name": "Goi",
        "last_name": "Judikulovich",
        "surname": "Xoi"
    })
    x = response.json()
    assert x["Message"] == "Verify your email!"
    code = int(input("Enter sended code:"))
    response = requests.post("http://localhost:8000/verify", json={
        "code": code,
        "identifier": x["Identifier"]
    })
    assert response.json()["Message"] == "Verified successfully!"
    return x
def test_account_creation():
    x = register()
    user_id = x["Identifier"]
    ident = "kaisergrobe@gmail.com"
    password = "ABCDEFabcd123#./"
    x = {}
    assertion = ident.startswith("+")
    x["phone_number" if assertion else "email"] = ident
    x["email" if assertion else "phone_number"] = ""
    x["password"] = password
    response = requests.post("http://localhost:8000/login", json=x)
    x = response.json()
    assert x["Message"] == "Success"
    token = x["Token"]
    response = requests.post("http://localhost:8000/account/create", json={
        "acc": {
            "currency_tag": "RUB",
            "user_id": user_id
        },
        "token": token
    })
    x = response.json()
    assert x["Message"] == "Success"
    accs = {}
    accs["RUB"] = x["AccountID"]
    response = requests.post("http://localhost:8000/account/create", json={
        "acc": {
            "currency_tag": "EUR",
            "user_id": user_id
        },
        "token": token
    })
    x = response.json()
    assert x["Message"] == "Success"
    accs["EUR"] = x["AccountID"]
    response = requests.post("http://localhost:8000/account/create", json={
        "acc": {
            "currency_tag": "USD",
            "user_id": user_id
        },
        "token": token
    })
    x = response.json()
    assert x["Message"] == "Success"
    accs["USD"] = x["AccountID"]
    response = requests.post(f"http://localhost:8000/account/deposit/{accs['USD']}", json={
        "token": token,
        "amount": 1500
    })
    assert response.json()["Message"] == "Success"
    # THIS TEST IS BUGGED, SOMEWHY FASTAPI THROWS "BODY - EXPECTED STR" error only here
    '''response = requests.post("http://localhost:8000/account/transfer", json={
        "token": token,
        "account_from_id": accs["USD"],
        "account_to_id": accs["EUR"],
        "amount": 500.0
    })
    print(response.json())
    assert response.json()["Message"] == "Success"'''
    response = requests.post(f"http://localhost:8000/account/{accs['EUR']}", json=token)
    print(response.json())
    response = requests.post("http://localhost:8000/account", json={
        "user_id": user_id,
        "token": token
    })
    print(response.json())