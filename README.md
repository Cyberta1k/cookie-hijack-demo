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
├── detection/
│   └── edr_detection_tips.md          ← Detection logic for blue teams
├── mfa_cookie_bypass.png          ← Diagrams/screenshots
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
## 2. 🔓 browser-cookie3

A Python tool that extracts and decrypts cookies from Chrome using the current user’s **DPAPI** context.

### 🧰 Requirements

Install the required Python module:

```bash
pip install browser-cookie3
```
### 🔍 Usage
Run the provided script:

```bash
python python/decrypt_with_browser_cookie3.py
```
You will be prompted to enter a domain (e.g., linkedin.com). The script will print decrypted cookies, including:

✅ li_at – LinkedIn session cookie (often used in MFA bypasses)

✅ li_rm, lidc, JSESSIONID, and others

> **🔒 Important**: Run the script under the same Windows user account where Chrome cookies were originally created. DPAPI decryption is user-context specific.

---
### 🛠️ Manual Cookie Injection for Session Hijacking

After extracting the plaintext cookie value (e.g., `li_at`), you can manually inject it into a browser to hijack the session:

1. Open your browser (Chrome recommended).
2. Navigate to the LinkedIn website: `https://www.linkedin.com`.
3. Open **Developer Tools**:
   - Press `F12` or `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (Mac).
4. Go to the **Application** tab.
5. Under **Storage** (left sidebar), select **Cookies** > `https://www.linkedin.com`.
6. In the cookie list, click **Add** (usually a "+" icon or right-click > "Add").
7. Create a new cookie with these details:
   - **Name:** `li_at`  
   - **Value:** `<paste_the_extracted_li_at_cookie_value_here>`  
   - **Domain:** `.linkedin.com`  
   - **Path:** `/`  
   - **Secure:** Checked  
   - **HttpOnly:** Checked (if possible)  
8. Refresh the LinkedIn page or open a new tab for `https://www.linkedin.com`.  
9. You should now be logged in as the user associated with the injected cookie.

> ⚠️ **Warning:** This technique bypasses normal login flows and MFA. Use responsibly and only in authorized environments.


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
