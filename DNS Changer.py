import shutil
import sys
import os
        
def main():
	try:
		adp = input("Write your connection name: ")
		if shutil.which("netsh"):
			print("<DNS Changer>")
			print("1. Google")
			print("2. Shecan")
			print("3. OpenDNS")
			print("4. Shecan + 185.55.225.25")
			print("5. 185.55.225.25 + 185.55.226.26")
			print("6. Custom")
			print("7. Reset to default")

			while True:
				choice = input("Select a provider [1-7]: ")
				if choice not in list(map(str, list(range(1, 7 + 1)))):
					continue
				choice = int(choice)
				break

			if choice == 1:
				provider = "Google"
				primaryAddress = "8.8.8.8"
				secondaryAddress = "8.8.4.4"
			elif choice == 2:
				provider = "Shecan"
				primaryAddress = "178.22.122.100"
				secondaryAddress = "185.51.200.2"
			elif choice == 3:
				provider = "OpenDNS"
				primaryAddress = "208.67.222.222"
				secondaryAddress = "208.67.220.220"
			elif choice == 4:
				provider = "Shecan + 185.55.225.25"
				primaryAddress = "178.22.122.100"
				secondaryAddress = "185.55.225.25"
			elif choice == 5:
				provider = "185.55.225.25 + 185.55.226.26"
				primaryAddress = "185.55.225.25"
				secondaryAddress = "185.55.226.26"
			elif choice == 6:
				primaryAddress = input("Enter address: ")
			elif choice == 7:
				pass

			if choice <= 6:
				a = execute("netsh interface ip set dns "+ adp + f" source = static address={primaryAddress}")
				if choice <= 5:
					b = execute("netsh interface ip add dns name=" + adp + f" addr={secondaryAddress} index=2")
				print("The DNS {0} has been changed to {1}".format("provider" if choice <= 5 else "address", provider if choice <= 5 else primaryAddress))
			else:
				execute("netsh interface ip set dns " + adp + " dhcp")
				print("The DNS provider has been reset to default")
		else:
			print("Command 'netsh' not found")
			os._exit(1)

	except (EOFError, KeyboardInterrupt):
		print()
		os._exit(0)

def execute(command):
	os.system(command)

if __name__ == "__main__":
	if sys.version_info.major == 3:
		main()
		input("press any key to continue...")
	else:
		print("Please run this script with python3")