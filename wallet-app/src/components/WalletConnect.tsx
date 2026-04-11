import React, { useState, useEffect } from 'react';
import { Wallet, ExternalLink, AlertCircle, CheckCircle } from 'lucide-react';
import { laceWallet } from '../services/laceWallet';
import { useWalletStore } from '../store/walletStore';

export const WalletConnect: React.FC = () => {
  const [laceInstalled, setLaceInstalled] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [laceConnected, setLaceConnected] = useState(false);
  const [laceAddress, setLaceAddress] = useState<string | null>(null);

  const { wallets } = useWalletStore();

  useEffect(() => {
    checkLaceWallet();
  }, []);

  const checkLaceWallet = async () => {
    const installed = await laceWallet.isInstalled();
    setLaceInstalled(installed);
  };

  const connectLaceWallet = async () => {
    setConnecting(true);
    setError(null);

    try {
      const connected = await laceWallet.connect();
      if (connected) {
        const address = await laceWallet.getAddress();
        setLaceConnected(true);
        setLaceAddress(address);
      } else {
        setError('Failed to connect to Lace wallet');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to connect to Lace wallet');
    } finally {
      setConnecting(false);
    }
  };

  const disconnectLaceWallet = () => {
    laceWallet.disconnect();
    setLaceConnected(false);
    setLaceAddress(null);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Connect Wallet</h1>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-red-800 font-medium">Connection Error</p>
            <p className="text-red-600 text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        {/* Lace Wallet */}
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-midnight-200 hover:border-midnight-400 transition">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-midnight-500 to-midnight-700 rounded-xl flex items-center justify-center">
                <Wallet className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold">Lace Wallet</h3>
                <p className="text-sm text-gray-600">Browser Extension</p>
              </div>
            </div>
            {laceConnected && (
              <CheckCircle className="w-6 h-6 text-green-500" />
            )}
          </div>

          <p className="text-sm text-gray-600 mb-4">
            Official Midnight wallet with full support for shielded transactions and ZK proofs.
          </p>

          {laceConnected ? (
            <div className="space-y-3">
              <div className="p-3 bg-green-50 rounded-lg">
                <p className="text-xs text-green-700 font-medium mb-1">Connected</p>
                <p className="text-sm text-green-900 font-mono break-all">
                  {laceAddress?.slice(0, 20)}...{laceAddress?.slice(-10)}
                </p>
              </div>
              <button
                onClick={disconnectLaceWallet}
                className="w-full px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg font-medium transition"
              >
                Disconnect
              </button>
            </div>
          ) : (
            <>
              {laceInstalled ? (
                <button
                  onClick={connectLaceWallet}
                  disabled={connecting}
                  className="w-full px-4 py-3 bg-midnight-600 hover:bg-midnight-700 text-white rounded-lg font-medium transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {connecting ? 'Connecting...' : 'Connect Lace Wallet'}
                </button>
              ) : (
                <a
                  href="https://www.lace.io/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full px-4 py-3 bg-midnight-600 hover:bg-midnight-700 text-white rounded-lg font-medium transition flex items-center justify-center gap-2"
                >
                  Install Lace Wallet
                  <ExternalLink className="w-4 h-4" />
                </a>
              )}
            </>
          )}

          <div className="mt-4 pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-500">
              ✓ Shielded transactions<br />
              ✓ ZK proof generation<br />
              ✓ Multi-network support<br />
              ✓ Hardware wallet compatible
            </p>
          </div>
        </div>

        {/* Native Wallet */}
        <div className="bg-white rounded-xl shadow-lg p-6 border-2 border-gray-200 hover:border-gray-300 transition">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-gray-500 to-gray-700 rounded-xl flex items-center justify-center">
                <Wallet className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold">Native Wallet</h3>
                <p className="text-sm text-gray-600">Built-in Wallet</p>
              </div>
            </div>
            {wallets.length > 0 && (
              <CheckCircle className="w-6 h-6 text-green-500" />
            )}
          </div>

          <p className="text-sm text-gray-600 mb-4">
            Create or import a wallet directly in the app with encrypted storage.
          </p>

          {wallets.length > 0 ? (
            <div className="space-y-3">
              <div className="p-3 bg-blue-50 rounded-lg">
                <p className="text-xs text-blue-700 font-medium mb-1">
                  {wallets.length} Wallet{wallets.length > 1 ? 's' : ''} Available
                </p>
                <p className="text-sm text-blue-900">
                  {wallets[0].name}
                </p>
              </div>
              <button
                onClick={() => window.location.href = '/dashboard'}
                className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition"
              >
                Open Dashboard
              </button>
            </div>
          ) : (
            <div className="space-y-2">
              <button
                onClick={() => window.location.href = '/create'}
                className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition"
              >
                Create New Wallet
              </button>
              <button
                onClick={() => window.location.href = '/import'}
                className="w-full px-4 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg font-medium transition"
              >
                Import Wallet
              </button>
            </div>
          )}

          <div className="mt-4 pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-500">
              ✓ Encrypted storage<br />
              ✓ Password protected<br />
              ✓ Multi-wallet support<br />
              ✓ Export/backup options
            </p>
          </div>
        </div>
      </div>

      {/* Information Section */}
      <div className="mt-8 p-6 bg-blue-50 rounded-xl">
        <h3 className="text-lg font-bold mb-3">Which wallet should I use?</h3>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <h4 className="font-semibold text-midnight-700 mb-2">Use Lace Wallet if:</h4>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• You want the official Midnight wallet</li>
              <li>• You need hardware wallet support</li>
              <li>• You use multiple DApps</li>
              <li>• You want browser extension convenience</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-blue-700 mb-2">Use Native Wallet if:</h4>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• You want a simple, integrated experience</li>
              <li>• You don't want to install extensions</li>
              <li>• You need multiple wallets in one place</li>
              <li>• You prefer web-based wallets</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
