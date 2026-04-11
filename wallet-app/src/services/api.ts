import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Network configurations
export const NETWORKS = {
  local: {
    nodeUrl: 'http://127.0.0.1:9944',
    indexerUrl: 'http://127.0.0.1:8088/api/v4/graphql',
    proofServerUrl: 'http://127.0.0.1:6300',
    networkId: 'undeployed',
  },
  preprod: {
    nodeUrl: 'https://rpc.preprod.midnight.network',
    indexerUrl: 'https://indexer.preprod.midnight.network/api/v4/graphql',
    proofServerUrl: 'https://proof-server.preprod.midnight.network',
    networkId: 'preprod',
  },
  testnet: {
    nodeUrl: 'https://rpc.testnet-02.midnight.network',
    indexerUrl: 'https://indexer.testnet-02.midnight.network/api/v4/graphql',
    proofServerUrl: 'https://proof-server.testnet-02.midnight.network',
    networkId: 'testnet-02',
  },
  mainnet: {
    nodeUrl: 'https://rpc.midnight.network',
    indexerUrl: 'https://indexer.midnight.network/api/v4/graphql',
    proofServerUrl: 'https://proof-server.midnight.network',
    networkId: 'mainnet',
  },
};

export type NetworkType = keyof typeof NETWORKS;

// API Client
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Wallet API
export const walletAPI = {
  // Generate new mnemonic
  generateMnemonic: async (): Promise<string> => {
    const response = await api.post('/wallet/generate-mnemonic');
    return response.data.mnemonic;
  },

  // Get address from mnemonic
  getAddress: async (mnemonic: string, networkId: string): Promise<{ address: string }> => {
    const response = await api.post('/wallet/get-address', { mnemonic, networkId });
    return response.data;
  },

  // Get private keys
  getPrivateKeys: async (mnemonic: string): Promise<{ privateKey: string; publicKey: string }> => {
    const response = await api.post('/wallet/get-private-keys', { mnemonic });
    return response.data;
  },

  // Get balance
  getBalance: async (address: string, networkId: string): Promise<{ dust: number; night: number }> => {
    const response = await api.post('/wallet/get-balance', { address, networkId });
    return response.data;
  },

  // Sign transaction
  signTransaction: async (tx: any, privateKey: string): Promise<any> => {
    const response = await api.post('/wallet/sign-transaction', { tx, privateKey });
    return response.data;
  },

  // Submit transaction
  submitTransaction: async (signedTx: any): Promise<{ txHash: string; status: string }> => {
    const response = await api.post('/wallet/submit-transaction', { signedTx });
    return response.data;
  },

  // Transfer unshielded
  transferUnshielded: async (
    from: string,
    to: string,
    amount: number,
    privateKey: string,
    networkId: string
  ): Promise<{ txHash: string }> => {
    const response = await api.post('/wallet/transfer-unshielded', {
      from,
      to,
      amount,
      privateKey,
      networkId,
    });
    return response.data;
  },

  // Transfer shielded
  transferShielded: async (
    from: string,
    to: string,
    amount: number,
    privateKey: string,
    networkId: string
  ): Promise<{ txHash: string }> => {
    const response = await api.post('/wallet/transfer-shielded', {
      from,
      to,
      amount,
      privateKey,
      networkId,
    });
    return response.data;
  },
};

// Indexer API
export const indexerAPI = {
  // Get contract state
  getContractState: async (address: string, indexerUrl: string): Promise<any> => {
    const response = await api.post('/indexer/get-contract-state', { address, indexerUrl });
    return response.data;
  },

  // Get transaction
  getTransaction: async (txHash: string, indexerUrl: string): Promise<any> => {
    const response = await api.post('/indexer/get-transaction', { txHash, indexerUrl });
    return response.data;
  },

  // Get latest block
  getLatestBlock: async (indexerUrl: string): Promise<any> => {
    const response = await api.post('/indexer/get-latest-block', { indexerUrl });
    return response.data;
  },

  // Check indexer health
  checkHealth: async (indexerUrl: string): Promise<boolean> => {
    const response = await api.post('/indexer/check-health', { indexerUrl });
    return response.data.isAlive;
  },
};

// Proof Server API
export const proofAPI = {
  // Generate proof
  generateProof: async (
    circuitId: string,
    privateInputs: any,
    publicInputs: any,
    proofServerUrl: string
  ): Promise<{ proof: string; publicOutputs: any }> => {
    const response = await api.post('/proof/generate', {
      circuitId,
      privateInputs,
      publicInputs,
      proofServerUrl,
    });
    return response.data;
  },

  // Check proof server health
  checkHealth: async (proofServerUrl: string): Promise<boolean> => {
    const response = await api.post('/proof/check-health', { proofServerUrl });
    return response.data.isAlive;
  },
};

// Contract API
export const contractAPI = {
  // Compile contract
  compileContract: async (contractPath: string): Promise<{ outputPath: string }> => {
    const response = await api.post('/contract/compile', { contractPath });
    return response.data;
  },

  // Deploy contract
  deployContract: async (
    contractPath: string,
    privateKey: string,
    networkId: string
  ): Promise<{ address: string; txHash: string }> => {
    const response = await api.post('/contract/deploy', { contractPath, privateKey, networkId });
    return response.data;
  },

  // Call contract method
  callContract: async (
    contractAddress: string,
    circuitId: string,
    args: any,
    privateKey: string,
    networkId: string
  ): Promise<{ txHash: string }> => {
    const response = await api.post('/contract/call', {
      contractAddress,
      circuitId,
      args,
      privateKey,
      networkId,
    });
    return response.data;
  },
};

// Node API
export const nodeAPI = {
  // Get node status
  getStatus: async (nodeUrl: string): Promise<any> => {
    const response = await api.post('/node/status', { nodeUrl });
    return response.data;
  },

  // Check node health
  checkHealth: async (nodeUrl: string): Promise<boolean> => {
    const response = await api.post('/node/check-health', { nodeUrl });
    return response.data.isAlive;
  },
};

// System API
export const systemAPI = {
  // Get all services status
  getStatus: async (network: NetworkType): Promise<{ node: boolean; indexer: boolean; prover: boolean }> => {
    const response = await api.post('/system/status', { network });
    return response.data;
  },

  // Get system info
  getInfo: async (): Promise<any> => {
    const response = await api.get('/system/info');
    return response.data;
  },
};

export default api;
