"""
AI/ML inference with ZK proofs — prove your model ran correctly
without revealing the input data or model weights.
"""

from midnight_py import MidnightClient
import numpy as np

def main():
    client = MidnightClient(network="preprod")
    
    # Simulate ML model prediction
    input_data = np.array([1.2, 3.4, 5.6])
    prediction = "positive"  # Your model's output
    
    # Generate ZK proof that the model ran correctly
    proof = client.prover.generate_proof(
        circuit_id="ml_inference:predict",
        private_inputs={
            "model_weights": [0.5, 0.3, 0.2],  # Secret
            "input_data": input_data.tolist(),  # Secret
        },
        public_inputs={
            "prediction": prediction,  # Public result
            "model_hash": "abc123...",  # Commit to model version
        }
    )
    
    print(f"✓ Proof generated: {proof.proof[:50]}...")
    print(f"✓ Public output: {proof.public_outputs}")
    print("\nAnyone can verify this prediction is correct")
    print("without seeing your data or model!")

if __name__ == "__main__":
    main()
