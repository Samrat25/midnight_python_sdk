---
inclusion: auto
description: Battle-tested patterns for deploying Midnight smart contracts using SDK 4.x and Compact 0.30.0. Includes critical workarounds for known bugs (transaction signing, vacant witnesses), CLI architecture patterns, testing with Vitest, and Docker configurations.
---

# Midnight CLI Deployment & SDK 4.x Workarounds

This skill provides battle-tested patterns for deploying Midnight smart contracts using Midnight SDK 4.x and Compact compiler 0.30.0. It includes critical workarounds for known bugs, CLI scaffolding patterns, and environment configurations.

## When to Use This Skill

Apply this skill when:
- Deploying Midnight smart contracts
- Compiling Compact 0.30.0 code
- Debugging Midnight SDK 4.x errors
- Writing integration tests for Midnight DApps
- Setting up CLI tools to interact with Midnight blockchain
- Troubleshooting transaction signing or witness-related issues

## Environment Requirements

- **Compact CLI (Compiler)**: 0.30.0
- **Midnight SDK**: 4.x (`@midnight-ntwrk/midnight-js: ^4.0.4`)
- **Node Execution**: `--no-warnings --experimental-specifier-resolution=node --loader ts-node/esm`
- **Testing**: Vitest with testcontainers
- **Logging**: Pino with pino-pretty

## Critical Known Issues & Workarounds

### 1. Contract State Constructor Argument Mismatch

**Symptom:** `Contract state constructor: expected X arguments, received Y`

**Cause:** Compact 0.30.0 constructor expects multiple arguments (e.g., `creator: Bytes<32>`), but they weren't passed in `args: []` during `deployContract`.

**Fix:** Provide arguments in the `args` array matching your `.compact` constructor signature:

```typescript
const contract = await deployContract(providers, {
  compiledContract: gameCompiledContract,
  privateStateId: 'gamePrivateState',
  initialPrivateState: privateState,
  args: [creatorBytes, maxPlayers], // MUST match constructor signature
});
```

### 2. Vacant Witnesses Error

**Symptom:** `first (witnesses) argument to Contract constructor does not contain a function-valued field`

**Cause:** Attempting to use `CompiledContract.withVacantWitnesses`. Compact 0.30.0 strictly verifies that every witness function exists during construction.

**Fix:** Provide actual witnesses instead of vacant witnesses:

```typescript
// WRONG - Don't use vacant witnesses
const contract = CompiledContract.make('game', Contract).pipe(
  CompiledContract.withVacantWitnesses, // ❌ This will fail
);

// CORRECT - Use actual witnesses
const contract = CompiledContract.make('game', Contract).pipe(
  CompiledContract.withWitnesses(witnesses), // ✅ Provide real witnesses
  CompiledContract.withCompiledFileAssets(zkConfigPath),
);
```

### 3. TypeScript Generic Type Constraint Error

**Symptom:** `Type 'Contract' is not generic`

**Cause:** New compiler output strips expected generics for Midnight SDK.

**Fix:** Bypass parameter constraints by declaring exports as `any`:

```typescript
// common-types.ts
export type GameContract = any; // Bypass generic constraints
export type GameProviders = any;
```

### 4. Transaction Signing Bug (CRITICAL)

**Symptom:** Transactions stuck indefinitely or rejected by Node

**Cause:** The `signTransactionIntents` bug in Wallet SDK. Transactions get signed but are misidentified as pre-proof intents instead of proof.

**Fix:** Implement this workaround wrapper function:

```typescript
/**
 * WORKAROUND: signTransactionIntents bug in Wallet SDK 4.x
 * 
 * Midnight SDK 4.0.4 has a known bug where wallet-sdk misidentifies
 * TransactionIntents as "pre-proof" rather than "proof", causing network
 * rejection. We MUST manually override the kind flag back to 'proof'.
 */
export const signTransactionIntents = async (
  wallet: WalletFacade,
  intents: TransactionIntent[],
): Promise<Uint8Array[]> => {
  const signed = await wallet.signTransactionIntents(intents);
  for (let i = 0; i < signed.length; i++) {
    const tx = signed[i];
    // Workaround: Patch 0x01 (pre-proof) with 0x02 (proof) at index 3
    if (intents[i].kind === 'proof' && tx.length > 3 && tx[3] === 0x01) {
      tx[3] = 0x02;
    }
  }
  return signed;
};
```

