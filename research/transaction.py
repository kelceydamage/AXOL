import datetime
import random

def merchant_id_randomizer():
	merchant_ids = [
		1092,
		9281,
		3,
		32,
		526,
		876,
		82,
		93586,
		2568285,
		2658
		]
	x = random.randint(0, len(merchant_ids))
	if 4 < x < 7:
		x = random.randint(2, x)
	return merchant_ids[x - 1]

body={
	'Id': 509004,
	'UserId': 2996,
	'CustomerId': 40081,
	'DeferDate': 'NULL',
	'Date': datetime.datetime.now(),
	'Status': 6,
	'Amount': 0,
	'PreviousTransactionId': 'NULL',
	'BaseTransactionId': 'NULL',
	'BatchLogId': 'NULL',
	'SourceIP': 'NULL',
	'AmountTax': 'NULL',
	'AmountTip': 'NULL',
	'AmountFood': 'NULL',
	'AmountMisc': 'NULL',
	'OrderId': 'NULL',
	'InvoiceId': 'NULL',
	'IsPadSigned': 0,
	'PadSignature': 'NULL',
	'Signature': 'NULL',
	'Response': 'NULL',
	'IsRecurring': 1,
	'RecurringPlanId': 1574,
	'TestMode': 0,
	'SystemAccountId': 1142,
	'TransactionType': 1,
	'ApiSessionId': 'NULL',
	'BCCEmail': 'NULL',
	'Description': 'qplay (monthly)',
	'Lat': 'NULL',
	'Long': 'NULL',
	'CardType': 2,
	'CardSuffix': 4131,
	'ApiSourceId': 7,
	'TransactionId': 100177017887,
	'CardExpiry': '04/16',
	'OriginalId': 'NULL',
	'Firstname': 'miss victoria',
	'Lastname': 'marshall',
	'Email': 'sheffbhoy91@gmail.com',
	'Company': 'NULL',
	'Telephone': '',
	'Address1': '',
	'Address2': '',
	'City': '',
	'Province': '',
	'Country': '',
	'PostalCode': '',
	'CurrencyId': 1,
	'AmountRefunded': 'NULL',
	'Captured': 'NULL',
	'AuthCode': '**01ND',
	'PayfirmaSupervisorName': 'NULL'
	}