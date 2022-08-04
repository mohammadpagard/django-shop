from kavenegar import *


def send_otp_code(phone_numebr, code):
    try:
        api = KavenegarAPI('397776766166513478504C317069744B41435247432F635062677377356530436F4F39473264426A4F50513D')
        params = {
            'sender': '',
            'receptor': phone_numebr,
            'message': f"You're verify code is {code}"
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