### 5. Witness Value Disclosure Compile Error

**Symptom:** `Compile Error: potential witness-value disclosure`

**Fix:** Wrap values in `.disclose()` inside your `.compact` code wherever a dynamic parameter is used in a ledger or increment step:

```compact
export circuit storeMessage(newMessage: Bytes<11>): [] {
  message = disclose(newMessage); // Use disclose() for dynamic values
}
```

## CLI Architecture Pattern

### Recommended Project Structure

```
project/
├── contract/
│   ├── src/                 # Contains .compact logic and witnesses.ts
│   ├── dist/                # Output of compactc via npm build
│   └── package.json
└── project-cli/
    ├── src/
    │   ├── api.ts           # Midnight SDK wrapper (adapter layer)
    │   ├── cli.ts           # Presentation layer & user input
    │   ├── common-types.ts  # Export wrappers around SDK/Compiler typings
    │   ├── config.ts        # Dynamic Network URLs configuration
    │   ├── preprod.ts       # Main Network initializer script
    │   └── standalone.ts    # Docker logic for local testnets
    └── package.json
```

### Layer Separation

**config.ts - Environment Configuration Layer**
- Resolves paths to compiled ZK assets
- Maintains classes for each network environment (standalone, preprod)
- Contains four critical URIs: `indexer`, `indexerWS`, `node`, `proofServer`
- **MUST** call `setNetworkId('preprod')` or `setNetworkId('undeployed')` in constructor

```typescript
import path from 'node:path';
import { setNetworkId } from '@midnight-ntwrk/midnight-js/network-id';

export const currentDir = path.resolve(new URL(import.meta.url).pathname, '..');

export const contractConfig = {
  privateStateStoreName: 'my-private-state',
  zkConfigPath: path.resolve(currentDir, '..', '..', 'contract', 'src', 'managed', 'game'),
};

export interface Config {
  readonly logDir: string;
  readonly indexer: string;
  readonly indexerWS: string;
  readonly node: string;
  readonly proofServer: string;
}

/** Local Standalone Testnet Configuration */
export class StandaloneConfig implements Config {
  logDir = path.resolve(currentDir, '..', 'logs', 'standalone', `${new Date().toISOString()}.log`);
  indexer = 'http://127.0.0.1:8088/api/v3/graphql';
  indexerWS = 'ws://127.0.0.1:8088/api/v3/graphql/ws';
  node = 'http://127.0.0.1:9944';
  proofServer = 'http://127.0.0.1:6300';
  constructor() {
    setNetworkId('undeployed');
  }
}

/** Official Midnight Preprod Configuration */
export class PreprodConfig implements Config {
  logDir = path.resolve(currentDir, '..', 'logs', 'preprod', `${new Date().toISOString()}.log`);
  indexer = 'https://indexer.preprod.midnight.network/api/v3/graphql';
  indexerWS = 'wss://indexer.preprod.midnight.network/api/v3/graphql/ws';
  node = 'https://rpc.preprod.midnight.network';
  proofServer = 'http://127.0.0.1:6300'; // Local proxy to preprod
  constructor() {
    setNetworkId('preprod'); // REQUIRED for signatures to work
  }
}
```

**common-types.ts - Type Boundary Layer**
- Prevents TypeScript confusion from dynamic compiler outputs
- Maps `Contract<any>` to simple exports
- Defines Private State structures locally

```typescript
export type GameContract = any; // Bypass generic constraints
export type GameProviders = any;
export type DeployedGameContract = any;
```

**api.ts - Adapter Layer**
- Zero knowledge of CLI prompts
- Wraps `@midnight-ntwrk/midnight-js`
- Contains `signTransactionIntents` workaround
- Compiles contract pipeline
- Exposes clean methods like `deploy()` and `join()`
- Uses `as any` casting to resolve type conflicts

