import urllib
import json
import re
from flask import Flask, request
import json as simplejson
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)


@app.route("/ProcessPayment/<string:CreditCardNumber>/<string:CardHolder>/<string:ExpirationDate>/<string:SecurityCode>/<string:Amount>"
, methods=['GET'])
def ProcessPayment(CreditCardNumber, CardHolder,ExpirationDate,SecurityCode, Amount  ):
    try:
       
        isVerified, error = procecssData(CreditCardNumber,CardHolder, ExpirationDate,SecurityCode,Amount)
        if (isVerified):
            paymentType = process_payment(float(Amount))
            print(paymentType)
            return dumps({'success': paymentType})
        else:
            return dumps({'success': error})

    except Exception as e:
        return dumps({'error': str(e)})



def process_payment(Amount):
    print(Amount)
    payment = ''
    if ((Amount)<20.0):
        payment = CheapPaymentGateway(Amount)
    elif ((Amount)>20.0 and (Amount)<500.0):
        payment = ExpensivePaymentGateway(Amount)
    elif ((Amount)>500.0):
        payment = PremiumPaymentGateway(Amount)

    print (payment)
    return payment


def CheapPaymentGateway(Amount):
    return str(Amount)+" payment done via cheap gateway"

def ExpensivePaymentGateway(Amount):
    return str(Amount)+" payment done via expensive gateway"

def PremiumPaymentGateway(Amount):
    return str(Amount)+" payment done via premium gateway"

def procecssData(CreditCardNumber,CardHolder,ExpirationDate,SecurityCode,Amount):
    validCard = cardValidator(CreditCardNumber)
    validName = isinstance(CardHolder, str)
    validDate = compareDate(ExpirationDate)
    validCode = validateCode(SecurityCode)
    validAmount = validateAmount(Amount)
    if (not validCard):
        return False, "invalid card"
    elif (not validName):
        return False, "invalid name"
    elif (not validDate):
        return False, "invalid date"
    elif (not validCode):
        return False, "invalid security code"
    elif (not validAmount):
        return False, "invalid amount"
    else:
        return True, "valid"


def validateAmount(Amount):
    if "." in Amount:
        if (float(Amount) >0 ):
            return True
        else:
            return False
    else:
        return False


def validateCode(SecurityCode):
    if (len(SecurityCode) == 3):
        return True
    else:
        return False


def compareDate(ExpirationDate):
    todaysDate = datetime.now()
    splitDate = ExpirationDate.split("-")
    actualDate = datetime(int(splitDate[2]), int(splitDate[1]), int(splitDate[0]))

    print (actualDate)
    print(todaysDate)
    if (actualDate>todaysDate):
        return True
    else:
        return False

def cardValidator(n):
    validatelist=[]
    for i in n:
        validatelist.append(int(i))
    for i in range(0,len(n),2):
        validatelist[i] = validatelist[i]*2
        if validatelist[i] >= 10:
            validatelist[i] = validatelist[i]//10 + validatelist[i]%10
    if sum(validatelist)%10 == 0:
        return True
    else:
        return False



if __name__ == '__main__':
    app.run()







