import json , requests
import kiteconnect.exceptions as ex
import logging
from urllib.parse import urljoin
from kiteconnect import KiteConnect, KiteTicker

log = logging.getLogger(__name__)


class KiteApp(KiteConnect):

    def __init__(self, api_key, userid, enctoken):
        self.api_key = api_key
        self.user_id = userid
        self.enctoken = enctoken
        self.headers = {
            "x-kite-version": "3",
            'Authorization': 'enctoken {}'.format(self.enctoken)
        }
        KiteConnect.__init__(self, api_key=api_key)

    def kws(self):
        return KiteTicker(api_key='kitefront', access_token=self.enctoken+"&user_id="+self.user_id, root='wss://ws.kite.trade')

    def _request(self, route, method, url_args=None,query_params=None,params=None, is_json=False):
        """Make an HTTP request."""
        if url_args:
            uri = self._routes[route].format(**url_args)
        else:
            uri = self._routes[route]

        url = urljoin(self.root, uri)

        headers = self.headers

        if self.debug:
            log.debug("Request: {method} {url} {params} {headers}".format(method=method, url=url, params=params, headers=headers))

        try:
            r = self.reqsession.request(method,
                                        url,
                                        json=params if (method in ["POST", "PUT"] and is_json) else None,
                                        data=params if (method in ["POST", "PUT"] and not is_json) else None,
                                        params=params if method in ["GET", "DELETE"] else None,
                                        headers=headers,
                                        verify=not self.disable_ssl,
                                        allow_redirects=True,
                                        timeout=self.timeout,
                                        proxies=self.proxies)
        except Exception as e:
            raise e

        if self.debug:
            log.debug("Response: {code} {content}".format(code=r.status_code, content=r.content))

        # Validate the content type.
        if "json" in r.headers["content-type"]:
            try:
                data = json.loads(r.content.decode("utf8"))
            except ValueError:
                raise ex.DataException("Couldn't parse the JSON response received from the server: {content}".format(
                    content=r.content))

            # api error
            if data.get("error_type"):
                if self.session_expiry_hook and r.status_code == 403 and data["error_type"] == "TokenException":
                    self.session_expiry_hook()

                # native Kite errors
                exp = getattr(ex, data["error_type"], ex.GeneralException)
                raise exp(data["message"], code=r.status_code)

            return data["data"]
        elif "csv" in r.headers["content-type"]:
            return r.content
        else:
            raise ex.DataException("Unknown Content-Type ({content_type}) with response: ({content})".format(
                content_type=r.headers["content-type"],
                content=r.content))

def login_with_credentials(userid, password, twofa):
    reqsession = requests.Session()
    r = reqsession.post('https://kite.zerodha.com/api/login', data={
        "user_id": userid,
        "password": password
    })

    r = reqsession.post('https://kite.zerodha.com/api/twofa', data={
        "request_id": r.json()['data']['request_id'],
        "twofa_value": twofa,
        "user_id": r.json()['data']['user_id']
    })
    enctoken = r.cookies.get('enctoken')
    with open('enctoken.txt', 'w') as wr:
        wr.write(enctoken)

def get_historical_data(self, instrument_token, from_date, to_date, interval):
    """Fetch historical data for a given instrument token"""
    try:
            historical_data = self.historical_data(
                instrument_token,
                from_date,
                to_date,
                interval
            )
            return historical_data
    except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None
