---
inclusion: auto
description: Production reference for building privacy-preserving NFT applications on Midnight Network with shielded state, ZK proofs, commitment-based ownership, and multi-contract factory patterns.
---

# Midnight NFT Launchpad - Shielded NFT Reference

Complete reference for building privacy-preserving NFT applications on Midnight Network with shielded state, ZK proofs, and factory patterns.

## Core Concepts

### Shielded NFTs
- **Ownership**: Hidden as cryptographic commitment hash
- **Metadata**: Private, only owner knows actual data
- **Verification**: ZK proofs verify ownership without revealing identity
- **On-chain**: Only `hash(ownerAddress, metadataHash)` stored publicly

### Multi-Contract Factory Pattern
- Base contract for simple NFTs
- Collection factory for independent instances with supply caps
- Each collection is a separate deployed contract

## Contract Patterns

### Commitment-Based Ownership

```compact
// Create commitment
circuit hashTokenData(owner: Bytes<32>, metadataHash: Bytes<32>): Bytes<32> {
    return persistentHash<Vector<2, Bytes<32>>>([owner, metadataHash]);
}

export circuit mint(metadataHash: Bytes<32>): [] {
    const caller = disclose(callerAddress());
    const commitment = hashTokenData(caller, metadataHash);
    tokenCommitments.insert(tokenId, disclose(commitment));
}
```

### Supply Cap Enforcement

```compact
constructor(name: Bytes<32>, desc: Bytes<64>, cap: Uint<64>) {
    maxSupply = disclose(cap);
    totalSupply = 0;
}

export circuit mint(metadataHash: Bytes<32>): [] {
    assert(totalSupply < maxSupply, "Collection supply reached");
    // ... mint logic
}
```

## TypeScript Implementation

### Witness Functions

```typescript
const callerAddressBytes = crypto.createHash('sha256')
  .update(walletAddressString)
  .digest();

const compiled = CompiledContract.make('collection', Contract).pipe(
  CompiledContract.withWitnesses({
    callerAddress: (context: any) => [context.privateState as never, callerAddressBytes]
  }),
  CompiledContract.withCompiledFileAssets(zkConfigPath),
);
```

### Multi-Contract Loading

```typescript
// Different paths for different contracts
const BASE_CONTRACT_PATH = 'contracts/managed/contract';
const COLLECTION_CONTRACT_PATH = 'contracts/managed/collection';

export async function getContractModule(contractName: 'contract' | 'collection') {
  const basePath = contractName === 'collection' 
    ? COLLECTION_CONTRACT_PATH 
    : BASE_CONTRACT_PATH;
  return import(pathToFileURL(path.join(basePath, 'contract', 'index.js')).href);
}
```

### Creating Collections

```typescript
export async function createCollection(seed: string, name: string, description: string, maxSupply: number) {
  const walletCtx = await createWallet(seed);
  await walletCtx.wallet.waitForSyncedState();
  
  const callerAddressBytes = crypto.createHash('sha256')
    .update(walletCtx.unshieldedKeystore.getBech32Address().toString())
    .digest();

  const collectionZkPath = path.resolve('contracts/managed/collection');
  const providers = await createProviders(walletCtx, collectionZkPath);
  
  // Pad to fixed sizes
  const nameBytes = Buffer.alloc(32);
  nameBytes.write(name);
  const descBytes = Buffer.alloc(64);
  descBytes.write(description);

  const deployed = await deployContract(providers, {
    compiledContract: compiledCollection,
    args: [nameBytes, descBytes, BigInt(maxSupply)]
  });

  return deployed.deployTxData.public.contractAddress;
}
```

### Minting NFTs

```typescript
export async function mintFromCollection(seed: string, contractAddress: string, metadata: string) {
  const walletCtx = await createWallet(seed);
  await walletCtx.wallet.waitForSyncedState();
  
  const metadataHashBytes = crypto.createHash('sha256').update(metadata).digest();
  
  const contract = await findDeployedContract(providers, {
    contractAddress,
    compiledContract: compiledCollection,
  });

  const tx = await contract.callTx.mint(metadataHashBytes);
  
  // Store metadata locally for later verification
  addOwnedToken(tokenId, toHex(metadataHashBytes), metadata, tx.public.txId, contractAddress);
}
```

## Key Patterns

### 1. Caller Address Hashing
Always hash wallet address for witness data:
```typescript
const callerAddressBytes = crypto.createHash('sha256')
  .update(walletAddressString)
  .digest();
```

### 2. Fixed-Size Byte Padding
Pad strings to match `Bytes<N>` types:
```typescript
const nameBytes = Buffer.alloc(32);
nameBytes.write(name);
```

### 3. Local State Management
Store private metadata locally:
```typescript
export function addOwnedToken(tokenId: string, metadataHash: string, metadata: string) {
  const state = loadState();
  state.ownedTokens.push({ tokenId, metadataHash, metadata });
  saveState(state);
}
```

### 4. Reading Ledger State
Query contract state to read public ledger:
```typescript
const state = await providers.publicDataProvider.queryContractState(contractAddress);
const ledgerState = collectionModule.ledger(state!.data);
const currentSupply = ledgerState.totalSupply;
```

## Environment Setup

```bash
# .env
PRIVATE_STATE_PASSWORD=YourStrongPasswordHere
WALLET_SEED=your_hex_seed_here
```

## Package.json

```json
{
  "type": "module",
  "scripts": {
    "compile": "compact compile contracts/contract.compact contracts/managed/contract && compact compile contracts/collection.compact contracts/managed/collection",
    "start-proof-server": "docker run -p 6300:6300 midnightntwrk/proof-server:8.0.3 -- midnight-proof-server -v",
    "cli": "tsx src/cli.ts"
  },
  "dependencies": {
    "@midnight-ntwrk/compact-runtime": "0.15.0",
    "@midnight-ntwrk/ledger-v8": "8.0.3",
    "@midnight-ntwrk/midnight-js-contracts": "4.0.2",
    "@midnight-ntwrk/wallet-sdk-facade": "3.0.0"
  }
}
```

## CLI Commands

```bash
# Deploy base contract
npm run cli -- deploy

# Create collection
npm run cli -- create-collection "Collection Name" "Description" 1000

# Mint from collection
npm run cli -- mint-from-collection <CONTRACT_ADDRESS> '{"rarity": "legendary"}'

# Verify ownership
npm run cli -- verify <TOKEN_ID> <CONTRACT_ADDRESS> '{"metadata": "data"}'

# Transfer NFT
npm run cli -- transfer <TOKEN_ID> <RECIPIENT_ADDRESS> <CONTRACT_ADDRESS> '{"metadata": "data"}'
```

## Best Practices

1. **Hash caller addresses** with SHA-256 for witness data
2. **Pad fixed-size bytes** using `Buffer.alloc(N)`
3. **Store metadata locally** in state management
4. **Use separate ZK paths** for different contract types
5. **Wait for sync** with `wallet.waitForSyncedState()`
6. **Enforce supply caps** in circuits with `assert()`
7. **Verify commitments** before transfers
8. **Clean up wallets** with `wallet.stop()`

## Reference

- GitHub: https://github.com/tusharpamnani/midnight-nft-launchpad
- Midnight SDK: 4.x with ledger-v8 8.0.3
- Compact: 0.22
- Pattern: Factory-based multi-contract NFT system
