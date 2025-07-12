# Chrome Cookie Hijacking: MFA Bypass, DPAPI, and EDR Blind Spots

## 🔍 Overview

This project demonstrates how Chrome browser cookies can be extracted and abused to hijack authenticated sessions—effectively bypassing MFA—using only local user access. It shows how attackers can extract, decrypt, and reuse cookies from a target system, and why AV/EDR solutions may not detect this behavior.

> **⚠️ Warning:** This project is for educational and defensive research purposes only.

---

## 🧠 What This Project Covers

* How Chrome stores session cookies using DPAPI encryption
* Techniques to extract encrypted cookie data using PowerShell
* Decrypting Chrome cookies using Python (`browser-cookie3`)
* Demonstrating real-world session hijacking with cookies (e.g., LinkedIn `li_at`)
* Why traditional MFA doesn’t protect against session hijacking
* Why AV/EDR often fails to detect cookie harvesting
* Detection strategies for blue teams

---

## 🛠️ File Structure

```
cookie-hijack-demo/
├── README.md                          ← You're here
├── powershell/
│   └── extract_cookie_paths.ps1       ← Locates and extracts cookie files
├── python/
│   └── decrypt_with_browser_cookie3.py← Extracts and decrypts cookies using DPAPI
├── samples/
│   └── example_cookie_output.txt      ← Sample cookies (obfuscated)
├── detection/
│   └── edr_detection_tips.md          ← Detection logic for blue teams
├── images/
│   └── mfa_cookie_bypass.png          ← Diagrams/screenshots (optional)
```

---

## 🔐 How Chrome Stores Cookies

Chrome saves cookies inside an SQLite database at:

```
%LOCALAPPDATA%\Google\Chrome\User Data\<Profile>\Network\Cookies
```

* The cookie value is stored in the `encrypted_value` column.
* Encrypted using **Windows DPAPI**, tied to the user profile.
* Cannot be reused on a different machine or user context.

---

## 📦 Tools Used

### 1. **PowerShell**

To locate cookies and other sensitive files:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\Google\Chrome\User Data\" -Recurse -Filter Cookies -ErrorAction SilentlyContinue
```

### 2. **browser-cookie3**

A Python tool to decrypt Chrome cookies using the current user context.

```bash
pip install browser-cookie3
python -c "import browser_cookie3; print(browser_cookie3.chrome(domain_name='linkedin.com'))"
```

---

## 🎯 Attack Flow Example

1. **User logs into LinkedIn** using Chrome (MFA enabled).
2. Chrome stores `li_at` cookie under `%LOCALAPPDATA%`.
3. Attacker (local user or RDP session) runs PowerShell to locate the cookie database.
4. Cookie is decrypted using `browser-cookie3` or via DPAPI.
5. Attacker imports the cookie into an incognito browser or automation tool.
6. **Session hijack successful** — MFA bypassed, full access granted.

---

## 🛡️ Detection Recommendations

* Monitor access to `Cookies` files from non-browser processes
* Detect PowerShell or Python accessing Chrome's `User Data` path
* Look for tools like `browser-cookie3`, SQLite usage on Chrome DBs
* Watch for unusual cookie reuse across geolocation/IP/device

Refer to [`detection/edr_detection_tips.md`](detection/edr_detection_tips.md) for detailed logic.

---

## 📌 Awareness Takeaway

Even without admin privileges, attackers (or insider threats) can extract session cookies and impersonate users. This is particularly dangerous for:

* Security staff reusing social media on work PCs
* Cloud console sessions (AWS, GCP, Azure)
* Privileged dashboards that don’t validate session IP/user agent

**MFA is not enough if the token/session is already trusted.**

---

## ✅ Defender Checklist

* [ ] Disable cookie saving for sensitive accounts
* [ ] Use Chrome policies to limit profile persistence
* [ ] Monitor cookie DB access
* [ ] Alert on `li_at`, `AWSALB`, `SID`, or other known session cookies
* [ ] Educate users on session risks and internal threat vectors

---

## 👤 Author

Abhiraj Singh
Cybersecurity Engineer | Blue Team | Detection Engineering
[LinkedIn](https://www.linkedin.com/in/abhiraj-singh-5029341b)

---

## 📄 License

MIT License
