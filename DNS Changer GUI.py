import json
import os, ctypes
import re
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import *
import psutil
from urllib.request import urlopen

class Application:
    def __init__(self, master, DNS: dict, connections: list):
        self.dns = DNS
        self.master = master
        self.connections = connections
        self.providers = [provider for provider in self.dns.keys()]
        self.vcmd = (master.register(self.validate))
        Application.GUI(self)
        try:
            is_admin = os.getuid() == 0 # this is for unix OS onlly and the in attribute exception is for windows
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() == 1
        if not is_admin:
            msg.showwarning("Admin privliage", "Run the program as administrator")
        self.Check_ip()
    
    # main window interface    
    def GUI(self):
        main_label = Label(self.master, text = "DNS Changer", fg = 'red', font = ("Bahnschrift", 18, "bold")).place(x = 135, y = 10)
        # choose provider
        provider_label = Label(self.master, text = "Providers:", font = ("Halvetica", 11)).place(x = 10, y = 70)
        self.provider_var = StringVar()
        self.provider_combobox = ttk.Combobox(self.master, textvariable = self.provider_var, values = self.providers, state = "readonly")
        self.provider_combobox.set("Choose a provider")
        self.provider_combobox.place(x = 145, y = 72, width = 142)
        self.provider_combobox.bind("<<ComboboxSelected>>", self.provider_changes)
        # Connections
        connections_label = Label(self.master, text = "Connections:", font = ("Halvetica", 11)).place(x = 10, y = 110)
        self.connections_combobox = ttk.Combobox(self.master, values = self.connections, state = "readonly")
        self.connections_combobox.set("Ethernet")
        self.connections_combobox.place(x = 145, y = 112, width = 142)
        # Primary address
        primary_address_label = Label(self.master, text = "Primary address:", font = ("Halvetica", 11)).place(x = 10, y = 150)
        self.primary_address_var = StringVar()
        self.primary_address_entry = ttk.Entry(self.master, textvariable = self.primary_address_var, state = "disabled", validate = 'all',
                                                validatecommand = (self.vcmd, '%P', '%S', '%i'))
        self.primary_address_entry.place(x = 145, y = 152, width = 142)
        # Secondary address
        secondary_address_label = Label(self.master, text = "Secondary address:", font = ("Halvetica", 11)).place(x = 10, y = 190)
        self.secondary_address_var = StringVar()
        self.secondary_address_entry = ttk.Entry(self.master, textvariable = self.secondary_address_var, state = "disabled", validate = 'all',
                                                  validatecommand = (self.vcmd, '%P', '%S', '%i')) 
        self.secondary_address_entry.place(x = 145, y = 192, width = 142)
        # Delete button
        self.delete_icon = PhotoImage(file = r'Icons/delete.png')
        self.delete_btn = ttk.Button(self.master, text = "Delete", image = self.delete_icon, compound = LEFT, command = self.Delete)
        self.delete_btn.place(x = 295, y = 70, width = 77, height = 25)
        # Edit/Save button
        self.edit_icon = PhotoImage(file = r'Icons/edit.png')
        self.save_icon = PhotoImage(file = r'Icons/save.png')
        self.edit_btn = ttk.Button(self.master, text = "Edit", image = self.edit_icon, compound = LEFT, command = lambda :self.Edit_and_Save(edit = True))
        self.edit_btn.place(x = 292, y = 150, width = 79, height = 25)
        # Set button
        self.set_icon = PhotoImage(file = r'Icons/set.png')
        self.set_btn = ttk.Button(self.master, text = "Set", image = self.set_icon, compound = LEFT, command = self.Execute) 
        self.set_btn.place(x = 250, y = 245, width = 77, height = 25)
        # Reset button
        self.reset_icon = PhotoImage(file = r'Icons/reset.png')
        self.reset_btn =ttk.Button(self.master, text = "Reset", image = self.reset_icon, compound = LEFT, command = self.Reset)
        self.reset_btn.place(x = 250, y = 280, width = 77, height = 25)
        # Add button
        self.add_icon = PhotoImage(file = r'Icons/add.png')
        self.add_btn = ttk.Button(self.master, text = 'Add', image = self.add_icon, compound = LEFT, command = self.Toplevel)
        self.add_btn.place(x = 250, y = 315, width = 77, height = 25)
        # Refresh button
        self.refresh_icon = PhotoImage(file = r'Icons/refresh.png')
        self.refresh_btn = ttk.Button(self.master, text = 'Refresh', image = self.refresh_icon, compound = LEFT, command = self.Check_ip)
        self.refresh_btn.place(x = 250, y = 350, width = 77, height = 25)
        # labelframe
        self.labelframe = LabelFrame(self.master, background = 'black', relief = 'sunken').place(x = 10, y = 235, width = 220, height = 160)
        self.ip_label = Label(self.labelframe, text = 'IP:',bg = 'black', fg = 'white', font = ('Bahnschrift', 11)).place(x = 15, y = 242)
        self.ip = Label(self.labelframe,bg = 'black', font = ('Bahnschrift', 11))
        self.ip.place(x = 80, y = 242)
        self.country_label = Label(self.labelframe, text = 'Country:', bg = 'black', fg = 'white', font = ('Bahnschrift', 11)).place(x = 15, y = 272)
        self.country = Label(self.labelframe, bg = 'black', font = ('Bahnschrift', 11))
        self.country.place(x = 80, y = 272)
        self.region_label = Label(self.labelframe, text = 'Region:', bg = 'black', fg = 'white', font = ('Bahnschrift', 11)).place(x = 15, y = 302)
        self.region = Label(self.labelframe, bg = 'black', font = ('Bahnschrift', 11))
        self.region.place(x = 80, y = 302)
        self.city_label = Label(self.labelframe, text = 'City:', bg = 'black', fg = 'white', font = ('Bahnschrift', 11)).place(x = 15, y = 332)
        self.city = Label(self.labelframe, bg = 'black', font = ('Bahnschrift', 11))
        self.city.place(x = 80, y = 332)
        self.location_label = Label(self.labelframe, text = 'Location:', bg = 'black', fg = 'white', font = ('Bahnschrift', 11)).place(x = 15, y = 362)
        self.location = Label(self.labelframe, bg = 'black', font = ('Bahnschrift', 11))
        self.location.place(x = 80, y = 362)

    # Toplevel window for adding
    def Toplevel(self):
        self.toplevel = Toplevel()
        self.add_btn['state'] = 'disabled'
        self.toplevel.bind('<Destroy>', self.addBtn_state)
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (400/2)
        y = (screen_height/2) - (400/2)
        self.toplevel.title("Add DNS")
        self.toplevel.geometry("270x200+%d+%d" % (x, y))
        self.toplevel.resizable(False, False)
        # Provider
        provider_label = Label(self.toplevel, text = "Provider:", font = ("Halvetica", 11)).place(x = 10, y = 20)
        self.provider_entry = ttk.Entry(self.toplevel)
        self.provider_entry.place(x = 85, y = 22)
        # Addresses
        address1 = Label(self.toplevel, text = "Address 1:", font = ("Halvetica", 11)).place(x = 10, y = 60)
        self.address1_entry = ttk.Entry(self.toplevel, validate = 'all', validatecommand = (self.vcmd, '%P', '%S', '%i'))
        self.address1_entry.place(x = 85, y = 62)
        address2 = Label(self.toplevel, text = "Address 2:", font = ("Halvetica", 11)).place(x = 10, y = 100)
        self.address2_entry = ttk.Entry(self.toplevel, validate = 'all', validatecommand = (self.vcmd, '%P', '%S', '%i'))
        self.address2_entry.place(x = 85, y = 102)
        # Submit
        self.submit_icon = PhotoImage(file = r'Icons/apply.png')
        submit_btn = ttk.Button(self.toplevel, text = "Apply", image = self.submit_icon, compound = LEFT, command = self.Add)
        submit_btn.place(x = 105, y = 145, width = 70)
          
    # check validation of user entries in dns fields
    def validate(self, P, S, i):
        if int(i) <= 14 and (str.isdigit(P) or P == "" or str.isdigit(S) or str(S) == "."):
            return True     
        else:
            return False
        
    # To change entrie fields when provider changes
    def provider_changes(self, event):
        self.primary_address_var.set(str(self.dns[self.provider_combobox.get()]["Primary Address"]))
        self.secondary_address_var.set(str(self.dns[self.provider_combobox.get()]["Secondary Address"]))
    
    # change add button state from disable to normal while add window closes
    def addBtn_state(self, event):
        self.add_btn['state'] = 'normal'
     
    # write new provider or delete in 'DNS Addresses.json'   
    def Write_on_DNS(self):
        with open('DNS Addresses.json', 'w') as file:
            file.write(json.dumps(self.dns, indent = 4))
    
    # check fields for adding dns        
    def Add(self):
        p = self.provider_entry.get()
        a1 = self.address1_entry.get()
        a2 = self.address2_entry.get()
        try:
            if not (re.search('[a-z]', p) or re.search('[A-Z]', p) or re.search('[0-9]', p)):
                msg.showerror("Error", "Please input valid name which contains alphabet or numbers.")
                return False
            elif a1 == "" or a2 == "":
                msg.showwarning("Warning", "Both DNS fields cannot be empty.")
                return False
        except Exception as e:
            msg.showerror("Error", e)
        else:
            self.dns.update({self.provider_entry.get():{"Primary Address": str(self.address1_entry.get()), "Secondary Address": str(self.address2_entry.get())}})       
            self.Write_on_DNS()
            self.provider_combobox['values'] = list(self.dns.keys())
            self.toplevel.destroy()
    
    # delete dns from json file
    def Delete(self):
        if not self.provider_combobox.get() == "Choose a provider":
            del self.dns[str(self.provider_combobox.get())]
            self.Write_on_DNS()
            self.provider_combobox['values'] = list(self.dns.keys())
            self.provider_combobox.set("Choose a provider")
            self.primary_address_var.set("")
            self.secondary_address_var.set("")
        else:
            msg.showerror("Wrong choice", "Choose a correct provider.")
     
    # edit and save dns addresses    
    def Edit_and_Save(self, edit:bool):
        if edit:
            if not self.provider_combobox.get() == "Choose a provider":
                self.primary_address_entry['state'] = 'normal'
                self.secondary_address_entry['state'] = 'normal'
                self.edit_btn.config(text = 'Save', image = self.save_icon, command = lambda: self.Edit_and_Save(edit = False))
            else:
                msg.showwarning('Wrong choice', 'first choose a provider for editing.')
        else:
            self.primary_address_entry['state'] = 'disabled'
            self.secondary_address_entry['state'] = 'disabled'
            self.dns.update({self.provider_combobox.get():{"Primary Address": str(self.primary_address_var.get()), "Secondary Address": str(self.secondary_address_var.get())}})
            self.Write_on_DNS()
            self.edit_btn.config(text = 'Edit', image = self.edit_icon, command = lambda: self.Edit_and_Save(edit = True))
    
    # set dns to connection  
    def Execute(self):
        if self.primary_address_var.get() != "" and self.secondary_address_entry.get() != "":
            try:
                if self.primary_address_entry.get() != "":
                    os.system(f"netsh interface ip set dns {str(self.connections_combobox.get())} static address={self.primary_address_var.get()}")
                if self.secondary_address_entry.get() != "":
                    os.system(f"netsh interface ip add dns {str(self.connections_combobox.get())} addr={self.secondary_address_entry.get()} index=2")
            except Exception as e:
                msg.showerror("Error", e)
            else:
                msg.showinfo("Done", f"The DNS has been changed to {self.provider_combobox.get()}")
        else:
            msg.showerror("Error", "Choose a valid provider or check DNS addresses.")
    
    # reset dns to default
    def Reset(self):
        try:
            os.system(f"netsh interface ip set dns {self.connections_combobox.get()} dhcp")
            msg.showinfo("Done", "The DNS provider has been reset to default")
        except Exception as e:
            msg.showerror("Error", e)
    
    # check ip details
    def Check_ip(self):
        try:
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)
            self.ip.config(text = data['ip'], fg = 'green')
            self.country.config(text = data['country'], fg = 'green')
            self.region.config(text = data['region'], fg = 'green')
            self.city.config(text = data['city'], fg = 'green')
            self.location.config(text = data['loc'], fg = 'green')
        except Exception as e:
            self.ip.config(fg = 'red', text = 'N/A')
            self.country.config(fg = 'red', text = 'N/A')
            self.region.config(fg = 'red', text = 'N/A')
            self.city.config(fg = 'red', text = 'N/A')
            self.location.config(fg = 'red', text = 'N/A')
            msg.showerror("Error", e)
                   
            
def main():
    root = Tk()
    root.title("DNS Changer")
    root.iconbitmap('Icons/dns.ico')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (400/2)
    y = (screen_height/2) - (400/2)
    root.geometry('400x400+%d+%d' % (x, y))
    root.resizable(False, False)
    connections = list((psutil.net_if_addrs()).keys())
    try:
        DNSs = json.load(open("DNS Addresses.json", "r"))
    except FileNotFoundError:
        with open("DNS Addresses.json", 'w') as file:
            file.write(json.dumps({
                "Google":{ # Provider
                    "Primary Address": "8.8.8.8", # First DNS address
                    "Secondary Address": "8.8.4.4" # Second DNS address
                    }
            }, indent=4))
    except json.JSONDecodeError as e:
        msg.showerror("json decoding error", e)
    finally:
        DNSs = json.load(open("DNS Addresses.json", "r"))
    app = Application(root, DNSs, connections)
    root.mainloop()
    
if __name__ == "__main__":
    main()