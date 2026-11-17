import time

import httpx


_RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}
_MAX_ATTEMPTS = 3


def _with_retry(send):
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = send()
        except (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError):
            if attempt == _MAX_ATTEMPTS:
                raise
        else:
            if response.status_code not in _RETRYABLE_STATUS or attempt == _MAX_ATTEMPTS:
                return response
            response.close()
        time.sleep(attempt)


def get_with_retry(url, **kwargs):
    return _with_retry(lambda: httpx.get(url, **kwargs))


def put_bytes_with_retry(url, content, **kwargs):
    return _with_retry(lambda: httpx.put(url, content=content, **kwargs))


def put_file_with_retry(url, file_path, **kwargs):
    def send():
        with open(file_path, "rb") as source:
            return httpx.put(url, content=source, **kwargs)

    return _with_retry(send)
