import requests

address = "mn_addr_undeployed1p6wepa6q49ta4ptu5lkltxl5x8a4efq06vft9uex0vpsk7wmvplsxmfzey"

# Get current balance
balance_response = requests.post(
    "http://localhost:8000/wallet/get-balance",
    json={"address": address, "networkId": "undeployed"}
)
current = balance_response.json()
print(f"Current Balance:")
print(f"  NIGHT: {current['night'] / 1_000_000:.6f}")
print(f"  DUST: {current['dust'] / 1_000_000:.6f}")

# Airdrop 10 NIGHT
print(f"\nPerforming airdrop of 10 NIGHT...")
airdrop_response = requests.post(
    "http://127.0.0.1:9944/balance",
    json={
        "address": address,
        "night": current['night'] + 10_000_000,
        "dust": current['dust'] + 10_000_000
    }
)

if airdrop_response.ok:
    print("✅ Airdrop successful!")
    
    # Check new balance
    balance_response = requests.post(
        "http://localhost:8000/wallet/get-balance",
        json={"address": address, "networkId": "undeployed"}
    )
    new = balance_response.json()
    print(f"\nNew Balance:")
    print(f"  NIGHT: {new['night'] / 1_000_000:.6f} (+10.000000)")
    print(f"  DUST: {new['dust'] / 1_000_000:.6f} (+10.000000)")
else:
    print(f"❌ Airdrop failed: {airdrop_response.text}")
