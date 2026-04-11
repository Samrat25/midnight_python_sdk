import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import CryptoJS from 'crypto-js';
import { NetworkType } from '../services/api';

interface Wallet {
  id: string;
  name: string;
  address: string;
  encryptedMnemonic: string;
  createdAt: number;
}

interface WalletState {
  wallets: Wallet[];
  currentWallet: Wallet | null;
  currentNetwork: NetworkType;
  isLocked: boolean;
  password: string | null;

  // Actions
  createWallet: (name: string, mnemonic: string, address: string, password: string) => void;
  importWallet: (name: string, mnemonic: string, address: string, password: string) => void;
  selectWallet: (id: string) => void;
  deleteWallet: (id: string) => void;
  switchNetwork: (network: NetworkType) => void;
  lock: () => void;
  unlock: (password: string) => boolean;
  getMnemonic: (walletId: string, password: string) => string | null;
}

const encryptMnemonic = (mnemonic: string, password: string): string => {
  return CryptoJS.AES.encrypt(mnemonic, password).toString();
};

const decryptMnemonic = (encryptedMnemonic: string, password: string): string | null => {
  try {
    const bytes = CryptoJS.AES.decrypt(encryptedMnemonic, password);
    const decrypted = bytes.toString(CryptoJS.enc.Utf8);
    return decrypted || null;
  } catch {
    return null;
  }
};

export const useWalletStore = create<WalletState>()(
  persist(
    (set, get) => ({
      wallets: [],
      currentWallet: null,
      currentNetwork: 'preprod',
      isLocked: true,
      password: null,

      createWallet: (name, mnemonic, address, password) => {
        const wallet: Wallet = {
          id: Date.now().toString(),
          name,
          address,
          encryptedMnemonic: encryptMnemonic(mnemonic, password),
          createdAt: Date.now(),
        };

        set((state) => ({
          wallets: [...state.wallets, wallet],
          currentWallet: wallet,
          password,
          isLocked: false,
        }));
      },

      importWallet: (name, mnemonic, address, password) => {
        const wallet: Wallet = {
          id: Date.now().toString(),
          name,
          address,
          encryptedMnemonic: encryptMnemonic(mnemonic, password),
          createdAt: Date.now(),
        };

        set((state) => ({
          wallets: [...state.wallets, wallet],
          currentWallet: wallet,
          password,
          isLocked: false,
        }));
      },

      selectWallet: (id) => {
        const wallet = get().wallets.find((w) => w.id === id);
        if (wallet) {
          set({ currentWallet: wallet });
        }
      },

      deleteWallet: (id) => {
        set((state) => ({
          wallets: state.wallets.filter((w) => w.id !== id),
          currentWallet: state.currentWallet?.id === id ? null : state.currentWallet,
        }));
      },

      switchNetwork: (network) => {
        set({ currentNetwork: network });
      },

      lock: () => {
        set({ isLocked: true, password: null });
      },

      unlock: (password) => {
        const { wallets } = get();
        if (wallets.length === 0) {
          set({ isLocked: false, password });
          return true;
        }

        // Try to decrypt the first wallet's mnemonic to verify password
        const firstWallet = wallets[0];
        const decrypted = decryptMnemonic(firstWallet.encryptedMnemonic, password);

        if (decrypted) {
          set({ isLocked: false, password });
          return true;
        }

        return false;
      },

      getMnemonic: (walletId, password) => {
        const wallet = get().wallets.find((w) => w.id === walletId);
        if (!wallet) return null;

        return decryptMnemonic(wallet.encryptedMnemonic, password);
      },
    }),
    {
      name: 'midnight-wallet-storage',
      partialize: (state) => ({
        wallets: state.wallets,
        currentWallet: state.currentWallet,
        currentNetwork: state.currentNetwork,
      }),
    }
  )
);
