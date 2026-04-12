// Midnight Wallet V2 - With CLI Integration and Shielded/Unshielded Transfers
const API_BASE = 'http://localhost:8000';

let currentWallet = {
    mnemonic: null,
    address: null,
    balance: { dust: 0, night: 0 },
    transferType: 'unshielded' // 'unshielded' or 'shielded'
};

let transactions = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSavedWallet();
    loadTransactions();
    
    // Add input listeners
    const amountInput = document.getElementById('transferAmount');
    if (amountInput) {
        amountInput.addEventListener('input', updateTransferSummary);
    }
    
    // Auto-refresh balance every 10 seconds if wallet is loaded
    setInterval(() => {
        if (currentWallet.address) {
            refreshBalance();
        }
    }, 10000);
});

// View Management
function switchView(viewName) {
    // Update nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.view === viewName) {
            item.classList.add('active');
        }
    });
    
    // Update views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    document.getElementById(`${viewName}-view`).classList.add('active');
    
    // Update receive address
    if (viewName === 'receive' && currentWallet.address) {
        document.getElementById('receiveAddress').textContent = currentWallet.address;
    }
    
    // Load activity
    if (viewName === 'activity') {
        displayTransactions();
    }
}

// Transfer Type Selection
function selectTransferType(type) {
    currentWallet.transferType = type;
    
    document.querySelectorAll('.type-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.type === type) {
            btn.classList.add('active');
        }
    });
}

// Modal Management
function showImportModal() {
    document.getElementById('importModal').classList.add('active');
}

function showCreateModal() {
    document.getElementById('createModal').classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Wallet Management
async function createWallet() {
    const btn = document.getElementById('createBtn');
    btn.innerHTML = '<span class="loading"></span> Generating...';
    btn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/wallet/generate-mnemonic`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) throw new Error('Failed to generate mnemonic');
        
        const data = await response.json();
        const mnemonic = data.mnemonic;
        
        document.getElementById('newMnemonicText').textContent = mnemonic;
        document.getElementById('newMnemonicDisplay').classList.remove('hidden');
        document.getElementById('mnemonicInput').value = mnemonic;
        
        showMessage('createMessage', '✅ Wallet generated! Save your recovery phrase securely.', 'success');
        
        // Auto import after 2 seconds
        setTimeout(async () => {
            closeModal('createModal');
            await importWallet();
        }, 2000);
        
        btn.textContent = 'Generate';
        btn.disabled = false;
    } catch (error) {
        showMessage('createMessage', `Error: ${error.message}`, 'error');
        btn.textContent = 'Generate';
        btn.disabled = false;
    }
}

async function importWallet() {
    const mnemonic = document.getElementById('mnemonicInput').value.trim();
    
    if (!mnemonic) {
        showMessage('importMessage', 'Please enter a recovery phrase', 'error');
        return;
    }
    
    const words = mnemonic.split(/\s+/);
    if (words.length !== 24) {
        showMessage('importMessage', 'Recovery phrase must be exactly 24 words', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/wallet/get-address`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mnemonic: mnemonic,
                networkId: 'undeployed'
            })
        });
        
        if (!response.ok) throw new Error('Failed to derive address');
        
        const data = await response.json();
        currentWallet.mnemonic = mnemonic;
        currentWallet.address = data.address;
        
        localStorage.setItem('midnight_wallet_mnemonic', mnemonic);
        localStorage.setItem('midnight_wallet_address', data.address);
        
        document.getElementById('walletAddress').textContent = data.address;
        document.getElementById('wallet-empty').classList.add('hidden');
        document.getElementById('wallet-loaded').classList.remove('hidden');
        
        await refreshBalance();
        
        closeModal('importModal');
        showMessage('importMessage', '✅ Wallet imported successfully!', 'success');
    } catch (error) {
        showMessage('importMessage', `Error: ${error.message}`, 'error');
    }
}

