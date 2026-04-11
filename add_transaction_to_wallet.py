"""
Add transaction to wallet localStorage
This script creates a JavaScript file that you can run in the browser console
"""

import json
from datetime import datetime

# Create the transaction for the 50 NIGHT airdrop
transaction = {
    "type": "receive",
    "address": "CLI Airdrop - 50 NIGHT",
    "amount": 50000000,
    "token": "NIGHT",
    "timestamp": int(datetime.now().timestamp() * 1000)
}

# Also add DUST transaction
dust_transaction = {
    "type": "receive",
    "address": "CLI Airdrop - 50 DUST",
    "amount": 50000000,
    "token": "DUST",
    "timestamp": int(datetime.now().timestamp() * 1000)
}

# Create JavaScript code to inject
js_code = f"""
// Add transactions to localStorage
(function() {{
    const transactions = [
        {json.dumps(transaction)},
        {json.dumps(dust_transaction)}
    ];
    
    let existing = JSON.parse(localStorage.getItem('midnight_transactions') || '[]');
    
    // Add new transactions at the beginning
    transactions.forEach(tx => {{
        existing.unshift(tx);
    }});
    
    localStorage.setItem('midnight_transactions', JSON.stringify(existing));
    
    console.log('✅ Added', transactions.length, 'transactions');
    console.log('Total transactions:', existing.length);
    
    // Reload to show transactions
    alert('✅ Transactions added! The page will reload.');
    location.reload();
}})();
"""

# Save to file
with open('wallet-app/inject-transactions.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Created inject-transactions.js")
print("\nTo add transactions to your wallet:")
print("1. Open your wallet in browser")
print("2. Press F12 to open Developer Tools")
print("3. Go to Console tab")
print("4. Copy and paste the content of wallet-app/inject-transactions.js")
print("5. Press Enter")
print("\nOr simply run this in console:")
print("-" * 60)
print(js_code)
print("-" * 60)
