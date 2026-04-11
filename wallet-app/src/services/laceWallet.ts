/**
 * Lace Wallet Integration
 * Connects to the Lace browser extension for Midnight blockchain
 */

export interface LaceWalletAPI {
  isEnabled: () => Promise<boolean>;
  enable: () => Promise<void>;
  getBalance: () => Promise<{ night: string; dust: string }>;
  getAddress: () => Promise<string>;
  getAddresses: () => Promise<{
    shieldedAddress: string;
    unshieldedAddress: string;
    dustAddress: string;
  }>;
  signTransaction: (tx: any) => Promise<string>;
  submitTransaction: (signedTx: string) => Promise<string>;
  getNetworkId: () => Promise<string>;
  switchNetwork: (networkId: string) => Promise<void>;
}

declare global {
  interface Window {
    midnight?: {
      mnLace?: LaceWalletAPI;
    };
  }
}

export class LaceWalletService {
  private api: LaceWalletAPI | null = null;

  /**
   * Check if Lace wallet is installed
   */
  async isInstalled(): Promise<boolean> {
    return typeof window !== 'undefined' && !!window.midnight?.mnLace;
  }

  /**
   * Connect to Lace wallet
   */
  async connect(): Promise<boolean> {
    if (!await this.isInstalled()) {
      throw new Error('Lace wallet is not installed. Please install from https://www.lace.io/');
    }

    this.api = window.midnight!.mnLace!;

    try {
      const isEnabled = await this.api.isEnabled();
      if (!isEnabled) {
        await this.api.enable();
      }
      return true;
    } catch (error) {
      console.error('Failed to connect to Lace wallet:', error);
      return false;
    }
  }

  /**
   * Get wallet balance
   */
  async getBalance(): Promise<{ night: bigint; dust: bigint }> {
    if (!this.api) {
      throw new Error('Wallet not connected');
    }

    const balance = await this.api.getBalance();
    return {
      night: BigInt(balance.night),
      dust: BigInt(balance.dust),
    };
  }

  /**
   * Get wallet address
   */
  async getAddress(): Promise<string> {
    if (!this.api) {
      throw new Error('Wallet not connected');
    }

    return await this.api.getAddress();
  }

  /**
   * Get all wallet addresses
   */
  async getAddresses(): Promise<{
    shieldedAddress: string;
    unshieldedAddress: string;
    dustAddress: string;
  }> {
    if (!this.api) {
      throw new Error('Wallet not connected');
    }

    return await this.api.getAddresses();
  }

  /**
   * Sign a transaction
   */
  async signTransaction(tx: any): Promise<string> {
    if (!this.api) {
      throw new Error('Wallet not connected');
    }

    return await this.api.signTransaction(tx);
  }

  /**
   * Submit a signed transaction
   */
  async submitTransaction(signedTx: string): Promise<string> {
    if (!this.api) {
      throw new Error('Wallet not connected');
    }

    return await this.api.submitTransaction(signedTx);
  }

  /**
   * Get current network ID
   */
  async getNetworkId(): Promise<string> {
    if (!this.api) {
      throw new Error('Wallet not connected');
    }

    return await this.api.getNetworkId();
  }

  /**
   * Switch network
   */
  async switchNetwork(networkId: string): Promise<void> {
    if (!this.api) {
      throw new Error('Wallet not connected');
    }

    await this.api.switchNetwork(networkId);
  }

  /**
   * Disconnect wallet
   */
  disconnect(): void {
    this.api = null;
  }
}

// Singleton instance
export const laceWallet = new LaceWalletService();
