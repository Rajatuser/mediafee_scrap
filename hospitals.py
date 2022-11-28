import requests
from bs4 import BeautifulSoup
import pandas as pd
from models import hospitals, facilities
from models import engine
import datetime
from sqlalchemy import insert

base_url = 'https://www.medifee.com'  # base url to get te links
hospitals.metadata.create_all(engine)  # to create table from classes in sqlalchemy


def hospital_data():
    res = requests.get(base_url + '/hospitals-in-chandigarh')  # base url to get all the anchor href
    soup = BeautifulSoup(res.content, "html.parser")
    a = soup.find_all("a", href=True)  # query to find all the anchor href's
    count = 0  # to count the id of the hospitals
    for i in a:  # to iterate through every link
        if 'hospital/' in i['href']:  # to ensure that links belong to the hospitals
            req = requests.get(base_url + i['href'])  # to send an http requests to the link
            soups = BeautifulSoup(req.content, "html.parser")

            facility = []  # list to store the facilities in a hopital
            price = []  # list tp stpre the price of the facilities of the hospital

            hospitala = []  # to store the name and address of the hospital

            ndata = soups.find("h4").text  # find all the h4 tags to get te name of the hospital
            print(ndata, "Hospital")
            hospitala.append(ndata)

            fdata = soups.find("p")  # find all the p tags to get the address of the hospitals
            print(fdata.text, "address")
            hospitala.append(fdata.text)

            num = fdata.next_sibling.text[6:]  # to remove phone number string from the actual number
            numbers = [i for i in num if i.isdigit()]  # conditioning a list to get the contact numbers of hospitals
            if len(numbers) > 9:
                print("".join(numbers[:10]), "numbers")
                pnumber = "".join(numbers[:10])
                data = (insert(hospitals).
                        values(hospital=str(hospitala[0]),
                               address=str(hospitala[1]),
                               contact_number=pnumber,
                               status=True))
                result = engine.execute(data)

            else:
                # to add the hospital name and address in the hospital table
                data = (insert(hospitals).
                        values(hospital=str(hospitala[0]),
                               address=str(hospitala[1]),
                               status=True))
                engine.execute(data)

            count += 1

            datatable = soups.find("table", {"class": "table"})
            for i in datatable.find_all("td")[0::2]:
                facility.append(i.text)

            for i in datatable.find_all("td")[1::2]:
                price.append(i.text)

            for datafac in range(len(facility)):
                # to add the facility and price in the facility table along with hospital id
                data = (
                    insert(facilities).
                    values(hospital_id=count, facility=str(facility[datafac]),
                           price=str(price[datafac]),
                           status=True))

                engine.execute(data)


hospital_data()




