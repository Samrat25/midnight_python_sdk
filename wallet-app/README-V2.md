# 🌙 Midnight Wallet V2 - Lace-Inspired Design

## ✨ What's New

### 🎨 **Modern Lace.io-Inspired UI**
- Clean, professional design matching Lace wallet aesthetics
- Smooth animations and transitions
- Dark theme optimized for crypto
- Responsive sidebar navigation
- Beautiful gradient cards

### 🔐 **Shielded & Unshielded Transfers**
- **Unshielded**: Public transfers (visible on blockchain)
- **Shielded**: Private transfers (ZK-proof protected)
- Easy toggle between transfer types
- Same simple interface for both

### ⚡ **CLI Integration**
- Open wallet with one command: `open-wallet.bat`
- No need to navigate to file manually
- Auto-starts backend if not running
- Quick access from command line

---

## 🚀 Quick Start

### **Option 1: Double-Click (Easiest)**
```
Double-click: open-wallet.bat
```

### **Option 2: Command Line**
```bash
cd wallet-app
open-wallet.bat
```

### **Option 3: Manual**
```bash
# 1. Start backend (if not running)
python api/server.py

# 2. Open wallet
# Open: index-v2.html in browser
```

---

## 🎯 Features

### **Wallet Management**
- ✅ Import wallet (24-word recovery phrase)
- ✅ Create new wallet
- ✅ Persistent storage
- ✅ Copy address function

### **Balance Display**
- ✅ Total balance hero card
- ✅ NIGHT balance (transferable)
- ✅ DUST balance (gas token)
- ✅ Real-time updates

### **Send Transfers**
- ✅ **Unshielded** - Public transfers
- ✅ **Shielded** - Private transfers with ZK proofs
- ✅ Quick amount buttons (0.5, 1, 5, 10, MAX)
- ✅ Transaction summary
- ✅ TX hash confirmation

### **Receive**
- ✅ Display address
- ✅ QR code placeholder
- ✅ Copy function

### **Activity**
- ✅ Complete transaction history
- ✅ Send/Receive/DUST tracking
- ✅ Transfer type display (shielded/unshielded)
- ✅ Persistent storage

### **Quick Actions**
- ✅ Send button
- ✅ Receive button
- ✅ DUST generation
- ✅ Airdrop (10 NIGHT)

---

## 🔐 Transfer Types Explained

### **Unshielded Transfers**
- **Public**: Transaction details visible on blockchain
- **Fast**: Quick confirmation
- **Simple**: No ZK proof generation
- **Use for**: Regular transfers, public payments

### **Shielded Transfers**
- **Private**: Transaction details hidden with ZK proofs
- **Secure**: Amount and recipient concealed
- **Advanced**: Uses zero-knowledge cryptography
- **Use for**: Private payments, confidential transactions

---

## 🎨 UI Design

### **Inspired by Lace.io**
- Modern, clean interface
- Professional color scheme
- Smooth animations
- Card-based layout
- Intuitive navigation

### **Color Palette**
- Primary: `#6366f1` (Indigo)
- Secondary: `#8b5cf6` (Purple)
- Success: `#10b981` (Green)
- Error: `#ef4444` (Red)
- Warning: `#f59e0b` (Amber)

### **Layout**
```
┌─────────────────────────────────────┐
│  🌙 Midnight    [Local Network]     │
├──────────┬──────────────────────────┤
│ Overview │  Total Balance Card      │
│ Send     │  Quick Actions Grid      │
│ Receive  │  Assets List             │
│ Activity │  Address Display         │
│          │                          │
│ Settings │                          │
└──────────┴──────────────────────────┘
```

---

## 📁 Files

### **New V2 Files**
- `index-v2.html` - Modern UI
- `styles-v2.css` - Lace-inspired styles
- `wallet-v2.js` - Enhanced logic with shielded/unshielded
- `open-wallet.bat` - CLI launcher
- `README-V2.md` - This file

### **Backend**
- `api/server.py` - FastAPI backend

---

## 🔧 How It Works

### **Unshielded Transfer Flow**
```
User selects "Unshielded"
  ↓
Enters recipient + amount
  ↓
Calls /wallet/transfer-unshielded
  ↓
Signs with mnemonic
  ↓
Submits to blockchain
  ↓
Returns TX hash
  ↓
Logs transaction
```

### **Shielded Transfer Flow**
```
User selects "Shielded"
  ↓
Enters recipient + amount
  ↓
Calls /wallet/transfer-shielded
  ↓
Generates ZK proof
  ↓
Signs with mnemonic
  ↓
Submits to blockchain
  ↓
Returns TX hash
  ↓
Logs transaction
```

---

