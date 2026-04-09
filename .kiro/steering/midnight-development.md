---
inclusion: auto
description: Comprehensive guidelines for developing smart contracts on Midnight blockchain using Nightforge, Compact language, and Midnight SDK 4.x. Covers prerequisites, version compatibility, deployment workflows, DUST token management, and production deployment patterns.
---

# Midnight Blockchain Development Rules

This skill provides comprehensive guidelines for developing smart contracts on the Midnight blockchain using Nightforge, Compact language, and the Midnight SDK.

## Core Technologies

- **Nightforge**: CLI tool for Midnight smart contract development
- **Compact**: Domain-specific language for writing Midnight smart contracts
- **Midnight SDK**: JavaScript/TypeScript SDK for interacting with contracts
- **Proof Server**: ZK proof generation service (runs on Docker)

## Prerequisites & Setup

### Required Tools
- Node.js v22+
- Docker (for proof server)
- Compact compiler installation:
  ```bash
  curl --proto '=https' --tlsv1.2 -LsSf https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh
  source ~/.bashrc
  ```

### Project Initialization
```bash
npx nightforge init <project-name>
cd <project-name>
```

## Critical Version Compatibility Rules

### Compact Language Version
- **ALWAYS** use `pragma language_version >= 0.22;` in `.compact` files
- **NEVER** use `pragma language_version 0.21;` (outdated)
- Fix this in `contracts/example.compact` after initialization

### SDK Version Requirements
Nightforge 0.0.6 scaffolds SDK 3.x but Compact 0.5.0+ requires SDK 4.x.

**Required package.json dependencies:**
```json
{
  "@midnight-ntwrk/compact-runtime": "0.15.0",
  "@midnight-ntwrk/compact-js": "2.5.0",
  "@midnight-ntwrk/ledger": "4.0.0",
  "@midnight-ntwrk/ledger-v8": "8.0.3",
  "@midnight-ntwrk/midnight-js-contracts": "4.0.2",
  "@midnight-ntwrk/midnight-js-http-client-proof-provider": "4.0.2",
  "@midnight-ntwrk/midnight-js-indexer-public-data-provider": "4.0.2",
  "@midnight-ntwrk/midnight-js-level-private-state-provider": "4.0.2",
  "@midnight-ntwrk/midnight-js-network-id": "4.0.2",
  "@midnight-ntwrk/midnight-js-node-zk-config-provider": "4.0.2",
  "@midnight-ntwrk/midnight-js-types": "4.0.2",
  "@midnight-ntwrk/midnight-js-utils": "4.0.2",
  "@midnight-ntwrk/wallet-sdk-address-format": "3.1.0",
  "@midnight-ntwrk/wallet-sdk-dust-wallet": "3.0.0",
  "@midnight-ntwrk/wallet-sdk-facade": "3.0.0",
  "@midnight-ntwrk/wallet-sdk-hd": "3.0.1",
  "@midnight-ntwrk/wallet-sdk-shielded": "2.1.0",
  "@midnight-ntwrk/wallet-sdk-unshielded-wallet": "2.1.0",
  "rxjs": "^7.8.2",
  "ws": "^8.19.0"
}
```

**After updating package.json:**
```bash
rm -rf node_modules package-lock.json && npm install
```

## Deployment Workflows

### Preprod Network Deployment

1. **Compile contracts:**
   ```bash
   npx nightforge compile
   ```

2. **Start proof server:**
   ```bash
   docker run -d -p 6300:6300 midnightntwrk/proof-server:latest midnight-proof-server -v
   ```

3. **Create and fund wallet:**
   ```bash
   npx nightforge wallet create
   ```
   - Visit https://faucet.preprod.midnight.network/
   - Paste wallet address and request tNIGHT
   - Wait 2-3 minutes for funding

4. **Deploy using custom script:**
   ```bash
   node deploy.mjs
   ```
   - **NEVER** use `npx nightforge deploy` (incompatible with SDK 4.x)
   - Custom script handles: wallet setup, DUST registration, ZK proof generation, deployment
   - Contract address saved to `deployment.json`

### Local Dev Network Deployment

1. **Start local environment:**
   ```bash
   git clone https://github.com/midnightntwrk/midnight-local-dev
   cd midnight-local-dev
   docker compose up
   ```

2. **Service endpoints:**
   - Node: `http://127.0.0.1:9944`
   - Indexer: `http://127.0.0.1:8088/api/v3/graphql`
   - Indexer WS: `ws://127.0.0.1:8088/api/v3/graphql/ws`
   - Proof Server: `http://127.0.0.1:6300`

