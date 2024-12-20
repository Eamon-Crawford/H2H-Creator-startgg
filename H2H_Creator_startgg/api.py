import requests
from .exceptions import TooManyRequestsError, ResponseError, RequestError, ServerError, NoIdeaError

def run_query(query, variables, header):
    json_request = {'query': query, 'variables': variables}
    try:
        request = requests.post(url='https://api.start.gg/gql/alpha', json=json_request, headers=header)
        if request.status_code == 400:
            raise RequestError
        elif request.status_code == 429:
            raise TooManyRequestsError
        elif 400 <= request.status_code < 500:
            raise ResponseError
        elif 500 <= request.status_code < 600:
            raise ServerError
        elif 300 <= request.status_code < 400:
            raise NoIdeaError

        response = request.json()
        return response

    except RequestError:
        print("Error 400: Bad request (probably means your key is wrong)")
        return 400

    except TooManyRequestsError:
        print("Error 429: Sending too many requests right now")
        return 429

    except ResponseError:
        print("Error {}: Unknown request error".format(request.status_code))
        return 404

    except ServerError:
        print("Error {}: Unknown server error".format(request.status_code))
        return 500

    except NoIdeaError:
        print("Error {}: I literally have no idea how you got this status code, please send this to me".format(request.status_code))
        return