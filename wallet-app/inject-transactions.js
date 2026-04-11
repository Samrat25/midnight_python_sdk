
// Add transactions to localStorage
(function() {
    const transactions = [
        {"type": "receive", "address": "CLI Airdrop - 50 NIGHT", "amount": 50000000, "token": "NIGHT", "timestamp": 1775929976064},
        {"type": "receive", "address": "CLI Airdrop - 50 DUST", "amount": 50000000, "token": "DUST", "timestamp": 1775929976064}
    ];
    
    let existing = JSON.parse(localStorage.getItem('midnight_transactions') || '[]');
    
    // Add new transactions at the beginning
    transactions.forEach(tx => {
        existing.unshift(tx);
    });
    
    localStorage.setItem('midnight_transactions', JSON.stringify(existing));
    
    console.log('✅ Added', transactions.length, 'transactions');
    console.log('Total transactions:', existing.length);
    
    // Reload to show transactions
    alert('✅ Transactions added! The page will reload.');
    location.reload();
})();
