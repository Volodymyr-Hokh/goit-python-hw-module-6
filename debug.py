import re
import sys
from pathlib import Path



EXTENSIONS = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR'),
}

folder_names = EXTENSIONS.keys()


def normalize(name: str) -> str:

    cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    latin = ('a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l', 'm', 'n',
              'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'ts', 'ch', 'sh', 'sch', '', 'y', 
              '', 'e', 'yu', 'ya', 'je', 'i', 'ji', 'g')
    trans = {}
        
    for cyr, lat in zip(cyrillic, latin):
        trans[ord(cyr)] = lat
        trans[ord(cyr.upper())] = lat.title()

    translated_name = name.translate(trans)

    # Replace all characters except letters, numbers and '.' with '_'
    formatted_name = re.sub(r'[^a-zA-Z0-9.]', '_', translated_name)

    # Replace all '.' except the last one with '_'
    normalized_name = re.sub(r'\.(?=.*\.)', '_', formatted_name)

    return normalized_name


def sort_files(path: Path, is_recursive=False):

    main_folder_path = Path('D:\GitHub\goit-python-hw-module-6\TestRenameFolder')

    if not is_recursive:
        for folder in folder_names:
            folder_path = path.joinpath(folder)
            folder_path.mkdir(exist_ok=True)

    for item in path.iterdir():

        new_name = normalize(item.name)

        if item.is_dir():
            if item.name in folder_names:
                continue
            
            # new_dir = path.joinpath(new_name)
            # item.rename(new_dir)
            sort_files(item, is_recursive=True)

            if len(list(item.iterdir())) == 0:
                item.rmdir()


        file_extension = item.suffix[1:].upper()

        if file_extension in EXTENSIONS['images']:
            new_path = main_folder_path.joinpath('images', new_name)
            item.rename(new_path)

        elif file_extension in EXTENSIONS['video']:
            new_path = main_folder_path.joinpath('video', new_name)
            item.rename(new_path)
                        
        elif file_extension in EXTENSIONS['documents']:
            new_path = main_folder_path.joinpath('documents', new_name)
            item.rename(new_path)
                                    
        elif file_extension in EXTENSIONS['audio']:
            new_path = main_folder_path.joinpath('audio', new_name)
            item.rename(new_path)
                                                
        elif file_extension in EXTENSIONS['archives']:
            new_path = main_folder_path.joinpath('archives', new_name)
            item.rename(new_path)
    


def rename_all_folders(path):
    new_name = normalize(path.name)

    for item in path.iterdir():

        if item.is_dir():
            if item.name in folder_names:
                continue

            rename_all_folders(item)
            new_dir = item.parent.joinpath(new_name)
            item.rename(new_dir)


        

def main():
    
    path = Path('D:\GitHub\goit-python-hw-module-6\TestRenameFolder')


    rename_all_folders(path)
    

if __name__ == '__main__':
    main()
