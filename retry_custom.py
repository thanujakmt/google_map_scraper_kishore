import requests
import time

def retryFunction(func, retries = 3):
    def retry_wrapper(*args, **kwargs):
        attemp =0
        while attemp<retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
                time.sleep(2)
                attemp += 1
    return retry_wrapper
@retryFunction
def getData():
    url = 'https://www.google.com'
    r = requests.get(url)
    print(r.text)

if __name__ == '__main__':
    getData()
