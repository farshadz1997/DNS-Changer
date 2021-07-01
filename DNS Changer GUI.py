import shutil
import sys
import os
import json
import threading
from tkinter import ttk, messagebox as msg, filedialog
from tkinter import *
import psutil
class Application:
    def __init__(self, master, DNS: dict, connections: list):
        self.dns = DNS
        self.master = master
        self.connections = connections
        self.providers = [provider for provider in self.dns.keys()]
        Application.GUI(self)
        
    def GUI(self):
        main_label = Label(self.master, text = "DNS Changer", font = ("Halvetica", 18, "bold")).place(x = 135, y = 10)
        # choose provider
        provider_label = Label(self.master, text = "Choose provider:", font = ("Halvetica", 11)).place(x = 10, y = 70)
        provider_combobox = ttk.Combobox(self.master, values = self.providers, state = "readonly")
        provider_combobox.set("Choose a provider")
        provider_combobox.place(x = 145, y = 72, width = 142)
        # Connections
        connections_label = Label(self.master, text = "Connections:", font = ("Halvetica", 11)).place(x = 10, y = 110)
        connections_combobox = ttk.Combobox(self.master, values = self.connections, state = "readonly")
        connections_combobox.set("Ethernet")
        connections_combobox.place(x = 145, y = 112, width = 142)
        # Primary address
        primary_address_label = Label(self.master, text = "Primary address:", font = ("Halvetica", 11)).place(x = 10, y = 150)
        self.primary_address_entry = ttk.Entry(self.master, state = "disabled")
        self.primary_address_entry.place(x = 145, y = 152, width = 142)
        # Secondary address
        secondary_address_label = Label(self.master, text = "Secondary address:", font = ("Halvetica", 11)).place(x = 10, y = 190)
        self.secondary_address_entry = ttk.Entry(self.master, state = "disabled") 
        self.secondary_address_entry.place(x = 145, y = 192, width = 142)
        # Buttons
        self.delete_btn = ttk.Button(self.master, text = "Delete")
        self.delete_btn.place(x = 90, y = 260)
        self.set_btn = ttk.Button(self.master, text = "Set") 
        self.set_btn.place(x = 170, y = 260)
        self.add_btn = ttk.Button(self.master, text = "Add", command = self.Toplevel)
        self.add_btn.place(x = 250, y = 260)
        self.edit_btn = ttk.Button(self.master, text = "Edit")
        self.edit_btn.place(x = 130, y = 290)
        self.save_btn = ttk.Button(self.master, text = "Save")
        self.save_btn.place(x = 210, y = 290)

    # Toplevel window for adding
    def Toplevel(self):
        self.toplevel = Toplevel()
        self.toplevel.title("Add DNS")
        self.toplevel.geometry("270x200")
        self.toplevel.resizable(False, False)
        # Provider
        provider_label = Label(self.toplevel, text = "Provider:", font = ("Halvetica", 11)).place(x = 10, y = 20)
        provider_entry = ttk.Entry(self.toplevel)
        provider_entry.place(x = 85, y = 22)
        # Addresses
        address1 = Label(self.toplevel, text = "Address 1:", font = ("Halvetica", 11)).place(x = 10, y = 60)
        address1_entry = ttk.Entry(self.toplevel)
        address1_entry.place(x = 85, y = 62)
        address2 = Label(self.toplevel, text = "Address 2:", font = ("Halvetica", 11)).place(x = 10, y = 100)
        address2_entry = ttk.Entry(self.toplevel)
        address2_entry.place(x = 85, y = 102)
        # Submit
        submit_btn = ttk.Button(self.toplevel, text = "Submit")
        submit_btn.place(x = 105, y = 145, width = 70)
        
        
    def Execute(self):
        pass
    
def main():
    root = Tk()
    root.title("DNS Changer")
    root.geometry("400x400")
    root.resizable(False, False)
    addrs = psutil.net_if_addrs()
    connections = list(addrs.keys())
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
    finally:
        DNSs = json.load(open("DNS Addresses.json", "r"))
    app = Application(root, DNSs, connections)
    root.mainloop()
    
if __name__ == "__main__":
    main()