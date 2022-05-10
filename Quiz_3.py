import requests
import json
import sqlite3

#1
url = "https://mailcheck.p.rapidapi.com/"
domain = input('შეიყვანეთ ელ-ფოსტა ან დომენური სახელი: ')
payload = {"domain": domain}
headers = {	"X-RapidAPI-Host": "mailcheck.p.rapidapi.com",
			"X-RapidAPI-Key": "876c28ce0cmsh0170b6a656d6f1fp1c3465jsnc828e868617e"}

response = requests.get(url, headers=headers,  params=payload)
# print(response.status_code)
# print(response.content)
# print(response.headers)


#2
r = response.json()
f = open('domains.json', 'w')
json.dump(r, f, indent=4)


#3
#პირველ დავალებაში შეიყვანა მომხმარებელმა დომეინი და აქ ვუბეჭდავ, არის თუ არა ვალიდური/დასაბლოკი, ასევე რამდენადაა
#რისკის შემცველი
if r['valid'] == False and r['block'] == True:   #r['valid'] boolean ტიპის აღმოჩნდა
	print('შეყვანილი დომეინი არავალიდურია, უმჯობესია დაბლოკოთ')
elif r['valid'] == True and r['block'] == False and r['risk'] > 15:
	print('შეყვანილი დომეინი ვალიდურია, თუმცა უმჯობესია უსაფრთხოებისთვის იცოდეთ,'
		  ' რომ რისკისშემცველობა არის {}'.format(r['risk']))
else: print('შეყვანილი დომეინი უსაფრთხოა')


#4
#მომხმარებელს ექნება სია, რომელშიც იქნება ასახული არავალიდური იმეილები ან ის იმეილები, რომლებსაც
# ჩვეულზე მაღალი რისკისშემცველობა აქვთ
conn = sqlite3.connect('domains_database.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS UNSAFE_DOMAINS
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 domain VARCHAR(50),
                 valid VARCHAR(5),   --ვინაიდან პასუხები არის True ან False
                 block VARCHAR(5),
                 risk INTEGER,
                 mx_host VARCHAR(100))
                 ''')

e_valid = r['valid']
e_block = r['block']
e_risk = r['risk']
mx_host = r['mx_host']  #MX არის Mail Exchange მისი ჰოსტები არიან, მაგალითად, google.com(gmail.com-ის)

if e_valid == False or e_block == True or e_risk > 15:
	cursor.execute('INSERT INTO DOMAINS(domain, valid, block, risk, mx_host) VALUES(?, ?, ?, ?, ?)',
	(domain, str(e_valid), str(e_block), e_risk, mx_host))
conn.commit()


conn.close()


