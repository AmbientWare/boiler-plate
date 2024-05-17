from typing import Any, Dict

from twilio.twiml.voice_response import VoiceResponse

# This response API is never hit because we pass in the params
# programmatically when we make a call. (At least I think that's why)
# However, we are required to give it an api to hit regardless so we
# provide it this empty dummy VoiceResponse endpoint to keep it happy


def get_xml() -> str:
    response = VoiceResponse()
    return str(response)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    xml_response = get_xml()

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": xml_response,
    }
