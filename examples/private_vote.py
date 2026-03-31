"""
Private voting example — vote without revealing your choice.
Only the final tally is public.
"""

from midnight_py import MidnightClient
from midnight_py.codegen import compact_to_python

def main():
    client = MidnightClient(network="preprod")
    
    # Load voting contract
    VotingContract = compact_to_python("contracts/private_vote.compact")
    contract = client.get_contract("voting_address_here", ["cast_vote", "tally"])
    voting = VotingContract(contract)
    
    # Cast a private vote (choice stays secret)
    result = voting.cast_vote(
        private_inputs={"choice": "candidate_A", "voter_id": "voter123"},
        public_inputs={"election_id": "2024_election"}
    )
    print(f"Vote cast! TX: {result.tx_hash}")
    
    # Read public tally
    state = voting.state()
    print(f"Current tally: {state.state}")

if __name__ == "__main__":
    main()
