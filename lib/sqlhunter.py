import requests, re, json, time, os, sys

def typewrite(message):
    for character in message:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.0000005)
    
    print(colors.reset)

class colors:
    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    magenta = "\033[1;35m"
    cyan = "\033[1;36m"
    white = "\033[1;37m"
    reset = "\033[0m"
    bold = "\033[;1m"
    verybold = "\033[;1;4m"
    
    class gradients:
        redblue = "\033[1;31;44m"
        redgreen = "\033[1;31;42m"
        redyellow = "\033[1;31;43m"
        redmagenta = "\033[1;31;45m"
        redcyan = "\033[1;31;46m"
        bluegreen = "\033[1;34;42m"
        blueyellow = "\033[1;34;43m"
        bluemagenta = "\033[1;34;45m"
        bluecyan = "\033[1;34;46m"
        greenyellow = "\033[1;32;43m"
        greenmagenta = "\033[1;32;45m"
        greencyan = "\033[1;32;46m"
        yellowmagenta = "\033[1;33;45m"
        yellowcyan = "\033[1;33;46m"
        magentacyan = "\033[1;35;46m"
        redwhite = "\033[1;31;47m"

def GetURLsFromDork(dork):
    results = []
    page = 0

    while page <= 5:
        try:
            page += 1
            print(colors.blue + "[*] Scanning page: " + colors.reset + str(page))
            r = requests.get("https://www.google.com/search?q=" + dork + "&start=" + str(page))

            if "recaptcha" in r.text:
                print(colors.red + "[!] Recaptcha detected!" + colors.reset)
                page = 6
                break

            if "google" in r.text:
                # Ignore the result with google in it
                print(colors.red + "[!] Ignoring google links!" + colors.reset)
                continue

            urls = re.findall(r"(https:\/\/[a-zA-Z0-9_\-\.\/\?&=]+)", r.text)
            for url in urls:
                if url not in results:
                    print(colors.blue + "[*] Found URL: " + colors.reset + url)
                    results.append(url)

        except KeyboardInterrupt:
            # Stop the scan, this function is called from another function which is in a while loop
            print(colors.red + "[!] Stopping scan..." + colors.reset)
            break

        except Exception as e:
            break

    return results