```typescript
import { Contract, ledger, witnesses } from '@framed/contract';
import { deployContract } from '@midnight-ntwrk/midnight-js/contracts';
import { CompiledContract } from '@midnight-ntwrk/compact-js';
import { WebSocket } from 'ws';

// Required for GraphQL subscriptions in Node.js
globalThis.WebSocket = WebSocket as any;

// CompiledContract Pipeline with actual witnesses
const gameCompiledContract = ((CompiledContract as any).make('game', Contract)).pipe(
  (CompiledContract as any).withWitnesses(witnesses), 
  (CompiledContract as any).withCompiledFileAssets(zkConfigPath),
) as any;

export const deploy = async (
  providers: GameProviders,
  privateState: any,
  creator: Uint8Array,
  maxPlayers: bigint,
): Promise<DeployedGameContract> => {
  const gameContract = await deployContract(providers as any, {
    compiledContract: gameCompiledContract,
    privateStateId: 'gamePrivateState',
    initialPrivateState: privateState,
    args: [creator, maxPlayers], // Match constructor signature
  });
  return gameContract;
};
```

**cli.ts - Presentation Layer**
- Listens to stdin
- Uses `console.log` and `inquire` prompts
- Delegates actions to `api.ts`
- Subscribes to Wallet and Dust state via RxJS Observables

**standalone.ts & preprod.ts - Bootstrappers**
- Initializes Docker networks for test environments (standalone)
- Configures Midnight Node, Proof Server, and Indexer URLs
- Executes WalletFacade builder
- Injects WalletContext and Providers into cli.ts

## Package.json Scripts Pattern

```json
{
  "scripts": {
    "typecheck": "tsc -p tsconfig.json --noEmit",
    "build": "rm -rf dist && tsc --project tsconfig.build.json",
    
    "standalone": "docker compose -f standalone.yml pull && node --no-warnings --experimental-specifier-resolution=node --loader ts-node/esm src/standalone.ts",
    
    "preprod": "node --no-warnings --experimental-specifier-resolution=node --loader ts-node/esm src/preprod.ts",
    "preprod-ps": "docker compose -f proof-server.yml pull && docker compose -f proof-server.yml up -d",
    
    "test": "docker compose -f standalone.yml pull && DEBUG='testcontainers' vitest run"
  }
}
```

### Command Explanations

1. **`npm run standalone`**: Executes entirely locally, bootstraps DockerComposeEnvironment on standard ports (9944, 8088, 6300)

2. **`npm run preprod` and `npm run preprod-ps`**: 
   - Preprod network uses remote Indexers and Node URLs
   - Midnight doesn't provide open Proof Server URI
   - Must first run `npm run preprod-ps` to boot local proof server
   - Then run `npm run preprod` for CLI interactions

3. **ESM Resolution**: Always use experimental flags:
   ```bash
   node --no-warnings --experimental-specifier-resolution=node --loader ts-node/esm src/YOUR_TARGET.ts
   ```

## Docker & Proof Servers

You cannot deploy a contract without a Proof Server.

**Standalone**: testcontainers orchestrates Local Node, Indexer, and Proof Server automatically

**Preprod**: Deploy your own proof server container:

```yaml
# proof-server.yml
services:
  proof-server:
    image: ghcr.io/midnight-ntwrk/proof-server:4.2.0
    ports:
      - "6300:6300"
    environment:
      - NETWORK_NAME=preprod
      - NODE_URL=https://rpc.preprod.midnight.network
```

## Testing with Vitest & Testcontainers

### Test Pattern

