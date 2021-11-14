

class CustomException(Exception):
    def __init__(self, app_name: str, endpoint: str, ):
        self.endpoint = endpoint
        self.app_name = app_name