3. **Fund wallet:**
   ```bash
   yarn fund-and-register-dust "<wallet-seed>"
   ```

4. **Update deploy.mjs configuration:**
   ```javascript
   const NETWORK_ID = 'undeployed';
   const INDEXER = 'http://127.0.0.1:8088/api/v3/graphql';
   const INDEXER_WS = 'ws://127.0.0.1:8088/api/v3/graphql/ws';
   const NODE = 'http://127.0.0.1:9944';
   const PROOF_SERVER = 'http://127.0.0.1:6300';
   ```

5. **Deploy:**
   ```bash
   node deploy.mjs
   ```

## DUST Token Management

**Critical concept:** DUST is a non-transferable gas token generated over time from registered tNIGHT UTXOs.

### DUST Generation Process
1. Wallet must have tNIGHT tokens
2. UTXOs must be registered for DUST generation
3. **Wait 2-5 minutes** after registration for DUST to accrue
4. DUST accumulates automatically from registered UTXOs

### Handling "Insufficient Funds: could not balance dust"
1. Verify wallet has tNIGHT (use faucet or local funding)
2. Ensure deploy script registers UTXOs
3. **Wait 2-5 minutes** after registration
4. Retry deployment: `node deploy.mjs`

## Common Issues & Solutions

### Version Mismatch Errors

**Error:** "Version mismatch: compiled code expects 0.15.0, runtime is 0.14.0"
- **Solution:** Update `compact-runtime` to `0.15.0` and `compact-js` to `2.5.0`

**Error:** "expected instance of ContractMaintenanceAuthority / LedgerParameters / DustParameters"
- **Cause:** SDK version mismatch (ledger-v7 types mixed with ledger-v8)
- **Solution:** Upgrade all wallet SDK packages to ledger-v8 compatible versions

### Proof Server Issues

**Error:** "Proof server status not found"
- **Cause:** Nightforge expects `proof-server-status.json` in project root
- **Solution:** Use `deploy.mjs` instead (connects to proof server directly)

**Issue:** Deployment timeout
- **Cause:** Proof generation takes 30-60 seconds
- **Solution:** 
  - Verify proof server is running: `curl http://127.0.0.1:6300`
  - Retry deployment

## Code Generation Rules

### When generating deploy.mjs scripts:
1. Include wallet setup and initialization
2. Implement DUST registration logic
3. Connect to proof server (not status file)
4. Handle ZK proof generation with proper timeouts
5. Save deployment info to `deployment.json`
6. Use correct network configuration constants

### When working with Compact contracts:
1. Always use `pragma language_version >= 0.22;`
2. Follow Compact syntax and type system
3. Compile before deployment: `npx nightforge compile`
4. Check compiled output in `managed/` directory

### When creating client code:
1. Import from SDK 4.x packages
2. Use ledger-v8 types consistently
3. Handle async operations with proper error handling
4. Implement proper wallet connection logic
5. Use RxJS for reactive state management

## Best Practices

1. **Always verify SDK versions** before deployment
2. **Never mix ledger-v7 and ledger-v8** types
3. **Wait for DUST accumulation** before retrying failed deployments
4. **Use custom deploy.mjs** instead of nightforge deploy command
5. **Keep proof server running** during development
6. **Test on local network** before preprod deployment
7. **Monitor proof generation** (can take 30-60 seconds)
8. **Save deployment artifacts** (deployment.json, contract addresses)

## File Structure Expectations

```
project-root/
├── contracts/
│   └── example.compact          # Smart contract source
├── managed/                      # Compiled contract output
├── deploy.mjs                    # Custom deployment script
├── deployment.json               # Deployment artifacts
├── package.json                  # SDK 4.x dependencies
└── node_modules/                 # Installed packages
```

## Network Configuration

### Preprod Network
- Network ID: `preprod`
- Faucet: https://faucet.preprod.midnight.network/
- Indexer: (provided by Midnight network)
- Node: (provided by Midnight network)

### Local Dev Network
- Network ID: `undeployed`
- All services run locally via Docker Compose
- Full control over network state

## When to Use This Skill

Apply these rules when:
- Initializing new Midnight projects
- Deploying smart contracts to Midnight
- Troubleshooting version compatibility issues
- Setting up local development environments
- Working with DUST token mechanics
- Generating deployment scripts
- Configuring SDK dependencies
- Debugging proof generation issues

