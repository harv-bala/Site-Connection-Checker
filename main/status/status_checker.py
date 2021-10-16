import requests

class StatusChecker():
    def __init__(self, domain) -> None:
        self.domain = domain
        self.status = None

    def check_status(self):
        try:
            response = requests.get(self.domain)
            if str(response.status_code)[0] == '5':
                self.status = False
            else:
                self.status = True
        except Exception as e:
            print(f'The following exception was caught: {e}')

    def get_status(self):
        return self.status