# 🚀 Midnight Wallet - Quick Reference Card

## 📍 File Location
```
C:\Users\Samrat\OneDrive\Desktop\midnightsdk\wallet-app\index.html
```

## ⚡ Quick Start

### **Option 1: Double-Click**
```
START_WALLET.bat
```

### **Option 2: Manual**
```bash
# 1. Backend (if not running)
python api/server.py

# 2. Open in browser
index.html
```

---

## 🎯 Features at a Glance

| Feature | Icon | Description |
|---------|------|-------------|
| **Wallet** | 💼 | View balances, address, quick actions |
| **Send** | 💸 | Transfer NIGHT to any address |
| **Receive** | 📥 | Display your address, copy function |
| **Transactions** | 📜 | Complete history of all operations |
| **Generate DUST** | ⚡ | Convert NIGHT to DUST (1:1) |
| **Airdrop** | 🎁 | Get 10 NIGHT instantly |

---

## 💰 Token Info

| Token | Type | Units | Use |
|-------|------|-------|-----|
| **NIGHT** | Transferable | 1 = 1,000,000 | Main currency |
| **DUST** | Gas Token | 1 = 1,000,000 | Transaction fees |

**Conversion**: 1 NIGHT = 1 DUST (one-way)

---

## 🎨 UI Navigation

```
┌─────────────────────────────────────┐
│  🌙 Midnight Wallet    [Local Net]  │
├──────────┬──────────────────────────┤
│ 💼 Wallet│  Balance Cards           │
│ 💸 Send  │  Address Display         │
│ 📥 Receive│  Quick Actions          │
│ 📜 Trans │  Transaction List        │
│ ⚡ DUST  │  DUST Conversion         │
└──────────┴──────────────────────────┘
```

---

## 🔑 Quick Actions

### **Import Wallet**
1. Click "Import Wallet"
2. Paste 24-word mnemonic
3. Click "Import"

### **Send NIGHT**
1. Go to "Send" view
2. Enter address (mn_addr_undeployed1...)
3. Enter amount or click quick button
4. Click "Send Transaction"

### **Generate DUST**
1. Go to "Generate DUST" view
2. Enter NIGHT amount
3. See 1:1 preview
4. Click "Generate DUST"

### **Get Free Tokens**
1. Click "Airdrop" button
2. Receive 10 NIGHT instantly

---

## 📊 Transaction Log

| Type | Icon | Color | Meaning |
|------|------|-------|---------|
| Send | 💸 | Red | Outgoing transfer |
| Receive | 📥 | Green | Incoming transfer |
| DUST | ⚡ | Yellow | DUST generation |

**Storage**: Persists in browser localStorage

---

## 🌐 Endpoints

| Service | URL |
|---------|-----|
| Backend API | http://localhost:8000 |
| Node | http://127.0.0.1:9944 |
| Indexer | http://127.0.0.1:8088 |
| Prover | http://127.0.0.1:6300 |

---

## 🎯 Quick Buttons

### **Send View**
- `0.5` - Send 0.5 NIGHT
- `1` - Send 1 NIGHT
- `5` - Send 5 NIGHT
- `10` - Send 10 NIGHT
- `MAX` - Send all NIGHT

### **DUST View**
- `1` - Convert 1 NIGHT
- `5` - Convert 5 NIGHT
- `10` - Convert 10 NIGHT

---

## 🔄 Status Indicators

| Indicator | Meaning |
|-----------|---------|
| 🔄 | Refresh balance |
| ⏳ | Loading... |
| ✅ | Success |
| ❌ | Error |
| 📋 | Copy to clipboard |

---

## 💾 Storage

| Key | Data |
|-----|------|
| `midnight_wallet_mnemonic` | Your 24-word phrase |
| `midnight_wallet_address` | Your wallet address |
| `midnight_transactions` | Transaction history |

**Location**: Browser localStorage

---

## 🐛 Quick Fixes

### **Balance not updating?**
→ Click refresh button (🔄)

### **Transaction failed?**
→ Check balance and address format

### **Backend not responding?**
→ Restart: `python api/server.py`

### **Wallet not loading?**
→ Clear browser cache

---

## 📱 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` | Copy (when address selected) |
| `F5` | Refresh page |
| `Ctrl+Shift+I` | Open DevTools |

---

## 🎨 Color Codes

| Color | Hex | Use |
|-------|-----|-----|
| Primary | `#6366f1` | Main actions |
| Secondary | `#8b5cf6` | Secondary actions |
| Success | `#10b981` | Confirmations |
| Error | `#ef4444` | Errors |
| Warning | `#f59e0b` | Warnings |

---

## 📞 Support Checklist

Before asking for help:
- [ ] Backend API running?
- [ ] Docker containers up?
- [ ] Browser console errors?
- [ ] Correct address format?
- [ ] Sufficient balance?
- [ ] Network connected?

---

## 🎉 You're All Set!

**Wallet Location**:
```
C:\Users\Samrat\OneDrive\Desktop\midnightsdk\wallet-app\index.html
```

**Backend Status**: ✅ Running (Terminal ID: 9)

**Quick Start**: Double-click `START_WALLET.bat`

---

## 📚 Documentation

- `README.md` - Complete guide
- `WALLET_COMPLETE.md` - Implementation details
- `WALLET_FEATURES_SUMMARY.md` - Feature overview
- `QUICK_REFERENCE.md` - This file

---

**Happy transacting! 🚀🌙**