## Example Contract Code

### Hello World Contract (example.compact)

```compact
// Hello World Compact contract
pragma language_version >= 0.22;

// Public on-chain state
export ledger message: Bytes<11>;

// Initialize state during deploy 
constructor() {
  message = "Hello World";
}

// Read current message
export circuit getMessage(): Bytes<11> {
  return message;
}

// Update current message
export circuit storeMessage(newMessage: Bytes<11>): [] {
  message = disclose(newMessage);
}

// Hardcoded default: "Hello World"
```

### Key Contract Patterns

1. **Pragma Declaration**: Always use `pragma language_version >= 0.22;`
2. **Ledger State**: Use `export ledger` for public on-chain state
3. **Constructor**: Initialize state during deployment
4. **Circuits**: Use `export circuit` for callable functions
5. **Type System**: Compact has strict typing (e.g., `Bytes<11>` for fixed-size byte arrays)
6. **Disclose**: Use `disclose()` to make private data public on-chain

## Production Deployment Script

### Complete deploy.mjs Template

```javascript
import { CompiledContract } from '@midnight-ntwrk/compact-js';
import { deployContract } from '@midnight-ntwrk/midnight-js-contracts';
import { setNetworkId, getNetworkId } from '@midnight-ntwrk/midnight-js-network-id';
import { httpClientProofProvider } from '@midnight-ntwrk/midnight-js-http-client-proof-provider';
import { indexerPublicDataProvider } from '@midnight-ntwrk/midnight-js-indexer-public-data-provider';
import { levelPrivateStateProvider } from '@midnight-ntwrk/midnight-js-level-private-state-provider';
import { NodeZkConfigProvider } from '@midnight-ntwrk/midnight-js-node-zk-config-provider';
import { WalletFacade } from '@midnight-ntwrk/wallet-sdk-facade';
import { DustWallet } from '@midnight-ntwrk/wallet-sdk-dust-wallet';
import { HDWallet, Roles } from '@midnight-ntwrk/wallet-sdk-hd';
import { ShieldedWallet } from '@midnight-ntwrk/wallet-sdk-shielded';
import { createKeystore, InMemoryTransactionHistoryStorage, PublicKey, UnshieldedWallet } from '@midnight-ntwrk/wallet-sdk-unshielded-wallet';
import * as ledger from '@midnight-ntwrk/ledger-v8';
import * as Rx from 'rxjs';
import path from 'node:path';
import fs from 'node:fs';
import { Buffer } from 'buffer';
import { WebSocket } from 'ws';

globalThis.WebSocket = WebSocket;

// Network configuration
const NETWORK_ID = 'preprod';
const INDEXER = 'https://indexer.preprod.midnight.network/api/v3/graphql';
const INDEXER_WS = 'wss://indexer.preprod.midnight.network/api/v3/graphql/ws';
const NODE = 'https://rpc.preprod.midnight.network';
const PROOF_SERVER = 'http://127.0.0.1:6300';

async function deploy() {
  setNetworkId(NETWORK_ID);

  // Load wallet from nightforge directory
  const walletDir = path.join(process.env.HOME, '.nightforge', 'wallets');
  const walletFile = fs.readdirSync(walletDir)[0];
  const walletData = JSON.parse(fs.readFileSync(path.join(walletDir, walletFile), 'utf8'));
  console.log(`Wallet: ${walletData.name} | ${walletData.address}`);

  // Load compiled contract
  const zkConfigPath = path.resolve('contracts', 'managed', 'example');
  const contractModule = await import(path.resolve(zkConfigPath, 'contract', 'index.js'));
  const compiledContract = CompiledContract.make('example', contractModule.Contract).pipe(
    CompiledContract.withVacantWitnesses,
    CompiledContract.withCompiledFileAssets(zkConfigPath),
  );
  console.log('Contract loaded.');

  // Derive keys from wallet seed
  const keys = deriveKeysFromSeed(walletData.seed);
  const shieldedSecretKeys = ledger.ZswapSecretKeys.fromSeed(keys[Roles.Zswap]);
  const dustSecretKey = ledger.DustSecretKey.fromSeed(keys[Roles.Dust]);
  const unshieldedKeystore = createKeystore(keys[Roles.NightExternal], getNetworkId());

  // Initialize wallet with proper configuration
  const walletConfig = {
    networkId: getNetworkId(),
    indexerClientConnection: { indexerHttpUrl: INDEXER, indexerWsUrl: INDEXER_WS },
    provingServerUrl: new URL(PROOF_SERVER),
    relayURL: new URL(NODE.replace(/^http/, 'ws')),
    costParameters: { additionalFeeOverhead: 300_000_000_000_000n, feeBlocksMargin: 5 },
    txHistoryStorage: new InMemoryTransactionHistoryStorage(),
  };

  console.log('Initializing wallet...');
  const wallet = await WalletFacade.init({
    configuration: walletConfig,
    shielded: (cfg) => ShieldedWallet(cfg).startWithSecretKeys(shieldedSecretKeys),
    unshielded: (cfg) => UnshieldedWallet(cfg).startWithPublicKey(PublicKey.fromKeyStore(unshieldedKeystore)),
    dust: (cfg) => DustWallet(cfg).startWithSecretKey(dustSecretKey, ledger.LedgerParameters.initialParameters().dust),
  });
  await wallet.start(shieldedSecretKeys, dustSecretKey);
  console.log('Wallet started. Syncing...');

  // Wait for wallet sync
  await Rx.firstValueFrom(wallet.state().pipe(Rx.throttleTime(5000), Rx.filter((s) => s.isSynced)));
  console.log('Wallet synced.');

  // Check balance
  let state = await Rx.firstValueFrom(wallet.state().pipe(Rx.filter((s) => s.isSynced)));
  const balance = state.unshielded.balances[ledger.unshieldedToken().raw] ?? 0n;
  console.log(`Balance: ${balance.toLocaleString()} tNight`);

  // Register UTXOs for DUST generation if needed
  if (state.dust.availableCoins.length === 0) {
    const nightUtxos = state.unshielded.availableCoins.filter((c) => c.meta?.registeredForDustGeneration !== true);
    if (nightUtxos.length > 0) {
      console.log(`Registering ${nightUtxos.length} NIGHT UTXO(s) for DUST generation...`);
      const recipe = await wallet.registerNightUtxosForDustGeneration(
        nightUtxos, unshieldedKeystore.getPublicKey(), (p) => unshieldedKeystore.signData(p),
      );
      const finalized = await wallet.finalizeRecipe(recipe);
      await wallet.submitTransaction(finalized);
      console.log('Registration submitted. Waiting for DUST...');
    }

    // Wait for DUST to accumulate
    await Rx.firstValueFrom(
      wallet.state().pipe(
        Rx.throttleTime(5000),
        Rx.filter((s) => s.isSynced),
        Rx.filter((s) => s.dust.balance(new Date()) > 0n),
      ),
    );
  }

  state = await Rx.firstValueFrom(wallet.state().pipe(Rx.filter((s) => s.isSynced)));
  const dustBal = state.dust.balance(new Date());
  console.log(`DUST balance: ${dustBal.toLocaleString()}`);

  // Build providers for contract deployment
  const walletProvider = await createWalletAndMidnightProvider({ wallet, shieldedSecretKeys, dustSecretKey, unshieldedKeystore });
  const accountId = walletProvider.getCoinPublicKey();
  const storagePassword = `${Buffer.from(accountId, 'hex').toString('base64')}!`;
  const zkConfigProvider = new NodeZkConfigProvider(zkConfigPath);

  const providers = {
    privateStateProvider: levelPrivateStateProvider({
      privateStateStoreName: 'example-private-state',
      accountId,
      privateStoragePasswordProvider: () => storagePassword,
    }),
    publicDataProvider: indexerPublicDataProvider(INDEXER, INDEXER_WS),
    zkConfigProvider,
    proofProvider: httpClientProofProvider(PROOF_SERVER, zkConfigProvider),
    walletProvider,
    midnightProvider: walletProvider,
  };

  // Deploy contract (proof generation takes 30-60 seconds)
  console.log('Deploying contract (30-60 seconds)...');
  const deployed = await deployContract(providers, {
    compiledContract,
    privateStateId: 'exampleState',
    initialPrivateState: {},
    args: [],
  });

  const contractAddress = deployed.deployTxData.public.contractAddress;
  console.log('\n=== CONTRACT DEPLOYED ===');
  console.log(`Address: ${contractAddress}`);
  console.log(`Network: ${NETWORK_ID}`);

  // Save deployment info
  fs.writeFileSync('deployment.json', JSON.stringify({
    contractAddress, 
    network: NETWORK_ID,
    deployedAt: new Date().toISOString(), 
    deployer: walletData.address,
  }, null, 2));
  console.log('Saved to deployment.json');
  
  await wallet.stop();
  process.exit(0);
}

// Helper: Derive keys from wallet seed
function deriveKeysFromSeed(seed) {
  const hdWallet = HDWallet.fromSeed(Buffer.from(seed, 'hex'));
  if (hdWallet.type !== 'seedOk') throw new Error('Invalid seed');
  const result = hdWallet.hdWallet.selectAccount(0).selectRoles([Roles.Zswap, Roles.NightExternal, Roles.Dust]).deriveKeysAt(0);
  if (result.type !== 'keysDerived') throw new Error('Key derivation failed');
  hdWallet.hdWallet.clear();
  return result.keys;
}

// Helper: Sign transaction intents
function signTransactionIntents(tx, signFn, proofMarker) {
  if (!tx.intents || tx.intents.size === 0) return;
  for (const segment of tx.intents.keys()) {
    const intent = tx.intents.get(segment);
    if (!intent) continue;
    const cloned = ledger.Intent.deserialize('signature', proofMarker, 'pre-binding', intent.serialize());
    const sigData = cloned.signatureData(segment);
    const signature = signFn(sigData);
    if (cloned.fallibleUnshieldedOffer) {
      const sigs = cloned.fallibleUnshieldedOffer.inputs.map((_, i) => cloned.fallibleUnshieldedOffer.signatures.at(i) ?? signature);
      cloned.fallibleUnshieldedOffer = cloned.fallibleUnshieldedOffer.addSignatures(sigs);
    }
    if (cloned.guaranteedUnshieldedOffer) {
      const sigs = cloned.guaranteedUnshieldedOffer.inputs.map((_, i) => cloned.guaranteedUnshieldedOffer.signatures.at(i) ?? signature);
      cloned.guaranteedUnshieldedOffer = cloned.guaranteedUnshieldedOffer.addSignatures(sigs);
    }
    tx.intents.set(segment, cloned);
  }
}

// Helper: Create wallet and midnight provider
async function createWalletAndMidnightProvider(ctx) {
  const state = await Rx.firstValueFrom(ctx.wallet.state().pipe(Rx.filter((s) => s.isSynced)));
  return {
    getCoinPublicKey() { return state.shielded.coinPublicKey.toHexString(); },
    getEncryptionPublicKey() { return state.shielded.encryptionPublicKey.toHexString(); },
    async balanceTx(tx, ttl) {
      const recipe = await ctx.wallet.balanceUnboundTransaction(tx,
        { shieldedSecretKeys: ctx.shieldedSecretKeys, dustSecretKey: ctx.dustSecretKey },
        { ttl: ttl ?? new Date(Date.now() + 30 * 60 * 1000) },
      );
      const signFn = (payload) => ctx.unshieldedKeystore.signData(payload);
      signTransactionIntents(recipe.baseTransaction, signFn, 'proof');
      if (recipe.balancingTransaction) signTransactionIntents(recipe.balancingTransaction, signFn, 'pre-proof');
      return ctx.wallet.finalizeRecipe(recipe);
    },
    submitTx(tx) { return ctx.wallet.submitTransaction(tx); },
  };
}

deploy().catch((err) => {
  console.error('DEPLOY FAILED:', err.message || err);
  if (err.stack) console.error(err.stack);
  process.exit(1);
});
```

### Deployment Script Key Components

1. **Network Configuration**: Set NETWORK_ID, INDEXER, NODE, and PROOF_SERVER URLs
2. **Wallet Loading**: Load wallet from `~/.nightforge/wallets/`
3. **Contract Loading**: Import compiled contract from `contracts/managed/`
4. **Key Derivation**: Derive Zswap, Dust, and Unshielded keys from seed
5. **Wallet Initialization**: Create WalletFacade with shielded, unshielded, and dust wallets
6. **DUST Registration**: Auto-register UTXOs for DUST generation if needed
7. **Provider Setup**: Configure all required providers (private state, public data, ZK config, proof, wallet)
8. **Contract Deployment**: Call deployContract with providers and contract config
9. **Result Saving**: Save contract address and metadata to deployment.json

## Reference

- GitHub Repository: https://github.com/Debanjannnn/Midnight-Fix
- Midnight Network: https://midnight.network/
- Compact Compiler: https://github.com/midnightntwrk/compact
- Local Dev Environment: https://github.com/midnightntwrk/midnight-local-dev