def start():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    banner = open("./lib/banner.txt", "r").read()
    typewrite(colors.red + banner)

    print(colors.blue + """
 ____   ___  _     _   _             _            
/ ___| / _ \| |   | | | |_   _ _ __ | |_ ___ _ __ 
\___ \| | | | |   | |_| | | | | '_ \| __/ _ \ '__|
 ___) | |_| | |___|  _  | |_| | | | | ||  __/ |   
|____/ \__\_\_____|_| |_|\__,_|_| |_|\__\___|_|                                                  
""" + colors.reset)
    
    print(colors.red + "SQLHunter v1.0.0" + colors.reset + "\n")
    print(colors.blue + "This tool will scan a URL for SQL injection vulnerabilities." + colors.reset)
    print(colors.blue + "It will test all parameters found in the URL for SQL injection." + colors.reset)
    print(colors.blue + "If a parameter is vulnerable, it will be marked as such." + colors.reset)
    print(colors.blue + "You can save the scan results to a file." + colors.reset)
    print("")
    print(colors.yellow + "Made by GitHub: iuseyahoo, discord: altorx" + colors.reset)
    # version
    print(colors.yellow + "Version: 1.0.4" + colors.reset)

    while True:
        print("\n[1] - Manual URL entry     [2] - Gather URLs from dork     [3] - Exit")
        try:
            option = input(colors.blue + "\n[*] Enter a number: " + colors.reset)
            if option == "1":

                url = input(colors.blue + "\n[*] Enter URL: " + colors.reset)
                if url == "":
                    print(colors.red + "[!] URL cannot be empty!" + colors.reset)
                    continue

                if not url.startswith("http"):
                    url = "http://" + url

                found_params = []
                params = re.findall(r"\?([a-zA-Z0-9_]+)\=", url)
                for param in params:
                    if param not in found_params:
                        found_params.append(param)

                if len(found_params) == 0:
                    print(colors.red + "[!] No parameters found!" + colors.reset)
                    continue

                print(colors.blue + "[*] Found parameters: " + colors.reset + str(found_params) + "\n")
                for param in found_params:
                    print(colors.blue + "[*] Testing parameter: " + colors.reset + param)
                    payload = url.replace(param + "=", param + "=1\'")
                    r = requests.get(payload)
                    if "error in your SQL syntax" in r.text:
                        print(colors.green + "[+] Parameter " + param + " seems to be vulnerable!" + colors.reset)
                    else:
                        print(colors.red + "[-] Parameter " + param + " does not seem to be vulnerable!" + colors.reset)

                dataToPossiblySave = {
                    "url": url,
                    "params": found_params
                }

                save = input(colors.blue + "\n[*] Do you want to save this scan? (y/n): " + colors.reset)
                if save.lower() == "y":
                    fileName = input(colors.blue + "[*] Enter filename: " + colors.reset)
                    if fileName == "":
                        print(colors.red + "[!] Filename cannot be empty!" + colors.reset)
                        continue

                    if not fileName.endswith(".json"):
                        fileName += ".json"

                    if os.path.isfile(fileName):
                        print(colors.red + "[!] File already exists!" + colors.reset)
                        continue

                    with open(fileName, "w") as f:
                        f.write(json.dumps(dataToPossiblySave))
                        print(colors.green + "[+] File saved!" + colors.reset)
                else:
                    print(colors.red + "[!] Scan not saved!" + colors.reset)
                    continue

                domainname = re.findall(r"([a-zA-Z0-9_\-\.]+)\.([a-zA-Z0-9_\-\.]+)", url)
                print("Scan finished for " + colors.green + domainname[0][0] + "." + domainname[0][1] + colors.reset + "!")
                print("You can find the results in " + colors.green + fileName + colors.reset + "!")
            elif option == "2":
                # dorklist = ["inurl:index.php?id=", "site:.gov filetype:php ?id="]
                dorklist = open("./dorks.txt", "r").readlines()
                dorksitesfound = []

                for dork in dorklist:
                    print(colors.blue + "[*] Gathering URLs from dork: " + colors.reset + dork)
                    urls = GetURLsFromDork(dork)
                    
                    if len(urls) == 0:
                        print(colors.red + "[!] Stopping scan..." + colors.reset)
                        break

                    for url in urls:
                        if url not in dorksitesfound:
                            print(colors.blue + "[*] Found URL: " + colors.reset + url)
                            dorksitesfound.append(url)
                        else:
                            print(colors.blue + "[*] URL already found: " + colors.reset + url)
                            continue

                print(colors.blue + "[*] Found " + str(len(dorksitesfound)) + " URLs!" + colors.reset)

                for url in dorksitesfound:
                    found_params = []

                    print(colors.blue + "[*] Testing URL: " + colors.reset + url)
                    params = re.findall(r"\?([a-zA-Z0-9_]+)\=", url)
                    for param in params:
                        if param not in found_params:
                            found_params.append(param)

                    if len(found_params) == 0:
                        print(colors.red + "[!] No parameters found!" + colors.reset)
                        continue

                    print(colors.blue + "[*] Found parameters: " + colors.reset + str(found_params) + "\n")
                    
                    for param in found_params:
                        print(colors.blue + "[*] Testing parameter: " + colors.reset + param)
                        payload = url.replace(param + "=", param + "=1\'")
                        r = requests.get(payload)
                        if "error in your SQL syntax" in r.text:
                            print(colors.green + "[+] Parameter " + param + " seems to be vulnerable!" + colors.reset)
                        else:
                            print(colors.red + "[-] Parameter " + param + " does not seem to be vulnerable!" + colors.reset)    
            elif option == "3":
                print(colors.red + "[!] Exiting..." + colors.reset)
                sys.exit(0)
            else:
                print(colors.red + "[!] Invalid option!" + colors.reset)
                continue

        except Exception as e:
            print(colors.red + "[!] Error: " + str(e) + colors.reset)
            continue
