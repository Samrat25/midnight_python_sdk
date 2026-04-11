import requests

address = "mn_addr_undeployed1pn6kwy6260h0j45lh7xtc59asgqx8q46wudcfn6plgtq35rzesxsfp4d78"

print(f"Airdropping to: {address}\n")

# Get current balance
try:
    balance_response = requests.post(
        "http://localhost:8000/wallet/get-balance",
        json={"address": address, "networkId": "undeployed"},
        timeout=5
    )
    current = balance_response.json()
    print(f"Current Balance:")
    print(f"  NIGHT: {current['night'] / 1_000_000:.6f}")
    print(f"  DUST: {current['dust'] / 1_000_000:.6f}")
except Exception as e:
    print(f"Could not get current balance: {e}")
    current = {"night": 0, "dust": 0}

# Airdrop 50 NIGHT
print(f"\n🎁 Performing airdrop of 50 NIGHT...")
try:
    airdrop_response = requests.post(
        "http://127.0.0.1:9944/balance",
        json={
            "address": address,
            "night": current['night'] + 50_000_000,
            "dust": current['dust'] + 50_000_000
        },
        timeout=5
    )

    if airdrop_response.ok:
        print("✅ Airdrop successful!")
        
        # Check new balance
        balance_response = requests.post(
            "http://localhost:8000/wallet/get-balance",
            json={"address": address, "networkId": "undeployed"},
            timeout=5
        )
        new = balance_response.json()
        print(f"\n💰 New Balance:")
        print(f"  NIGHT: {new['night'] / 1_000_000:.6f} (+50.000000)")
        print(f"  DUST: {new['dust'] / 1_000_000:.6f} (+50.000000)")
        print(f"\n✨ Now refresh your wallet to see the updated balance!")
    else:
        print(f"❌ Airdrop failed: {airdrop_response.text}")
except Exception as e:
    print(f"❌ Error during airdrop: {e}")
