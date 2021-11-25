'''the requests module simplifies sending HTTP requests.'''
import requests


class StatusChecker():
    '''handle getting responses and record status of each site'''
    def __init__(self, url) -> None:
        self.url = url
        self.status = None

    def check_status(self):
        '''send a HTTP requests and use it to determine site status.'''
        try:
            # Send HTTP GET request to the given url
            response = requests.get(self.url)
            # Response codes of the format 5xx are server errors.
            # This would indicate that the website is down,
            # hence status is set to false (Down)
            if str(response.status_code)[0] == '5':
                self.status = False
            else:
                # Typically, a 200 OK code will be sent back from a page,
                # however client errors can also occurr, of the format 4xx,
                # such as a 404 (page requested wasn't found).
                # This doesn't suggest that there's an issue with the server,
                # however, so the status is still set to True (Live)
                self.status = True
        except Exception as exception:
            print(f'The following exception was caught: {exception}')

    def get_status(self):
        '''return the boolean status attribute.'''
        return self.status
