from typing import Any, Dict


class Lambda_Client:
    def invoke(
        self,
        FunctionName: str,
        Payload: Dict[str, Any],
    ) -> str:
        assert isinstance(FunctionName, str)
        assert Payload

        return "Succeeded"