```typescript
import { describe, it, beforeAll, afterAll, expect } from 'vitest';
import { DockerComposeEnvironment, StartedDockerComposeEnvironment } from 'testcontainers';
import { StandaloneConfig } from './config.js';
import * as api from './api.js';

describe('Game Contract Integration', () => {
  let dockerEnv: StartedDockerComposeEnvironment;
  let testProviders: api.GameProviders;
  let testWallet: api.WalletContext;

  beforeAll(async () => {
    // 1. Boot standalone Node, Indexer, and Proof Server
    const env = new DockerComposeEnvironment(path.resolve(currentDir, '..'), 'standalone.yml');
    dockerEnv = await env.up();
    
    // 2. Map standard standalone ports
    const config = new StandaloneConfig();
    
    // 3. Generate fresh randomized seed for testing
    const seed = api.generateRandomSeed();
    const logger = await createLogger('test.log');

    // 4. Initialize Midnight Providers over local containers
    testProviders = await api.initializeProviders(config, logger);
    testWallet = await api.buildWallet(testProviders, seed);
    
    // 5. Register for DUST generation (CRITICAL)
    await api.registerForDustGeneration(testWallet.wallet);
  }, 60000); // Large timeout for container booting

  afterAll(async () => {
    await dockerEnv.down();
  });

  it('should deploy the contract via test wallet', async () => {
    const dummyHostKey = new Uint8Array(32).fill(0xee);
    const contract = await api.deploy(testProviders, {
      role: 0,
      myVote: 0,
      witnessedEvents: []
    }, dummyHostKey, 10n);

    expect(contract.deployTxData.public.contractAddress).toBeDefined();
  }, 30000); // 30 second timeout for ZK-proof generation
});
```

### Testing Best Practices

1. **Timeouts**: Testcontainers take 20+ seconds to boot, ZK proofs take 2-5 seconds. Override `beforeAll` and `it` timeouts heavily.

2. **DUST Funding**: New wallets from `generateRandomSeed()` have zero DUST. Tests crash on deployment unless `registerForDustGeneration()` is explicitly run.

3. **Observables**: Wrap ledger state validations in promises checking for specific states due to variable block propagation latency.

## Logging with Pino

### Logger Setup

```typescript
import * as path from 'node:path';
import * as fs from 'node:fs/promises';
import pinoPretty from 'pino-pretty';
import pino from 'pino';
import { createWriteStream } from 'node:fs';

export const createLogger = async (logPath: string): Promise<pino.Logger> => {
  // Ensure logging directory exists
  await fs.mkdir(path.dirname(logPath), { recursive: true });
  
  // Configure pretty stream for terminal output
  const pretty: pinoPretty.PrettyStream = pinoPretty({
    colorize: true,
    sync: true, // Ensures CLI prompts aren't overwritten
  });
  
  const level = process.env.DEBUG_LEVEL || 'info';

  // Pipe logs to both console and file
  return pino(
    { level, depthLimit: 20 },
    pino.multistream([
      { stream: pretty, level },
      { stream: createWriteStream(logPath), level },
    ]),
  );
};
```

### Usage

```typescript
const logger = await createLogger(config.logDir);

logger.info(`Deployed contract at address: ${contractAddress}`);
logger.warn('Preproof transaction identified. Executing workaround override...');
```

## Deployment Checklist

When deploying or integrating a contract CLI:

- [ ] Update Compact pragma to `>= 0.22` and add `.disclose()` where needed
- [ ] Implement complete witnesses (never use vacant witnesses)
- [ ] Fix `Contract` generic type constraints with `any` casting
- [ ] Scaffold network config (`config.ts`) with proper `setNetworkId()`
- [ ] Update `CompiledContract` pipeline in `api.ts` with actual witnesses
- [ ] Apply `signTransactionIntents` workaround
- [ ] Bootstrap environments (`standalone.ts` & `preprod.ts`)
- [ ] Set up proper logging with Pino
- [ ] Configure package.json scripts with ESM flags
- [ ] Write integration tests with testcontainers

## Common Error Solutions Quick Reference

| Error | Solution |
|-------|----------|
| Constructor argument mismatch | Pass args matching .compact constructor |
| Vacant witnesses error | Use `withWitnesses(witnesses)` not `withVacantWitnesses` |
| Type 'Contract' is not generic | Export types as `any` |
| Transactions stuck/rejected | Apply signTransactionIntents workaround |
| Witness-value disclosure | Wrap values in `.disclose()` |
| ESM resolution errors | Use `--experimental-specifier-resolution=node` flag |
| Test timeouts | Increase timeouts to 30-60 seconds |
| No DUST for deployment | Call `registerForDustGeneration()` |

## Reference

- GitHub Repository: https://github.com/soumyacodes007/Midnight-deploy-cli
- Midnight SDK: https://docs.midnight.network/
- Compact Compiler: https://github.com/midnightntwrk/compact
- Testcontainers: https://testcontainers.com/
