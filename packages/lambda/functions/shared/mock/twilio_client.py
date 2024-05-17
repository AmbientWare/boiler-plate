class Messages:
    def create(self, body: str, from_: str, to: str) -> str:
        return "Successful"


class Calls:
    def create(
        self,
        url: str,
        record: bool,
        send_digits: str,
        time_limit: int,
        trim: str,
        from_: str,
        to: str,
        recording_status_callback: str,
        recording_channels: str = "",
    ) -> str:
        assert isinstance(url, str)
        assert isinstance(record, bool)
        assert isinstance(send_digits, str)
        assert isinstance(time_limit, int)
        assert isinstance(trim, str)
        assert isinstance(from_, str)
        assert isinstance(to, str)
        assert isinstance(recording_status_callback, str)
        assert recording_channels in ["", "dual", "mono"]

        return "Succeeded"


class TwilioClient:
    def __init__(self) -> None:
        self.messages = Messages()
        self.calls = Calls()
