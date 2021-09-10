import requests, bs4, os, shutil
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import ttk

window = tk.Tk()

window.title("Manga Downloader")
window.minsize(600,400)


'''PARTE DO WEB SCRAPING'''
def manga(s):
    
    # Open the Website
    res = requests.get(f'https://nhentai.net/g/{s}/')
    
    if res.ok:
    
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Check the number of pages
        pages = soup.select('.tag-container')[-2]

        area_pgs = False
        num_pgs = ''

        for i in pages.text:
            if i != '\t' and i != '\n':

                if area_pgs:
                    num_pgs += i

                if i == ':':
                    area_pgs = True
        
        # Checks if there are too many pages and asks if you want to continue
        if int(num_pgs) <= 25:
            download = '1'
        else:
            download = (input(f'This manga have {num_pgs} pages\Enter 1 to continue or 2 to stop: '))
            
            
        if download == '1':
            
            # Main part
            for num in range(1, int(num_pgs)+1):

                # Open the file
                f = open(f'pg{num}.jpg', 'wb')

                # Access image with good resolution
                res_img = requests.get(f'https://nhentai.net/g/{s}/{num}')
                soup_img = bs4.BeautifulSoup(res_img.text, 'lxml')

                # Get image link
                img = soup_img.select('img')[1]
                area_img = False
                img_source = ''

                for i in str(img).split()[2]:

                    if i == '"':
                        area_img = False

                    if area_img:
                        img_source += i

                    if i == '"':
                        area_img = True

                # Write the image in the file
                image_link = requests.get(img_source)
                f.write(image_link.content)        
                f.close()

                # Get manga name
                area_nm = True
                nome_hnt = '\\'

                for i in soup.select("title")[0].text:

                    if i == '»':
                        area_nm = False

                    if area_nm:
                        if i in ['”', '"', '*', ':', '<', '>', '?', '/', '\\', '|']:
                            continue
                        else:
                            nome_hnt += i

                nome_hnt = nome_hnt[:-1]

                # Create a manga folder
                global path
                try:
                    os.mkdir(path + nome_hnt)
                except FileExistsError:
                    pass

                # Move the image to the manga folder
                shutil.move(str(os.getcwd()) + f'\\pg{num}.jpg', path + nome_hnt)
                
                numberPages = ttk.Label(window, text = f'{nome_hnt[1:]} downloaded succesfully')
                numberPages.grid(column = 0, row = 4)
                
                print(f'{num}/{num_pgs}')

            print('\nDownload completed')
        
        else:
            print('\nDownload interrupted')
        
    else:
        print('The code does\'n exist')


'''BOTÕES DO TKINTER'''
def click():
    manga(name.get())

def choosePath():
    root = tk.Tk()
    root.withdraw()
    
    global path
    path = askdirectory()
    
    pathLabel.configure(text = path)


'''SAIR DO INTERPRETADOR QUANDO FECHAR A JANELA'''
def on_closing():
    quit()

# Choose dir button
path = str(os.getcwd())
pathButton = ttk.Button(window, text = "Choose directory", command = choosePath)
pathButton.grid(column = 0, row = 0)
pathLabel = ttk.Label(window, text = path)
pathLabel.grid(column = 1, row = 0)


# Label
label = ttk.Label(window, text = "Enter manga code")
label.grid(column = 0, row = 1)

# Text box
name = tk.StringVar()
nameEntered = ttk.Entry(window, width = 15, textvariable = name)
nameEntered.grid(column = 0, row = 2)
s = name.get()


# Download button
button = ttk.Button(window, text = "Download", command = click)
button.grid(column= 0, row = 3)

# 147852 manga with 6 pages for tests
# 298350 manga with a lot of pages for tests

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