## 🌐 Endpoints

### **Wallet Operations**
- `POST /wallet/generate-mnemonic` - Generate new wallet
- `POST /wallet/get-address` - Get address from mnemonic
- `POST /wallet/get-balance` - Get NIGHT and DUST balance
- `POST /wallet/transfer-unshielded` - Public transfer
- `POST /wallet/transfer-shielded` - Private transfer

### **Node Operations**
- `POST http://127.0.0.1:9944/balance` - Update balance (airdrop/DUST)

---

## 💡 Usage Examples

### **Open Wallet**
```bash
# From anywhere
cd C:\Users\Samrat\OneDrive\Desktop\midnightsdk\wallet-app
open-wallet.bat
```

### **Send Unshielded Transfer**
1. Click "Send" in sidebar
2. Select "Unshielded" (default)
3. Enter recipient address
4. Enter amount or use quick buttons
5. Click "Send Transaction"
6. View TX hash in confirmation

### **Send Shielded Transfer**
1. Click "Send" in sidebar
2. Select "Shielded"
3. Enter recipient address
4. Enter amount
5. Click "Send Transaction"
6. Wait for ZK proof generation
7. View TX hash in confirmation

### **Generate DUST**
1. Click "DUST" in quick actions
2. Enter NIGHT amount to convert
3. Confirm conversion (1:1 ratio)
4. DUST added instantly

### **View Activity**
1. Click "Activity" in sidebar
2. See all transactions
3. Filter by type (send/receive/dust)
4. View transfer type (shielded/unshielded)

---

## 🎯 Comparison: V1 vs V2

| Feature | V1 | V2 |
|---------|----|----|
| UI Design | Basic gradients | Lace-inspired |
| Transfer Types | Unshielded only | Unshielded + Shielded |
| CLI Integration | Manual open | `open-wallet.bat` |
| Navigation | Top tabs | Sidebar |
| Layout | Single column | Card-based grid |
| Animations | Basic | Smooth transitions |
| Color Scheme | Purple/blue | Professional dark |
| Quick Actions | 4 buttons | 4 action cards |
| Activity View | List | Enhanced list with icons |

---

## 🔥 Key Improvements

### **1. Better UI/UX**
- Lace.io-inspired design
- Professional appearance
- Smooth animations
- Better spacing and typography

### **2. Shielded Transfers**
- Privacy-preserving transactions
- ZK-proof integration
- Easy toggle between types

### **3. CLI Integration**
- One-command launch
- Auto-start backend
- No manual navigation

### **4. Enhanced Activity**
- Transfer type display
- Better transaction cards
- Improved time formatting

### **5. Modern Layout**
- Sidebar navigation
- Card-based design
- Responsive grid
- Better visual hierarchy

---

## 📊 Technical Details

### **Frontend**
- Pure HTML5, CSS3, JavaScript
- No framework dependencies
- Modern CSS Grid and Flexbox
- Custom SVG icons
- Inter font family

### **Backend**
- FastAPI (Python)
- Midnight Python SDK
- Transfer scripts (Node.js)
- CORS enabled

### **Blockchain**
- Node: http://127.0.0.1:9944
- Indexer: http://127.0.0.1:8088
- Prover: http://127.0.0.1:6300
- Network: undeployed

---

## 🐛 Troubleshooting

### **Wallet won't open**
```bash
# Check file path
cd C:\Users\Samrat\OneDrive\Desktop\midnightsdk\wallet-app

# Run manually
start index-v2.html
```

### **Backend not starting**
```bash
# Check if running
tasklist | findstr python

# Start manually
python api/server.py
```

### **Shielded transfer fails**
- Ensure proof server is running (http://127.0.0.1:6300)
- Check Docker containers are up
- Verify sufficient DUST for fees
- Check indexer connection

### **Balance not updating**
- Click refresh button
- Check Docker containers
- Verify node endpoint
- Clear browser cache

---

## 🎉 Success!

Your new Midnight Wallet V2 is ready with:
- ✨ Modern Lace-inspired UI
- 🔐 Shielded & Unshielded transfers
- ⚡ CLI integration
- 📜 Enhanced activity tracking
- 💰 Real-time balance updates

**Open it now:**
```bash
cd wallet-app
open-wallet.bat
```

---

## 📞 Quick Access

### **Wallet Location**
```
C:\Users\Samrat\OneDrive\Desktop\midnightsdk\wallet-app\index-v2.html
```

### **CLI Command**
```bash
cd C:\Users\Samrat\OneDrive\Desktop\midnightsdk\wallet-app
open-wallet.bat
```

### **Backend API**
```
http://localhost:8000
```

---

**Enjoy your new wallet! 🚀🌙**
