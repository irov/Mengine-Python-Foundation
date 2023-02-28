import json
from Foundation.Task.TaskHeaderDataBase import TaskHeaderDataBase


class TaskPlayFabRequest(TaskHeaderDataBase):

    def _onSuccess(self, response):
        error_data = response_data = None

        # Contacted playfab
        decoded_response = json.loads(response)

        if decoded_response["code"] != 200:
            # contacted PlayFab, but response indicated failure
            error_data = decoded_response
        else:
            # successful call to PlayFab
            response_data = decoded_response["data"]

        if error_data and self.cb:
            try:
                # Notify the caller about an API Call failure
                self.cb(None, error_data)
            except Exception as e:
                # Global notification about exception in caller's callback
                self.log(str(e))
        elif response_data and self.cb:
            try:
                # Notify the caller about an API Call success
                self.cb(response_data, None)
            except Exception as e:
                # Global notification about exception in caller's callback
                self.log(str(e))

    def _onFailed(self, error, response):
        self.cb(None, {
            "code": 408,
            "status":
                "Request Timeout",
            "error": "ServiceUnavailable",
            "errorCode": 1123,
            "errorMessage": error,
            "errorDetails": None,
        })