async function loadSavedWallet() {
    const savedMnemonic = localStorage.getItem('midnight_wallet_mnemonic');
    const savedAddress = localStorage.getItem('midnight_wallet_address');
    
    if (savedMnemonic && savedAddress) {
        document.getElementById('mnemonicInput').value = savedMnemonic;
        currentWallet.mnemonic = savedMnemonic;
        currentWallet.address = savedAddress;
        
        document.getElementById('walletAddress').textContent = savedAddress;
        document.getElementById('wallet-empty').classList.add('hidden');
        document.getElementById('wallet-loaded').classList.remove('hidden');
        
        await refreshBalance();
    }
}

// Balance Management
async function refreshBalance() {
    if (!currentWallet.address) return;
    
    try {
        const response = await fetch(`${API_BASE}/wallet/get-balance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                address: currentWallet.address,
                networkId: 'undeployed'
            })
        });
        
        if (!response.ok) throw new Error('Failed to get balance');
        
        const data = await response.json();
        
        // Check for balance changes (airdrop detection)
        if (currentWallet.balance.night > 0 || currentWallet.balance.dust > 0) {
            const nightDiff = data.night - currentWallet.balance.night;
            const dustDiff = data.dust - currentWallet.balance.dust;
            
            // If balance increased, log as airdrop/receive
            if (nightDiff > 0) {
                addTransaction({
                    type: 'receive',
                    address: 'External Airdrop',
                    amount: nightDiff,
                    token: 'NIGHT',
                    timestamp: Date.now()
                });
            }
            
            if (dustDiff > 0 && nightDiff === 0) {
                // DUST only increase (not from NIGHT conversion)
                addTransaction({
                    type: 'receive',
                    address: 'External Airdrop',
                    amount: dustDiff,
                    token: 'DUST',
                    timestamp: Date.now()
                });
            }
        }
        
        currentWallet.balance = data;
        
        const nightFormatted = formatBalance(data.night);
        const dustFormatted = formatBalance(data.dust);
        
        document.getElementById('totalBalance').textContent = nightFormatted;
        document.getElementById('nightBalance').textContent = nightFormatted;
        document.getElementById('dustBalance').textContent = dustFormatted;
    } catch (error) {
        console.error('Balance refresh error:', error);
    }
}

async function airdropFunds() {
    if (!currentWallet.address) {
        alert('Please import a wallet first');
        return;
    }
    
    try {
        // Get current balance first
        const currentBalance = { ...currentWallet.balance };
        
        const response = await fetch('http://127.0.0.1:9944/balance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                address: currentWallet.address,
                dust: currentWallet.balance.dust + 10_000_000,
                night: currentWallet.balance.night + 10_000_000
            })
        });
        
        if (!response.ok) throw new Error('Failed to add funds');
        
        // Log the airdrop transaction
        addTransaction({
            type: 'receive',
            address: 'Wallet Airdrop',
            amount: 10_000_000,
            token: 'NIGHT',
            timestamp: Date.now()
        });
        
        // Also log DUST
        addTransaction({
            type: 'receive',
            address: 'Wallet Airdrop',
            amount: 10_000_000,
            token: 'DUST',
            timestamp: Date.now()
        });
        
        setTimeout(() => refreshBalance(), 1000);
        
        alert('✅ Added 10 NIGHT and 10 DUST to your wallet!');
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Transfer Management
function setAmount(amount) {
    document.getElementById('transferAmount').value = amount;
    updateTransferSummary();
}

function setMaxAmount() {
    const maxNight = currentWallet.balance.night / 1_000_000;
    document.getElementById('transferAmount').value = maxNight.toFixed(6);
    updateTransferSummary();
}

function updateTransferSummary() {
    const amount = parseFloat(document.getElementById('transferAmount').value) || 0;
    document.getElementById('summaryAmount').textContent = `${amount.toFixed(6)} NIGHT`;
    document.getElementById('summaryTotal').textContent = `${amount.toFixed(6)} NIGHT`;
}

async function sendTransfer() {
    if (!currentWallet.mnemonic || !currentWallet.address) {
        showMessage('sendMessage', 'Please import a wallet first', 'error');
        return;
    }
    
    const recipient = document.getElementById('recipientAddress').value.trim();
    const amountNight = parseFloat(document.getElementById('transferAmount').value);
    
    if (!recipient) {
        showMessage('sendMessage', 'Please enter recipient address', 'error');
        return;
    }
    
    if (!amountNight || amountNight <= 0) {
        showMessage('sendMessage', 'Please enter a valid amount', 'error');
        return;
    }
    
    if (!recipient.startsWith('mn_addr_')) {
        showMessage('sendMessage', 'Invalid recipient address format', 'error');
        return;
    }
    
    const amount = Math.floor(amountNight * 1_000_000);
    
    if (amount > currentWallet.balance.night) {
        showMessage('sendMessage', `Insufficient balance. You have ${formatBalance(currentWallet.balance.night)} NIGHT`, 'error');
        return;
    }
    
    const btn = document.getElementById('sendBtn');
    btn.innerHTML = '<span class="loading"></span> Sending...';
    btn.disabled = true;
    
    try {
        let endpoint, requestBody;
        
        if (currentWallet.transferType === 'unshielded') {
            // Unshielded transfer
            endpoint = `${API_BASE}/wallet/transfer-unshielded`;
            requestBody = {
                fromAddress: currentWallet.address,
                toAddress: recipient,
                amount: amount,
                mnemonic: currentWallet.mnemonic,
                networkId: 'undeployed'
            };
        } else {
            // Shielded transfer
            endpoint = `${API_BASE}/wallet/transfer-shielded`;
            requestBody = {
                fromAddress: currentWallet.address,
                toAddress: recipient,
                amount: amount,
                mnemonic: currentWallet.mnemonic,
                networkId: 'undeployed'
            };
        }
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Transfer failed');
        }
        
        const data = await response.json();
        
        // Add to transaction log
        addTransaction({
            type: 'send',
            address: recipient,
            amount: amount,
            token: 'NIGHT',
            txHash: data.txHash,
            transferType: currentWallet.transferType,
            timestamp: Date.now()
        });
        
        showMessage('sendMessage', 
            `<strong>✅ Transfer Successful!</strong><br>
            Type: ${currentWallet.transferType}<br>
            TX Hash: ${data.txHash}<br>
            Amount: ${formatBalance(amount)} NIGHT`, 
            'success'
        );
        
        document.getElementById('recipientAddress').value = '';
        document.getElementById('transferAmount').value = '';
        updateTransferSummary();
        
        setTimeout(() => refreshBalance(), 2000);
        
        btn.textContent = 'Send Transaction';
        btn.disabled = false;
    } catch (error) {
        showMessage('sendMessage', `Error: ${error.message}`, 'error');
        btn.textContent = 'Send Transaction';
        btn.disabled = false;
    }
}

// DUST Generation Modal
function generateDustModal() {
    const amount = prompt('Enter NIGHT amount to convert to DUST (1:1 ratio):');
    if (!amount) return;
    
    const amountNum = parseFloat(amount);
    if (isNaN(amountNum) || amountNum <= 0) {
        alert('Invalid amount');
        return;
    }
    
    generateDust(amountNum);
}

async function generateDust(amountNight) {
    if (!currentWallet.address) {
        alert('Please import a wallet first');
        return;
    }
    
    const amount = Math.floor(amountNight * 1_000_000);
    
    if (amount > currentWallet.balance.night) {
        alert(`Insufficient NIGHT balance. You have ${formatBalance(currentWallet.balance.night)} NIGHT`);
        return;
    }
    
    try {
        // Convert NIGHT to DUST (1:1 ratio)
        const newNight = currentWallet.balance.night - amount;
        const newDust = currentWallet.balance.dust + amount;
        
        const response = await fetch('http://127.0.0.1:9944/balance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                address: currentWallet.address,
                dust: newDust,
                night: newNight
            })
        });
        
        if (!response.ok) throw new Error('Failed to generate DUST');
        
        // Add to transaction log
        addTransaction({
            type: 'dust',
            address: 'DUST Generation',
            amount: amount,
            token: 'DUST',
            timestamp: Date.now()
        });
        
        alert(`✅ Generated ${formatBalance(amount)} DUST from ${formatBalance(amount)} NIGHT`);
        
        setTimeout(() => refreshBalance(), 1000);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Transaction Log
function addTransaction(tx) {
    transactions.unshift(tx);
    localStorage.setItem('midnight_transactions', JSON.stringify(transactions));
    loadTransactions();
}

function loadTransactions() {
    const saved = localStorage.getItem('midnight_transactions');
    if (saved) {
        transactions = JSON.parse(saved);
    }
}

async function syncTransactions() {
    if (!currentWallet.address) {
        alert('Please import a wallet first');
        return;
    }
    
    // Force a balance refresh to detect any changes
    await refreshBalance();
    displayTransactions();
    alert('✅ Transactions synced!');
}

function displayTransactions() {
    const container = document.getElementById('activityList');
    
    if (transactions.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                    <circle cx="32" cy="32" r="30" stroke="currentColor" stroke-width="2" opacity="0.2"/>
                </svg>
                <h3>No Activity Yet</h3>
                <p>Your transaction history will appear here</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = transactions.map(tx => {
        const iconSvg = tx.type === 'send' 
            ? '<path d="M3 12l18-9-9 18-3-9-6 0z"/>'
            : tx.type === 'receive'
            ? '<path d="M12 3v14m0 0l-5-5m5 5l5-5M4 21h16"/>'
            : '<path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z"/>';
        
        const iconClass = tx.type;
        
        // Enhanced type label with transfer type badge
        let typeLabel = '';
        if (tx.type === 'send') {
            const transferBadge = tx.transferType === 'shielded' 
                ? '<span style="background: rgba(139, 92, 246, 0.2); color: #a78bfa; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-left: 6px;">🔒 Shielded</span>'
                : '<span style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-left: 6px;">👁 Public</span>';
            typeLabel = `Sent ${transferBadge}`;
        } else if (tx.type === 'receive') {
            typeLabel = 'Received';
        } else {
            typeLabel = 'Generated DUST';
        }
        
        const amountClass = tx.type === 'send' ? 'negative' : 'positive';
        const amountSign = tx.type === 'send' ? '-' : '+';
        const time = formatTime(tx.timestamp);
        
        // Format address display
        const addressDisplay = tx.address.length > 40 
            ? tx.address.substring(0, 20) + '...' + tx.address.substring(tx.address.length - 10)
            : tx.address;
        
        return `
            <div class="activity-item">
                <div class="activity-icon ${iconClass}">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        ${iconSvg}
                    </svg>
                </div>
                <div class="activity-details">
                    <div class="activity-type">${typeLabel}</div>
                    <div class="activity-address">${addressDisplay}</div>
                </div>
                <div class="activity-amount">
                    <div class="activity-value ${amountClass}">${amountSign}${formatBalance(tx.amount)} ${tx.token}</div>
                    <div class="activity-time">${time}</div>
                </div>
            </div>
        `;
    }).join('');
}

// Utility Functions
function formatBalance(amount) {
    return (amount / 1_000_000).toFixed(6);
}

function formatTime(timestamp) {
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
}

function copyAddress() {
    if (!currentWallet.address) {
        alert('No wallet connected');
        return;
    }
    
    navigator.clipboard.writeText(currentWallet.address).then(() => {
        alert('✅ Address copied to clipboard!');
    });
}

function copyMnemonic() {
    const mnemonic = document.getElementById('newMnemonicText').textContent;
    navigator.clipboard.writeText(mnemonic).then(() => {
        alert('✅ Recovery phrase copied to clipboard!');
    });
}

function showMessage(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="message ${type}">${message}</div>`;
    
    if (type === 'success') {
        setTimeout(() => {
            element.innerHTML = '';
        }, 5000);
    }
}

function showSettings() {
    alert('Settings coming soon!');
}
