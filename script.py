import APIClass
import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-u] FILE or [-d] FILE",
        description="Upload or Download file to your YandexDisk."
    )
    api = APIClass.API("config.json")
    parser.add_argument('-upload', '--upload', '-u', type=str, nargs='?', default="None")
    parser.add_argument('-download', '--download', '-d', type=str, nargs='?', default="None")
    if parser.parse_args().upload != "None":
        file_path = Path(parser.parse_args().upload)
        if file_path.exists() == False:
            print("No such file, try again")
        # file_name = file_path[file_path.rfind('/') + 1 :]
        file_name = str(file_path.name)
        req = input("type \"cd\" to got to choose the installation path or type the path\n")
        if req == "cd":
            disk_path = api.ChoosePath()
            api.UploadScript(file_path, file_name, disk_path)
        else:
            if api.CheckPathExistance(req):
                api.UploadScript(file_path, file_name, req)
            else:
                api.CreateNewDirectory(req)
                api.UploadScript(file_path, file_name, req)
    if parser.parse_args().download != "None":
        api.DownloadScript()
    if parser.parse_args().download == "None" and parser.parse_args().upload == "None":
        parser.print_help()
