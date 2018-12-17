from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from config.settings.base import SMS_API_KEY, SMS_API_SECRET

##  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP



def send_sms(number, message):
    # set api key, api secret
    api_key = SMS_API_KEY
    api_secret = SMS_API_SECRET
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['from'] = '01066511550' # Sender number
    params['text'] = str(message) # Message

    if isinstance(number, (list, tuple)):
        number = ','.join(number)

    params['to'] = str(number)  # Recipients Number '01000000000,01000000001'

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)