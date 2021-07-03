import json
import threading
import os, ctypes
import sys
import shutil
from tkinter import ttk, filedialog
from tkinter import messagebox as msg
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
        self.primary_address_entry = ttk.Entry(self.master, textvariable = self.primary_address_var, state = "disabled")
        self.primary_address_entry.place(x = 145, y = 152, width = 142)
        # Secondary address
        secondary_address_label = Label(self.master, text = "Secondary address:", font = ("Halvetica", 11)).place(x = 10, y = 190)
        self.secondary_address_var = StringVar()
        self.secondary_address_entry = ttk.Entry(self.master, textvariable = self.secondary_address_var, state = "disabled") 
        self.secondary_address_entry.place(x = 145, y = 192, width = 142)
        # Buttons
        self.delete_btn = ttk.Button(self.master, text = "X", command = self.Delete)
        self.delete_btn.place(x = 295, y = 70, width = 25)
        self.set_btn = ttk.Button(self.master, text = "Set", command = self.Execute) 
        self.set_btn.place(x = 170, y = 260)
        self.add_btn = ttk.Button(self.master, text = "Add", command = self.Toplevel)
        self.add_btn.place(x = 250, y = 260)
        self.edit_btn = ttk.Button(self.master, text = "E", command = self.Edit)
        self.edit_btn.place(x = 292, y = 150, width = 25)
        self.save_btn = ttk.Button(self.master, text = "S", command = self.Save, state = DISABLED)
        self.save_btn.place(x = 292, y = 190, width = 25)
        self.reset_btn =ttk.Button(self.master, text = "Reset", command = self.Reset)
        self.reset_btn.place(x = 90, y = 260)

    # Toplevel window for adding
    def Toplevel(self):
        self.toplevel = Toplevel()
        self.add_btn.state(['disabled'])
        self.toplevel.bind('<Destroy>', self.addBtn_state)
        self.toplevel.title("Add DNS")
        self.toplevel.geometry("270x200")
        self.toplevel.resizable(False, False)
        # Provider
        provider_label = Label(self.toplevel, text = "Provider:", font = ("Halvetica", 11)).place(x = 10, y = 20)
        self.provider_entry = ttk.Entry(self.toplevel)
        self.provider_entry.place(x = 85, y = 22)
        # Addresses
        address1 = Label(self.toplevel, text = "Address 1:", font = ("Halvetica", 11)).place(x = 10, y = 60)
        self.address1_entry = ttk.Entry(self.toplevel)
        self.address1_entry.place(x = 85, y = 62)
        address2 = Label(self.toplevel, text = "Address 2:", font = ("Halvetica", 11)).place(x = 10, y = 100)
        self.address2_entry = ttk.Entry(self.toplevel)
        self.address2_entry.place(x = 85, y = 102)
        # Submit
        submit_btn = ttk.Button(self.toplevel, text = "Submit", command = self.Add)
        submit_btn.place(x = 105, y = 145, width = 70)
    
    # For changing entries fields when provider changes
    def provider_changes(self, event):
        self.primary_address_var.set(str(self.dns[self.provider_combobox.get()]["Primary Address"]))
        self.secondary_address_var.set(str(self.dns[self.provider_combobox.get()]["Secondary Address"]))
        
    def addBtn_state(self, event):
        self.add_btn['state'] = 'normal'
        
    def Write_on_DNS(self):
        with open('DNS Addresses.json', 'w') as file:
            file.write(json.dumps(self.dns, indent = 4))
            
    def Add(self): #! need to be complete for validation
        try:
            if self.provider_entry.get() == None:
                msg.showerror("Error", "Provider can not be empty!")
            else:
                self.dns.update({self.provider_entry.get():{"Primary Address": str(self.address1_entry.get()), "Secondary Address": str(self.address2_entry.get())}})       
        except Exception:
            pass
        except KeyError: 
            pass
        else:
            self.Write_on_DNS()
            self.provider_combobox['values'] = list(self.dns.keys())
            self.toplevel.destroy()
    
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
            
    def Edit(self):
        if not self.provider_combobox.get() == "Choose a provider":
            self.edit_btn['state'] = 'disabled'
            self.primary_address_entry['state'] = 'normal'
            self.secondary_address_entry['state'] = 'normal'
            self.save_btn['state'] = 'normal'
        else:
            msg.showwarning('Wrong choice', 'first choose a provider for editing.')
            
    def Save(self):
        self.save_btn['state'] = 'disabled'
        self.edit_btn['state'] = 'normal'
        self.primary_address_entry['state'] = 'disabled'
        self.secondary_address_entry['state'] = 'disabled'
        self.dns.update({self.provider_combobox.get():{"Primary Address": str(self.primary_address_var.get()), "Secondary Address": str(self.secondary_address_var.get())}})
        self.Write_on_DNS()
        
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
    
    def Reset(self):
        try:
            os.system(f"netsh interface ip set dns {self.connections_combobox.get()} dhcp")
            msg.showinfo("Done", "The DNS provider has been reset to default")
        except Exception as e:
            msg.showerror("Error", e)
            
            
def main():
    root = Tk()
    root.title("DNS Changer")
    root.geometry("400x400")
    root.resizable(False, False)
    connections = list((psutil.net_if_addrs()).keys())
    try:
        DNSs = json.load(open("DNS Addresses.json", "r"))
        # is_admin = os.getuid() == 0
    except FileNotFoundError:
        with open("DNS Addresses.json", 'w') as file:
            file.write(json.dumps({
                "Google":{ # Provider
                    "Primary Address": "8.8.8.8", # First DNS address
                    "Secondary Address": "8.8.4.4" # Second DNS address
                    }
            }, indent=4))
    # except AttributeError:
    #     is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    #     msg.showwarning("Admin privliage", "Run the program as administrator")
    finally:
        DNSs = json.load(open("DNS Addresses.json", "r"))
    app = Application(root, DNSs, connections)
    root.mainloop()
    
if __name__ == "__main__":
    main()