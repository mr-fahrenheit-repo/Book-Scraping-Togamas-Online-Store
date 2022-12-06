import re
import colorama

# Removing blank spaces from text
def striping(text):
    text = text.split()
    return text
    
# removing other than digit character
def number_plain(text):
    text = re.sub(r'[-()\"#/@;:<>{}`+=~|*.!?,]','', text).strip()
    text = text.replace("Rp", "")
    text = int(text)
    return text

# removing other than alphabet
def clean_text(text):
    text = re.sub(r'[-()\"#/@;:<>{}`+=~|*.!?,]','', text).strip()
    return text
    
# Removing unknown characters
def remove_unknown(text):
    text = text.encode('ascii', 'ignore')
    text = text.decode('utf-8')
    text = text.strip()
    return text

# Finding the link in string
def find_link(text):
    link = text
    try:
        link = link[link.find('http'):link.find('.jpg') + 4]
    except:
        link = link[link.find('http'):link.find('.png') + 4]
    return link

# Progress bar render
def progress_bar(progress, total, color=colorama.Fore.YELLOW):
    percent = 100 * (progress / float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(color+f"\r|{bar}| {percent:.2f}%", end="\r")
    if progress == total:
        print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")