# 🚀 Quick Start Guide

Get up and running with Midnight in 5 minutes!

## Prerequisites

- ✅ Python 3.11+ installed
- ✅ Docker Desktop installed and **RUNNING**
- ✅ Node.js 22+ installed

## Step 1: Install Dependencies

```bash
# Install Python package
pip install -e .

# Install Node.js dependencies (for wallet SDK)
npm install
```

## Step 2: Start Docker Services

**IMPORTANT**: Make sure Docker Desktop is running first!

```bash
# Start all services (node, indexer, proof server)
docker-compose up -d

# Wait 10 seconds for services to start
timeout /t 10

# Verify services are running
docker ps
```

You should see 3 containers running:
- `midnight_python_sdk-midnight-node-1`
- `midnight_python_sdk-midnight-indexer-1`
- `midnight_python_sdk-midnight-proof-1`

## Step 3: Create Your Wallet

```bash
python create_wallet.py
```

This will:
- Generate a new 24-word mnemonic phrase
- Save it to `mnemonic.txt`
- Display security warnings

**⚠️ IMPORTANT**: Write down your mnemonic phrase and store it safely!

## Step 4: Get Your Wallet Address

```bash
node get_wallet_address.mjs
```

Output:
```json
{
  "address": "mn_addr_undeployed1zaa268rc7sjz0cts...",
  "dust": "0",
  "night": "0"
}
```

**Note**: Local network wallets are automatically funded when you interact with them!

## Step 5: Deploy Your First Contract

```bash
python deploy_hello_world.py
```

This will:
- Connect to local services
- Compile the `hello_world.compact` contract
- Generate ZK proof (takes 30-60 seconds)
- Deploy to local blockchain
- Save contract address to `deployed_contract.txt`

## Step 6: Interact with Your Contract

```bash
python call_contract.py
```

This will:
- Load your deployed contract
- Prompt you for a message
- Call the `storeMessage` circuit
- Display the transaction hash
- Show the updated contract state

## Step 7: View in Explorer

Open your browser to:
```
http://localhost:8088
```

You'll see:
- All transactions in real-time
- Contract deployments
- Transaction details
- Auto-refresh every 5 seconds

## 🎯 Quick Commands Reference

```bash
# Check service status
midnight-sdk status

# Check wallet balance
midnight-sdk balance <your_address>

# Deploy a contract
python deploy_hello_world.py

# Call a contract
python call_contract.py

# Read contract state
midnight-sdk state <contract_address>

# View transaction
midnight-sdk tx get <tx_hash>

# Stop services
docker-compose down
```

## 🐛 Troubleshooting

### Docker not running
```
Error: Cannot connect to Docker daemon
```
**Solution**: Start Docker Desktop and wait for it to fully load

### Services not starting
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart

# Clean restart
docker-compose down -v
docker-compose up -d
```

### Port already in use
```
Error: port is already allocated
```
**Solution**: Stop other services using ports 9944, 8088, or 6300

### Proof server timeout
```
Error: Proof generation timeout
```
**Solution**: 
1. Check proof server: `docker-compose logs midnight-proof`
2. Restart: `docker-compose restart midnight-proof`
3. Wait 30 seconds and try again

## 📚 Next Steps

1. **Try other contracts**: Deploy `counter.compact`, `bulletin_board.compact`
2. **Run examples**: Check the `examples/` directory
3. **Read docs**: See `docs/` for detailed guides
4. **Test on preprod**: Deploy to real testnet (see `GETTING_STARTED.md`)

## 🎓 Learning Path

1. ✅ Create wallet (you just did this!)
2. ✅ Deploy contract (you just did this!)
3. ✅ Call circuits (you just did this!)
4. 📖 Read `docs/CONTRACT_TESTING_GUIDE.md`
5. 📖 Read `docs/QUICK_SIGNING_GUIDE.md`
6. 🚀 Deploy to preprod network
7. 🏗️ Build your own contract

## 💡 Tips

- **Local network**: Perfect for development, no real funds needed
- **Preprod network**: Real testnet, requires faucet tokens
- **Explorer**: Always check transactions in the web UI
- **Logs**: Use `docker-compose logs -f` to watch real-time logs
- **Clean slate**: Use `docker-compose down -v` to reset everything

---

**Congratulations!** 🎉 You've successfully created a wallet and deployed your first Midnight contract!

For more details, see `GETTING_STARTED.md`
