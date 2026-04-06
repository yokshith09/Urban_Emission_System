import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_training_data(output_path):
    print("Generating simulated historical dataset...")
    dates = [datetime.now() - timedelta(hours=i) for i in range(24 * 30)]
    dates.reverse()
    
    # Simulate data based on daily patterns
    y = []
    for d in dates:
        base = 70.0
        hr = d.hour
        daily = 20 if (7 <= hr <= 10 or 17 <= hr <= 20) else -10
        noise = np.random.normal(0, 5)
        y.append(base + daily + noise)
        
    df = pd.DataFrame({'ds': dates, 'y': y})
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df

def run_forecast(history_file, output_file):
    if not os.path.exists(history_file):
        df = generate_training_data(history_file)
    else:
        df = pd.read_csv(history_file)
        df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)
        
    try:
        from prophet import Prophet
        print("Training Prophet Model...")
        model = Prophet()
        model.fit(df)
        
        print("Predicting next 24 hours...")
        future = model.make_future_dataframe(periods=24, freq='h')
        forecast = model.predict(future)
        
        # Keep predictions only
        last_date = df['ds'].max()
        preds = forecast[forecast['ds'] > last_date][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        preds.to_csv(output_file, index=False)
        print(f"Prophet Forecast completed. Saved to {output_file}")
        
    except ImportError:
        print("Prophet not available, falling back to simple mock forecast.")
        last_date = df['ds'].max()
        dates = [last_date + timedelta(hours=i+1) for i in range(24)]
        mean_y = df['y'].iloc[-24:].mean() if len(df) >= 24 else df['y'].mean()
        
        yhat = []
        for d in dates:
            base = mean_y
            hour = d.hour
            daily = 20 if (7 <= hour <= 10 or 17 <= hour <= 20) else -10
            yhat.append(base + daily + np.random.normal(0, 5))
            
        preds = pd.DataFrame({
            'ds': dates,
            'yhat': yhat,
            'yhat_lower': [y-5 for y in yhat],
            'yhat_upper': [y+5 for y in yhat]
        })
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        preds.to_csv(output_file, index=False)
        print(f"Fallback Forecast completed. Saved to {output_file}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    history_file = os.path.join(base_dir, "data", "raw", "aqi_history.csv")
    output_file = os.path.join(base_dir, "data", "processed", "predictions.csv")
    
    run_forecast(history_file, output_file)
