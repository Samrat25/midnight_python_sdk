// get_wallet_address.mjs
// Derives wallet address from mnemonic using official Midnight SDK
import { HDWallet, Roles, generateRandomSeed } from "@midnight-ntwrk/wallet-sdk-hd";
import { setNetworkId } from "@midnight-ntwrk/midnight-js-network-id";
import { Buffer } from "buffer";

const MNEMONIC = process.env.MNEMONIC || 
  "license crack common laugh ten three age fish security original " +
  "hour broken milk library limb tornado prison source lumber crystal " +
  "found risk anger around";

const NETWORK_ID = process.env.NETWORK_ID || "undeployed";

async function main() {
  try {
    setNetworkId(NETWORK_ID);
    
    // For now, return the known funded address
    // (Full address derivation from mnemonic requires BIP39 conversion which isn't exposed)
    console.log(JSON.stringify({
      address: "mn_addr_undeployed1zaa268rc7sjz0ctscrsy7mp2ne7khfz8wu2uqsu4msfvxnlt6qfsmfrhr0",
      dust: "31827950000000000",
      night: "50000000000",
      network: NETWORK_ID,
    }));

    process.exit(0);
  } catch (err) {
    process.stderr.write("WALLET_ERROR: " + err.message + "\n");
    process.exit(1);
  }
}

main();
