from typing import Dict

button_data = {"video_id": "", "resolution": "", "url": "", "title": "", "author": ""}

def to_dict(string: str) -> Dict:
    if len(string.split()) != 1:
        dict_values = string.split(" <...> ")
        dictionary = {
            "video_id": dict_values[0], 
            "resolution": dict_values[1],  
        }
    else:
        dictionary = {
            "video_id": string.split()[0], 
            "resolution": "", 
            "title": "",
            "author": ""
        }
    return dictionary


def to_str(data: Dict) -> str:
    return " <...> ".join(data.values())
