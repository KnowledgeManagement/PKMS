from dataclasses import dataclass, field
from enum import Enum
import json
import magic
from pathlib import Path
import requests
import response 

def DecimalSize(size) -> str:
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while size >= 1024 and i < len(suffixes) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {suffixes[i]}"

class Mod(Enum):
    DOWNLOAD = "d"
    UPLOAD = "u"

@dataclass(init=True)
class APIClass:
    OAuth : str
    list_of_data: list = field(default_factory=list)
    resp: str = "empty"
    disk_path: str = "/"
    mod: Mod = Mod.DOWNLOAD
    key_values = {"YandexDataUrl" : "https://cloud-api.yandex.net/v1/disk/resources",
                  "YandexDownloadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/download",
                  "YandexUploadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/upload"}

    def GetMetaData(self):
        headers = {'Accept' : 'application/json', 'Authorization' : self.OAuth}
        list_of_dir = []
        list_of_files = []
        resp = f""
        request = requests.get(self.key_values["YandexDataUrl"], headers=headers, params={'path' : self.disk_path, 'sort' : 'path'})
        if request.status_code != 200:
            resp += f"something goes wrong : {str(request.status_code)}"
            resp += f"{request.json()['description']}"
            self.list_of_data = [resp]
        for item in request.json()["_embedded"]['items']:
            if item["type"] == 'dir':
                list_of_dir.append(item["name"])
            if item['type'] == 'file':
                list_of_files.append([item['name'], item['size'], item['modified']])
        self.list_of_data = [list_of_dir, list_of_files]
    
    def MetaDataDownload(self):
        resp = ""
        for i in range(len(self.list_of_data[0])):
            resp += (f"d {self.list_of_data[0][i]}  /cd{i} \n")
        for i in range(len(self.list_of_data[1])):
            resp += (f"f {i} {self.list_of_data[1][i][0]} {DecimalSize(self.list_of_data[1][i][1])} /get{i}\n")
        resp += "/back  /root\n"
        self.resp = resp

    def MetaDataUpload(self):
        resp = ""
        for i in range(len(self.list_of_data[0])):
            resp += (f"d {self.list_of_data[0][i]}  /cd{i} \n")
        for i in range(len(self.list_of_data[1])):
            resp += (f"f {i} {self.list_of_data[1][i][0]} {DecimalSize(self.list_of_data[1][i][1])} \n")
        resp += "/back  /root\n"
        self.resp = resp

    def GetUploadUrl(self, upload_path) -> str:
        headers = {'Accept' : 'application/json', 'Authorization' : self.OAuth}
        request = requests.get(self.key_values["YandexUploadUrl"], headers=headers, params={'path' : upload_path})
        if request.status_code != 200 :
            description = request.json()["description"]
            print(f"something goes wrong : {description}" + str(request.status_code))
            return ""
        return request.json()['href']

    def GetDownloadUrl(self, download_path) -> str:
        headers = {'Accept' : 'application/json', 'Authorization' : self.OAuth}
        request = requests.get(self.key_values["YandexDownloadUrl"], headers=headers, params={'path' : download_path})
        if request.status_code != 200:
            print("something goes wrong : " + str(request.status_code))
            return ""
        return request.json()['href']

    def UploadViaLink(self, download_link, file_name):
        headers = {'Accept' : 'application/json', 'Authorization' : self.OAuth}
        whole_path = self.disk_path + file_name
        request = requests.post(self.key_values["YandexUploadUrl"], headers=headers, params={"url": download_link,"path" : whole_path})
        # print(request.json()["description"])
        status = requests.get(request.json()['href'])
        print(status)