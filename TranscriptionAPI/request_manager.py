import os

class UrlRequest:
    def __init__(self, url:str, progress:int, filename:str):
        self.url = url
        self.progress = progress
        self.filename = filename

class RequestManager:
    request_index = 1
    request_items = {}

    @staticmethod
    def create_request(url_request):
        rm = RequestManager
        rm.request_items[rm.request_index] = url_request

        os.mkdir("Requests/" + str(rm.request_index))

        rm.request_index = rm.request_index + 1
        return (rm.request_index - 1)

    @staticmethod
    def get_progress(index):
        return RequestManager.request_items[index].progress