import requests

res = requests.get(
    url='https://jetlend-dev.akiselev.group/accounting/hs/borrowerNDFL/startTask',
    cert='cacert.pem'
)

print(res.text)