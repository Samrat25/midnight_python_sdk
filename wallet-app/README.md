# 🌙 Midnight Wallet - Single Page Application

A beautiful, Lace-inspired wallet for Midnight Network with complete transaction logging and DUST generation.

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Network](https://img.shields.io/badge/network-local%20docker-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ Features

### 🎨 **Beautiful UI**
- Lace-inspired design with purple/blue gradients
- Smooth animations and transitions
- Responsive sidebar navigation
- Dark theme optimized for crypto

### 💼 **Wallet Management**
- Import wallet with 24-word mnemonic
- Generate new secure wallet
- Persistent wallet storage
- Copy address with one click

### 💰 **Balance Display**
- Real-time NIGHT balance
- Real-time DUST balance
- Total balance overview
- Auto-refresh capability

### 💸 **Send Transfers**
- Send NIGHT to any address
- Quick amount buttons (0.5, 1, 5, 10, MAX)
- Transaction preview
- TX hash confirmation

### 📥 **Receive Tokens**
- Display your address
- QR code placeholder
- Easy copy function

### ⚡ **DUST Generation**
- Convert NIGHT to DUST (1:1 ratio)
- Quick conversion buttons
- Real-time preview
- Instant updates

### 📜 **Transaction History**
- Complete transaction log
- Send/Receive/DUST tracking
- Persistent storage
- Time-based display

### 🎁 **Airdrop**
- Get 10 NIGHT instantly
- Direct node integration
- Auto balance update

---

## 🚀 Quick Start

### **Option 1: Use Batch File (Easiest)**
```bash
# Double-click this file:
START_WALLET.bat
```

### **Option 2: Manual Start**
```bash
# 1. Start backend API
python api/server.py

# 2. Open wallet in browser
# Open: index.html
```

---

## 📋 Requirements

- Python 3.8+
- FastAPI
- Midnight Python SDK
- Docker (for local network)
- Modern web browser

---

## 🔧 Configuration

### **Backend API**
- **URL**: http://localhost:8000
- **CORS**: Enabled for local development
- **Endpoints**: See API documentation below

### **Blockchain Network**
- **Node**: http://127.0.0.1:9944
- **Indexer**: http://127.0.0.1:8088
- **Prover**: http://127.0.0.1:6300
- **Network ID**: undeployed

---

## 📁 File Structure

```
wallet-app/
├── index.html              # Main UI
├── styles.css              # Lace-inspired styles
├── wallet.js               # Wallet logic + transaction log
├── START_WALLET.bat        # Quick start script
├── README.md               # This file
└── api/
    └── server.py           # FastAPI backend
```

---

## 🎯 How to Use

### **1. Import or Create Wallet**
- Click "Import Wallet" to use existing mnemonic
- Click "Create New" to generate new wallet
- Save your mnemonic securely!

### **2. View Your Balance**
- See NIGHT (transferable tokens)
- See DUST (gas tokens)
- Click refresh to update

### **3. Send Tokens**
- Go to "Send" view
- Enter recipient address (mn_addr_undeployed1...)
- Enter amount or use quick buttons
- Click "Send Transaction"
- View TX hash in confirmation

### **4. Receive Tokens**
- Go to "Receive" view
- Copy your address
- Share with sender

### **5. Generate DUST**
- Go to "Generate DUST" view
- Enter NIGHT amount to convert
- See 1:1 conversion preview
- Click "Generate DUST"
- DUST added instantly

### **6. View History**
- Go to "Transactions" view
- See all send/receive/dust transactions
- View amounts and timestamps
- History persists across sessions

### **7. Get Test Tokens**
- Click "Airdrop" button
- Receive 10 NIGHT instantly
- Balance updates automatically

---

## 🌐 API Endpoints

### **Wallet Operations**

#### Generate Mnemonic
```http
POST /wallet/generate-mnemonic
Response: { "mnemonic": "word1 word2 ... word24" }
```

#### Get Address
```http
POST /wallet/get-address
Body: { "mnemonic": "...", "networkId": "undeployed" }
Response: { "address": "mn_addr_..." }
```

#### Get Balance
```http
POST /wallet/get-balance
Body: { "address": "...", "networkId": "undeployed" }
Response: { "dust": 0, "night": 0 }
```

#### Transfer Unshielded
```http
POST /wallet/transfer-unshielded
Body: {
  "fromAddress": "...",
  "toAddress": "...",
  "amount": 1000000,
  "mnemonic": "...",
  "networkId": "undeployed"
}
Response: { "txHash": "0x...", "status": "pending" }
```

### **Node Operations**

#### Update Balance (Airdrop/DUST)
```http
POST http://127.0.0.1:9944/balance
Body: {
  "address": "...",
  "dust": 10000000,
  "night": 10000000
}
```

---

## 💾 Data Storage

### **LocalStorage Keys**
- `midnight_wallet_mnemonic` - Your wallet mnemonic
- `midnight_wallet_address` - Your wallet address
- `midnight_transactions` - Transaction history array

### **Transaction Format**
```javascript
{
  type: 'send' | 'receive' | 'dust',
  address: 'recipient or source',
  amount: 1000000,  // smallest units
  token: 'NIGHT' | 'DUST',
  txHash: '0x...',  // optional
  timestamp: 1234567890
}
```

---

## 🎨 UI Components

### **Views**
1. **Wallet** - Main dashboard with balances
2. **Send** - Transfer NIGHT tokens
3. **Receive** - Display your address
4. **Transactions** - View history
5. **Generate DUST** - Convert NIGHT to DUST

### **Modals**
- **Import Wallet** - Enter existing mnemonic
- **Create Wallet** - Generate new mnemonic

### **Cards**
- Balance cards (gradient primary, secondary grid)
- Address card (with copy button)
- Transaction items (with type icons)
- Form cards (with validation)

---

## 🔐 Security Notes

### **Development Mode**
- Mnemonic stored in localStorage (not secure for production)
- CORS enabled for all origins
- No encryption on stored data

### **Production Recommendations**
- Use secure key management (hardware wallet, encrypted storage)
- Implement proper CORS restrictions
- Add authentication and authorization
- Use HTTPS for all connections
- Encrypt sensitive data
- Add rate limiting
- Implement session management

---

## 🐛 Troubleshooting

### **Backend Not Starting**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F

# Restart backend
python api/server.py
```

### **Balance Not Updating**
- Click refresh button
- Check Docker containers are running
- Verify node endpoint: http://127.0.0.1:9944
- Check browser console for errors

### **Transaction Failed**
- Verify recipient address format (mn_addr_undeployed1...)
- Check sufficient balance
- Ensure DUST available for fees
- Check backend API logs

### **Wallet Not Loading**
- Clear browser cache
- Check localStorage is enabled
- Verify backend API is running
- Open browser console for errors

---

## 📊 Token Information

### **NIGHT Token**
- **Type**: Transferable
- **Units**: 1 NIGHT = 1,000,000 units
- **Use**: Main currency for transfers
- **Can be**: Sent, received, converted to DUST

### **DUST Token**
- **Type**: Non-transferable (gas token)
- **Units**: 1 DUST = 1,000,000 units
- **Use**: Transaction fees
- **Can be**: Generated from NIGHT, used for gas
- **Cannot be**: Transferred to other addresses

### **Conversion**
- **Ratio**: 1 NIGHT = 1 DUST (1:1)
- **Process**: Instant via node API
- **Reversible**: No (one-way conversion)

---

## 🎯 Features Checklist

- ✅ Wallet import/create
- ✅ Balance display (NIGHT + DUST)
- ✅ Send transfers
- ✅ Receive address
- ✅ DUST generation
- ✅ Transaction history
- ✅ Airdrop function
- ✅ Lace-inspired UI
- ✅ Persistent storage
- ✅ Real-time updates
- ✅ Copy address
- ✅ Quick amount buttons
- ✅ Transaction preview
- ✅ Loading states
- ✅ Error handling

---

## 🚀 Future Enhancements

- [ ] QR code generation
- [ ] Transaction filtering
- [ ] Export history (CSV/JSON)
- [ ] Multiple wallet support
- [ ] Address book
- [ ] Transaction notifications
- [ ] Price charts
- [ ] Shielded transfers
- [ ] Hardware wallet support
- [ ] Mobile responsive improvements

---

## 📝 Development

### **Tech Stack**
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: FastAPI (Python)
- **Blockchain**: Midnight Network (Docker)
- **Storage**: Browser LocalStorage

### **No Dependencies**
- No npm/yarn required
- No build process
- No framework overhead
- Pure vanilla implementation

### **Code Structure**
- Modular JavaScript functions
- CSS custom properties for theming
- RESTful API design
- Clean separation of concerns

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📞 Support

For issues or questions:
- Check troubleshooting section
- Review API documentation
- Check browser console
- Verify Docker containers

---

## 🎉 Enjoy Your Wallet!

Your Midnight wallet is ready to use with:
- ✨ Beautiful Lace-inspired UI
- ⚡ DUST generation
- 📜 Complete transaction log
- 💰 Real-time balance updates
- 🎁 Instant airdrop

**Happy transacting!** 🚀
