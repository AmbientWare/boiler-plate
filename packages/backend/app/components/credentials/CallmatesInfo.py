from app.components import ComponentInput
from app.components.credentials import BaseCredential

CallmatesInfo = BaseCredential(
    label="Callmates Info",
    name="CallmatesInfo",
    description="Please add your information so we can automate you test check!",
    inputs=[
        ComponentInput(
            label="Phone Number",
            name="userPhoneNumber",
            type="string",
            value="",
            description="Your phone number",
        ),
        ComponentInput(
            label="Hotline Phone Number",
            name="hotlinePhoneNumber",
            type="password",
            value="",
            description="The phone number for your hotline.",
        ),
        ComponentInput(
            label="Hotline ID",
            name="hotlineId",
            type="password",
            value="",
            description="The ID related to your hotline.",
        ),
    ],
)
