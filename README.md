# 🛡️ DNS Guard (Prototype/Demo Version)

> **⚠️ PROTOTYPE REPOSITORY:** This repository (`domain-history-ledger-demo`) is a proof-of-concept prototype. It does **not** connect to live APIs. Instead, it uses **mock data waves** to demonstrate the system's capabilities, UI, and smart contract anchoring. It is intended for presentations and architectural validation.

DNS Guard is a system that provides a **permanent, tamper-resistant history of internet domains** by combining a traditional relational database (for speed and rich queries) with a blockchain smart contract (as an **immutable audit log**).

The system is designed to prevent **domain reputation laundering**, where malicious actors reuse expired or transferred domains by erasing their past abuse history.

---

## ✨ Features & The "Data Control Center"

Because this is a prototype, we built a dedicated **Admin UI** to simulate real-world data ingestion.

*   **Search Interface:** A premium, glassmorphism UI where users can search for domains (e.g., `amazon-deals-support.net`) and view their current "Traffic Light" trust status alongside a historic timeline of events.
*   **Transparent Analysis:** Real-time console logs appearing on the frontend to visualize the backend Python engine's decision-making process.
*   **The Control Center (Admin):** A separated engineering dashboard used to simulate live OSINT feeds.
    *   **Slide-out JSON Editors:** Manually edit and save "Registrar" and "Abuse" feed data directly in the browser.
    *   **Wave-Based Ingestion:** Inject data in chronological "Waves" (Wave 1 & Wave 2) to watch the database state and blockchain anchor proofs update in real-time.
    *   **Nuclear Reset:** A one-click button to securely wipe the database and start the demo over from scratch.

---

## 🏗️ Technology Stack

This prototype was built without heavy JavaScript frameworks to keep things blazing fast and easy to understand.

*   **Frontend Layer:** Pure HTML, Vanilla JavaScript, and Custom CSS (No frameworks).
*   **Backend Layer:** Python, Flask API, SQLite database.
*   **Blockchain Layer:** Solidity Smart Contract, Local Hardhat Node, Ethers.js, `web3.py`.

---

## 🚀 How to Run the Demo Locally

You need three terminal windows to run this full-stack prototype.

### 1. Start the Blockchain Notary
In your first terminal, start the local Ethereum network:
```bash
cd blockchain
npm install
npx hardhat node
```
*(Leave this terminal running. The smart contract is already pre-configured to deploy to this local node).*

### 2. Start the Backend Engine
In your second terminal, activate the Python environment and start Flask:
```bash
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies (if first time)
pip install -r backend/requirements.txt

# Start the Flask API
python -m backend.app
```
*(The server will run on `http://localhost:5000`)*

### 3. Open the Web Application
Because the frontend uses vanilla web technologies, there is no need for a Node/React dev server!

Simply open your File Explorer/Finder, navigate to `frontend/src/`, and **double-click `index.html`** to open it directly in your web browser.

---

## 🎮 How to Use the Prototype

1.  Open the web app and click the **"⚙️ Admin"** button in the top right corner.
2.  Click **"☢️ Reset"** to ensure your database is completely clean.
3.  Open the **Registrar Feed** sidebar -> Select **Wave 1** -> Click **"Inject Current Wave"**.
4.  Open the **Abuse Feed** sidebar -> Select **Wave 1** -> Click **"Inject Current Wave"**.
5.  Click **"← Back to Search"** and type `amazon-deals-support.net` to see the anchored results!

---

## 🗄️ Database Schema & Anchoring

The backend operates on a minimal SQLite schema focusing on Append-Only event tracking.

*   **domains:** Tracks the current cached status (`GREEN`, `YELLOW`, `RED`).
*   **domain_events:** Tracks the chronological history (`REGISTERED`, `OWNERSHIP_CHANGED`, `ABUSE_FLAG`). 
    *   When high-risk events (like `ABUSE_FLAG`) occur, a Keccak-256 hash of the event is generated and sent to the local Hardhat smart contract. 
    *   The resulting Blockchain Transaction Hash (`blockchain_tx`) is stored in the database alongside the event as cryptographic proof.
