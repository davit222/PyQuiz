import requests
import json
import sqlite3

#^^^^^^^ EX 1 ^^^^^^
url = f'https://api.ratesapi.io/api/2010-01-12?base=USD&symbols=RUB'
response = requests.request("GET", url)
print(response)
print(response.status_code)
print(response.headers)
print("Details: ", response.headers['Set-Cookie'])


#^^^^^^^ EX 2 ^^^^^^

url = f'https://api.ratesapi.io/api/2010-01-12?base=USD&symbols=RUB'
response = requests.request("GET", url)

result_json = response.text
res = json.loads(result_json)
res_structured = json.dumps(res, indent=4)

#^^^^^^^ EX 3 ^^^^^^
curr_from = input("Input Base Currency")
curr_to = input("Input Rate Currency")
year = input("Input Date(Min. 2006) With Fomrat YYYY-DD-MM ")
url = f'https://api.ratesapi.io/api/{year}?base={curr_from}&symbols={curr_to}'
response = requests.request("GET", url)
# print(response.text)
result_json = response.text
res = json.loads(result_json)
res_structured = json.dumps(res, indent=4)

date = res['date']
value_2 = res['rates'][curr_to]

print("For", date, "Year 1", curr_from, "was worth", value_2, curr_to)

#^^^^^^^ EX 4 ^^^^^^
# მომხმაებელს მონაცემთა ბაზაში EXCHANGE_TABLES არსებულ ცხრილში EXCHANGE_RATES შეუძლია ჩაწეროს მის მიერ შეყვანილი ვალუტა curr_from
#რომლის ერთეულის ღირებულების გაგებაც სურს მეორე ვალუტაში curr_to შესაბამისი წლების დასაწყისში. მაგალითად მას შეუძლია
#შეყვანოს სასურველი წელის(2006 იდან ზემოთ) და მის შემდეგ რეინჯის მითითებით გარკვეული წლებში არსებული მონაცემები მიიღოს.
conn = sqlite3.connect("EXCHANGE_TABLES.sqlite")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE EXCHANGE_RATES
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                Currency_From FLOAT,
                Currency_To VARCHAR(50),
                Date DATE);''')
year = int(input("Input Year(Min. 2006) "))
curr_from = input("Input Base Currency With UpperCase")
curr_to = input("Input Rate Currency With UpperCase")
range_years = int(input("Insert Range "))
for each in range(range_years):
    year+=1
    url = f'https://api.ratesapi.io/api/{year}-02-01?base={curr_from}&symbols={curr_to}'
    response = requests.request("GET", url)
    result_json = response.text
    res = json.loads(result_json)
    res_structured = json.dumps(res, indent=4)
    date = res['date']
    value_2 = str(res['rates'][curr_to])
    cursor.execute('INSERT INTO EXCHANGE_RATES (Currency_From, Currency_To, Date) VALUES (?, ?, ?)',(curr_from,value_2+curr_to,date))
    conn.commit()
conn.close()