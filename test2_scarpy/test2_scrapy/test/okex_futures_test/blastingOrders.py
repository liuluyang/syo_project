import requests


contract_url = 'https://www.okex.me/v2/futures/pc/queryInfo/contractInfo.do'
contractInfo = requests.post(contract_url).json()
if contractInfo.get('msg') == 'success':
    contracts = contractInfo.get('contracts')
    print(contracts)

data = {
'status': 1,
'currentPage': 20,
'contractId': 201811300000034,
'pageLength': 50,
}

r = requests.post('https://www.okex.me/v2/futures/pc/public/blastingOrders.do',
                  data = data).json()

print(r)
if r.get('msg') == 'success':
    data = r.get('data', {})
    data_list = data.get('futureContractOrdersList')
    for index, d in enumerate(data_list):
        print(index, d)