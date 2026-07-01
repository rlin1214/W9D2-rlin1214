import sys
import time
import joblib
import pandas as pd

MODEL_PATH = "app/model.pkl"


def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python batch_infer.py data/input.csv data/predictions.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    start_time = time.time()

    # Load model
    model = joblib.load(MODEL_PATH)

    # Read input CSV
    df = pd.read_csv(input_file)

    # Ensure required columns exist
    required_columns = ["x1", "x2"]

    for column in required_columns:
        if column not in df.columns:
            print(f"Error: Missing required column '{column}'")
            sys.exit(1)

    # Generate predictions
    X = df[required_columns]

    predictions = model.predict_proba(X)[:, 1]

    # Add prediction column
    df["prediction"] = predictions.round(2)

    # Save output CSV
    df.to_csv(output_file, index=False)

    elapsed = time.time() - start_time

    print("Batch inference complete!")
    print(f"Rows processed: {len(df)}")
    print(f"Output file: {output_file}")
    print(f"Time taken: {elapsed:.3f} seconds")


if __name__ == "__main__":
    main()