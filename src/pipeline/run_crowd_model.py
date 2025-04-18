from utils.crowd_features import extract_features, generate_synthetic_scores
from core.crowd_model import train_crowd_model, save_model
import pandas as pd

def main():
    df = pd.read_csv("data/merged_stop_data.csv")
    df = generate_synthetic_scores(df)
    
    X = extract_features(df)
    y = df['synthetic_crowd_score']
    
    model = train_crowd_model(X, y)
    save_model(model)

if __name__ == "__main__":
    main()
