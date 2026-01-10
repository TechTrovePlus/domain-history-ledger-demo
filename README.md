# Domain History & Reputation Ledger

A mini project that provides a permanent, tamper-resistant history for internet domain names
using blockchain as an immutable audit log.

## Problem Statement
Domain reputation systems forget history when domains change ownership or are re-registered.
This allows attackers to reuse domains for phishing and scams.  
This project prevents reputation laundering by making domain history permanent and verifiable.

## Tech Stack
- Blockchain: Ethereum (Local Test Network)
- Smart Contracts: Solidity
- Backend: Python (Flask)
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Version Control: Git & GitHub

## Research Foundation
This project is grounded in prior research on:
- Blockchain-based reputation system architectures
- Domain name reputation and lifecycle analysis

The design follows best practices recommended in academic literature by using blockchain only as an immutable
audit layer while performing all analytics and reputation logic off-chain.

