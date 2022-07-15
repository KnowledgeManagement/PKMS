import APIClass
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-u] FILE or [-d] FILE",
        description="Upload or Download file to your YandexDisk."
    )
    api = APIClass.API("config.json")
    parser.add_argument('-upload', '--upload', '-u', type=str, nargs='?', default="none")
    parser.add_argument('-download', '--download', '-d', type=str, nargs='?', default="none")
    if parser.parse_args().upload != "none":
        file_path = parser.parse_args().upload
        file_name = file_path[file_path.rfind('/') + 1 :]
        api.UploadScript(file_path, file_name, '/test')
    if parser.parse_args().download != "none":
        api.DownloadScript()
    if parser.parse_args().download == "none" and parser.parse_args().upload == "none":
        parser.print_help()