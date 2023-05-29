import re





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



