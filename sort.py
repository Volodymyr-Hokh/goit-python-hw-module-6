import json
import re
import shutil
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



# Some containers to write results
images = []
video = []
documents = []
audio = []
archives = []
all_extensions = set()
unfamiliar_extensions = set()


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

    global images, video, documents, audio, archives, all_extensions, unfamiliar_extensions



    main_folder_path = Path(sys.argv[1])

    if not is_recursive:
        for folder in folder_names:
            folder_path = path.joinpath(folder)
            folder_path.mkdir(exist_ok=True)

    for item in path.iterdir():

        new_name = normalize(item.name)

        if item.is_dir():
            if item.name in folder_names:
                continue

            sort_files(item, is_recursive=True)

            if len(list(item.iterdir())) == 0:
                item.rmdir()


        file_extension = item.suffix[1:].upper()

        if file_extension:
            all_extensions.add(file_extension)

        if file_extension in EXTENSIONS['images']:
            new_path = main_folder_path.joinpath('images', new_name)
            item.rename(new_path)
            images.append(new_name)

        elif file_extension in EXTENSIONS['video']:
            new_path = main_folder_path.joinpath('video', new_name)
            item.rename(new_path)
            video.append(new_name)
                        
        elif file_extension in EXTENSIONS['documents']:
            new_path = main_folder_path.joinpath('documents', new_name)
            item.rename(new_path)
            documents.append(new_name)
                                    
        elif file_extension in EXTENSIONS['audio']:
            new_path = main_folder_path.joinpath('audio', new_name)
            item.rename(new_path)
            audio.append(new_name)
            
                                                
        elif file_extension in EXTENSIONS['archives']:
            archive_name = normalize(item.name).split('.')[0]
            new_path = main_folder_path.joinpath('archives', archive_name)
            shutil.unpack_archive(item, new_path)
            item.unlink()
            archives.append(new_name)

        else:
            if file_extension:
                unfamiliar_extensions.add(file_extension)


        results = {
            'Sorted folder': path.name,
            'Results': {
                "Formats": {
                    'images': images,
                    'video': video,
                    'documents': documents,
                    'audio': audio,
                    'archives': archives,
                },
                'Familiar extensions': list(all_extensions - unfamiliar_extensions),
                'Unfamiliar extensions': list(unfamiliar_extensions),
            }
        }

        with open('results.json', 'w') as file:
            json.dump(results, file, indent=4, ensure_ascii=False)

    

def rename_all_folders(path: Path):
    
    for item in path.iterdir():

        if item.is_dir():
            
            new_name = normalize(item.name)

            if item.name in folder_names:
                continue

            rename_all_folders(item)
            new_dir = item.parent.joinpath(new_name)
            item.rename(new_dir)


def main():
    
    if len(sys.argv) < 2:
        raise ValueError('Please enter the path to the folder you want to sort.')

    path = Path(sys.argv[1])

    if not path.is_dir():
        raise ValueError('Folder does not exists. Please check the path and try again.')

    sort_files(path)
    rename_all_folders(path)
    

if __name__ == '__main__':
    main()
