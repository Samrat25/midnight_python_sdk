from midnight_sdk.wallet import WalletClient

mnemonic = "next practice noodle hen mansion east spend pottery valid shield tortoise begin defense poet pottery rose matrix century umbrella release also clinic wet come"
w = WalletClient()
result = w.get_real_address(mnemonic, 'undeployed')
print(result['address'])
