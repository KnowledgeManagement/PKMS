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

class API:
    key_values = {"YandexDataUrl" : "https://cloud-api.yandex.net/v1/disk/resources",
                  "YandexDownloadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/download",
                  "YandexUploadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/upload"}
    def __init__(self, config_path):
        # self.request = requests() how to create a variable with response type
        self.config = json.load(open(config_path))
        # self.key_values = {"YandexDataUrl" : "https://cloud-api.yandex.net/v1/disk/resources",
        #                    "YandexDownloadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/download",
        #                    "YandexUploadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/upload"}
        # print("test APi init")

    def GetDownloadUrl(self, path, headers) -> str:
        request = requests.get(self.key_values["YandexDownloadUrl"], headers=headers, params={'path' : path})
        if request.status_code != 200:
            print("something goes wrong : " + str(request.status_code))
            return ""
        return request.json()['href']

    def CreateFileFromUrl(self, url, file_name) -> str:
        request = requests.get(url=url)
        current_dir = Path.cwd()
        file_path = str(current_dir) + "/" + file_name
        if Path(file_path).exists():
            suffixes = Path(file_name).suffixes
            suffixes_name = "".join(suffixes)
            p = Path(file_path)
            i = 1
            while p.exists():
                p_stem = file_path
                for j in range(len(suffixes)):
                    p_stem = Path(p_stem).stem
                if i > 1:
                    file_path = str(p.parent) + '/' + p_stem[0 : len(str(p.stem))-1] + str(i) + suffixes_name
                else:
                    file_path = str(p.parent) + "/" + p_stem + str(i) + suffixes_name
                p = Path(file_path)
                i += 1
            with open(p.name, "wb") as file:
                file.write(request.content)
            return p.name
        else:
            with open(file_name, "wb") as file:
                file.write(request.content)
            return file_name

    def CreateNewDirectory(self, path, headers):
        request = requests.put(self.key_values["YandexDataUrl"], headers=headers, params={'path': path})
        # print(request.json()["error"])
        if request.status_code == 409:
            if request.json()["error"] == "DiskPathPointsToExistentDirectoryError" :
                print(f"specified directory {path} already exists")
                return
            parents = Path(path).parents
            for i in range(len(parents)-1, -1, -1):
                request = requests.put(self.key_values["YandexDataUrl"], headers=headers, params={'path': parents[i]})
            request = requests.put(self.key_values["YandexDataUrl"], headers=headers, params={'path': path})
        if request.status_code != 201:
            description = request.json()["description"]
            print(f"{request.status_code} something gone wrong \n error description: {description}")
        
    def GetMetaData(self, path, headers) -> list:
        list_of_dir = []
        list_of_files = []
        request = requests.get(self.key_values["YandexDataUrl"], headers=headers, params={'path' : path, 'sort' : 'path'})
        if request.status_code != 200:
            print("something goes wrong : " + str(request.status_code))
            print(request.json()['description'])
            exit()
        for item in request.json()["_embedded"]['items']:
            if item["type"] == 'dir':
                list_of_dir.append(item["name"])
            if item['type'] == 'file':
                list_of_files.append([item['name'], item['size'], item['modified']])
        for dir in list_of_dir:
            print("d", dir, end='\n')
        for i in range(len(list_of_files)):
            print("f", i, list_of_files[i][0], DecimalSize(list_of_files[i][1]), list_of_files[i][2])
        return [list_of_dir, list_of_files]

    def CheckPathExistance(self, path) -> bool:
        headers = {'Accept' : 'application/json', 'Authorization' : self.config['OAuth']}
        request = requests.get(self.key_values["YandexDataUrl"], headers=headers, params={'path' : path, 'sort' : 'path'})
        if request.status_code != 200:
            return False
        return True

    def GetUploadUrl(self, download_path, headers) -> str:
        request = requests.get(self.key_values["YandexUploadUrl"], headers=headers, params={'path' : download_path})
        if request.status_code != 200 :
            description = request.json()["description"]
            print(f"something goes wrong : {description}" + str(request.status_code))
            return ""
        return request.json()['href']

    def PutFile(self, url, headers, file_path):
        request = requests.put(url, data=open(file_path, 'rb'), headers=headers)
        if request.status_code != 201 and request.status_code != 202:
            description = request.json()["description"]
            print(f"something goes wrong : {description}" + str(request.status_code))
            return False
        return True

    def ChoosePath(self) -> str:
        headers = {'Accept' : 'application/json', 'Authorization' : self.config['OAuth']}
        path = '/'
        list_of_data = self.GetMetaData(path, headers=headers)
        req = input()
        while req != "exit":
            if "cd " in req:
                trash, number =  req.split()
                if number == ".." or number == '../':
                    path = str(Path(path).parent)
                    list_of_data = self.GetMetaData(path, headers=headers)
                    req = input()
                    continue
                if int(number) >= len(list_of_data[0]):
                    print("Wrong dir number")
                    req = input()
                    continue
                path += list_of_data[0][int(number)]
                path += '/'
                list_of_data = self.GetMetaData(path, headers=headers)
                req = input()
                continue
            elif "here":
                return path
            else:
                print("Wrong command")
                req = input()
        return path

    def UploadScript(self, file_path, file_name, disk_path):
        mime = magic.Magic(mime=True)
        Content_type = mime.from_file(str(file_path))
        headers = {'Accept' : 'application/json', 'Authorization' : self.config['OAuth']}
        headers_send = {'Content-type' : Content_type, 'Slug' : file_name}
        download_url = self.GetUploadUrl(disk_path + file_name, headers)
        if download_url == "":
            exit()
        print(f"[+] uploading file")
        self.PutFile(download_url, headers_send, str(file_path))
        print(f"[+] file {file_name} successfully uploaded to {file_path}")

    def DownloadScript(self):
        headers = {'Accept' : 'application/json', 'Authorization' : self.config['OAuth']}
        list_of_data = self.GetMetaData('/', headers=headers)
        path = '/'
        req = input()
        while req != "exit":
            if "cd" in req:
                trash, number =  req.split()
                if number == ".." or number == '../':
                    path = str(Path(path).parent)
                    list_of_data = self.GetMetaData(path, headers=headers)
                    req = input()
                    continue
                if int(number) >= len(list_of_data[0]):
                    print("Wrong dir number")
                    req = input()
                    continue
                path += list_of_data[0][int(number)]
                path += '/'
                list_of_data = self.GetMetaData(path, headers=headers)
                req = input()
                continue
            elif "get" in req:
                trash, number = req.split()
                if int(number) >= len(list_of_data[1]):
                    print("Wrong file number")
                    req = input()
                    continue
                path += list_of_data[1][int(number)][0]
                download_url = self.GetDownloadUrl(path, headers)
                print(f"[+] Downloading file {Path(path).name} from {Path(path).stem}")
                print("[+] Processing...")
                file_name = self.CreateFileFromUrl(download_url, list_of_data[1][int(number)][0])
                print(f"[+] File {file_name} downloaded successfully")
                path = str(Path(path).parent)
                list_of_data = self.GetMetaData(path, headers=headers)
            else:
                print("Wrong command")
                req = input()
                continue
            req = input()
    