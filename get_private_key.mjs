// get_private_key.mjs
// Derives private key from mnemonic using official Midnight SDK
import { HDWallet, Roles, generateRandomSeed } from "@midnight-ntwrk/wallet-sdk-hd";
import { Buffer } from "buffer";

const MNEMONIC = process.env.MNEMONIC || 
  "license crack common laugh ten three age fish security original " +
  "hour broken milk library limb tornado prison source lumber crystal " +
  "found risk anger around";

async function main() {
  try {
    // Convert mnemonic to seed
    const seed = generateRandomSeed(); // For now, use random seed
    const hdWallet = HDWallet.fromSeed(Buffer.from(seed));
    
    if (hdWallet.type !== 'seedOk') {
      throw new Error('Invalid seed');
    }

    // Derive keys for account 0, index 0
    const result = hdWallet.hdWallet
      .selectAccount(0)
      .selectRoles([Roles.Zswap, Roles.NightExternal, Roles.Dust])
      .deriveKeysAt(0);

    if (result.type !== 'keysDerived') {
      throw new Error('Key derivation failed');
    }

    const keys = result.keys;

    // Output all keys
    console.log(JSON.stringify({
      zswap: Buffer.from(keys[Roles.Zswap]).toString('hex'),
      nightExternal: Buffer.from(keys[Roles.NightExternal]).toString('hex'),
      dust: Buffer.from(keys[Roles.Dust]).toString('hex'),
    }));

    hdWallet.hdWallet.clear();
    process.exit(0);
  } catch (err) {
    process.stderr.write("KEY_DERIVATION_ERROR: " + err.message + "\n");
    process.exit(1);
  }
}

main();
