import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from tkinter import messagebox
import time
import threading
import webbrowser

root = tk.Tk()
root.resizable(False,False)
root.iconbitmap("icon.ico")
root.geometry("260x350")
root.title("搜索達人")
label = tk.Label(root, text="地區前十搜索排行榜", font=("Arial", 20))
label.grid(row=0, column=0)
text = tk.Text(root, font=("Arial", 14), height=10 ,width=20)
text.grid(row=1, column=0)

regions = {"台灣": "TW", "美國": "US", "日本": "JP" ,"土耳其":"TR","丹麥":"DK","巴西":"BR","比利時":"BE","以色列":"IL","澳洲":"AU","加拿大":"CA","匈牙利":"HU","印尼":"ID","印度":"IN"} 
region_var = tk.StringVar() 
region_var.set("台灣")  
listbox = tk.Listbox(root, height=5)
scrollbar = tk.Scrollbar(root, command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
for region in regions.keys():
    listbox.insert(tk.END, region)
def on_select(event):
    region_var.set(listbox.get(listbox.curselection()))
    listbox.grid_forget()
    scrollbar.grid_forget()
    region_button.grid(row=3,column=0)
    threading.Thread(target=update_data).start()  

listbox.bind("<<ListboxSelect>>", on_select)
def on_click():
    region_button.grid_forget()
    listbox.grid(row=3, column=0, sticky="ew")
    scrollbar.grid(row=3, column=1, sticky="ns")

region_button = tk.Button(root, text="選擇地區", command=on_click)
region_button.grid(row=3, column=0)

progressbar = ttk.Progressbar(root, length=200, mode='indeterminate')
progressbar.grid(row=5, column=0, pady=10)
progressbar.grid_remove()
hint_label = tk.Label(root, text="提示:雙擊文字可以開啟瀏覽器查詢", font=("Arial", 8))
hint_label.grid(row=4, column=0)

def callback(event):
    tags = event.widget.tag_names(tk.CURRENT)
    if len(tags) > 1:
        webbrowser.open_new("https://www.google.com/search?q=" + tags[1])

def update_data():
    current_time = time.time()
    region_button.grid_remove()
    progressbar.grid()
    progressbar.start() 
    options = Options()
    options.add_argument("--headless")
    url = f'https://trends.google.com.tw/trends/trendingsearches/daily?geo={regions[region_var.get()]}&hl=zh-TW'
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
    driver.get(url)

    wait = WebDriverWait(driver, 10) 
    title_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'title')))
    lst = []
    for div in title_divs:
        soup = BeautifulSoup(div.get_attribute('innerHTML'), 'html.parser') 
        a_tags = soup.find_all('a')
        for a in a_tags:
            lst.append(a.text)
    driver.quit()
    clean_lst = [item.strip() for item in lst]
    text.delete(1.0, tk.END)
    for item in clean_lst[:10]:
        text.insert(tk.END, item + "\n")
        text.tag_add(item, "end-2l", "end-1l")
        text.tag_bind(item, "<Button-1>", callback)
    update_data.last_update = current_time
    update_data.last_region = region_var.get()
    progressbar.stop()  
    progressbar.grid_remove()
    region_button.grid()

def change_cursor(event):
    text.config(cursor="hand2")

def return_cursor(event):
    text.config(cursor="")

text.bind("<Enter>", change_cursor)
text.bind("<Leave>", return_cursor)

update_data.last_update = 0
update_data()

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()