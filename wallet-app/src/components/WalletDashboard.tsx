import React, { useEffect, useState } from 'react';
import { useWalletStore } from '../store/walletStore';
import { walletAPI, NETWORKS } from '../services/api';
import { Wallet, Send, ArrowDownUp, History, Settings, Copy, ExternalLink } from 'lucide-react';

export const WalletDashboard: React.FC = () => {
  const { currentWallet, currentNetwork } = useWalletStore();
  const [balance, setBalance] = useState({ dust: 0, night: 0 });
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (currentWallet) {
      loadBalance();
    }
  }, [currentWallet, currentNetwork]);

  const loadBalance = async () => {
    if (!currentWallet) return;

    setLoading(true);
    try {
      const networkConfig = NETWORKS[currentNetwork];
      const balanceData = await walletAPI.getBalance(currentWallet.address, networkConfig.networkId);
      setBalance(balanceData);
    } catch (error) {
      console.error('Failed to load balance:', error);
    } finally {
      setLoading(false);
    }
  };

  const copyAddress = () => {
    if (currentWallet) {
      navigator.clipboard.writeText(currentWallet.address);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const formatAddress = (address: string) => {
    return `${address.slice(0, 10)}...${address.slice(-8)}`;
  };

  const formatBalance = (amount: number) => {
    return (amount / 1_000_000).toFixed(6);
  };

  if (!currentWallet) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <Wallet className="w-16 h-16 mx-auto mb-4 text-midnight-400" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">No Wallet Selected</h2>
          <p className="text-gray-600">Create or import a wallet to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Wallet Header */}
      <div className="bg-gradient-to-r from-midnight-600 to-midnight-800 rounded-2xl p-6 text-white mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold">{currentWallet.name}</h2>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-sm opacity-80">{formatAddress(currentWallet.address)}</span>
              <button
                onClick={copyAddress}
                className="p-1 hover:bg-white/20 rounded transition"
                title="Copy address"
              >
                {copied ? (
                  <span className="text-xs">✓ Copied</span>
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </button>
              <a
                href={`https://explorer.midnight.network/address/${currentWallet.address}`}
                target="_blank"
                rel="noopener noreferrer"
                className="p-1 hover:bg-white/20 rounded transition"
                title="View on explorer"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm opacity-80">Network</div>
            <div className="text-lg font-semibold capitalize">{currentNetwork}</div>
          </div>
        </div>

        {/* Balance */}
        <div className="grid grid-cols-2 gap-4 mt-6">
          <div className="bg-white/10 rounded-xl p-4">
            <div className="text-sm opacity-80 mb-1">DUST Balance</div>
            <div className="text-3xl font-bold">
              {loading ? '...' : formatBalance(balance.dust)}
            </div>
            <div className="text-xs opacity-60 mt-1">Transaction Fees</div>
          </div>
          <div className="bg-white/10 rounded-xl p-4">
            <div className="text-sm opacity-80 mb-1">NIGHT Balance</div>
            <div className="text-3xl font-bold">
              {loading ? '...' : formatBalance(balance.night)}
            </div>
            <div className="text-xs opacity-60 mt-1">Shielded Token</div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <button className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl shadow hover:shadow-md transition">
          <Send className="w-6 h-6 text-midnight-600" />
          <span className="text-sm font-medium">Send</span>
        </button>
        <button className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl shadow hover:shadow-md transition">
          <ArrowDownUp className="w-6 h-6 text-midnight-600" />
          <span className="text-sm font-medium">Swap</span>
        </button>
        <button className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl shadow hover:shadow-md transition">
          <History className="w-6 h-6 text-midnight-600" />
          <span className="text-sm font-medium">History</span>
        </button>
        <button className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl shadow hover:shadow-md transition">
          <Settings className="w-6 h-6 text-midnight-600" />
          <span className="text-sm font-medium">Settings</span>
        </button>
      </div>

      {/* Recent Transactions */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-lg font-bold mb-4">Recent Transactions</h3>
        <div className="text-center text-gray-500 py-8">
          No transactions yet
        </div>
      </div>
    </div>
  );
};
