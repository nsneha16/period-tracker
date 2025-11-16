import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os
import io


def gen_key():
    key_file='secret.key'
    try:
        with open(key_file, 'rb') as f:
            return f.read()
        
    except FileNotFoundError:
        key=Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key;



class PeriodTracker:
    def __init__(self):
        self.data_file = 'period_data.csv'
        self.fieldnames = ['start_date', 'end_date', 'flow', 'symptoms']
        self.key = gen_key()
        self.cipher = Fernet(self.key)
        self.load_data()
    


    def load_data(self):
            """
            Loads and decrypts period data from the CSV file.
            This adapts the 'load_passwords' logic for DataFrame handling.
            """
            try:
                if os.path.exists(self.data_file):
                    print("⏳ Loading and decrypting data...")
                    
                    # Read encrypted data as bytes
                    with open(self.data_file, mode='rb') as f:
                        encrypted_data = f.read()
                    
                    # Decrypt the data bytes
                    decrypted_bytes = self.cipher.decrypt(encrypted_data)
                    
                    # Decode bytes to a CSV string
                    csv_string = decrypted_bytes.decode('utf-8')
                    
                    # Use io.StringIO to read the CSV string directly into a DataFrame
                    self.df = pd.read_csv(io.StringIO(csv_string), parse_dates=['start_date', 'end_date'])
                    print("✅ Data loaded and decrypted successfully!")
                else:
                    # Create new DataFrame if file does not exist
                    self.df = pd.DataFrame(columns=self.fieldnames)
                    print("📝 New tracker created (no prior data found).")
            
            except Exception as e:
                # Handle key mismatch, file corruption, or decryption errors
                print(f"🚨 ERROR in loading/decrypting file: {e}")
                self.df = pd.DataFrame(columns=self.fieldnames)
                print("⚠️ Initializing empty tracker due to error.")




    # def load___data(self):
    #     #"""Load existing data or create new DataFrame"""
    #     try:
    #         self.df = pd.read_csv(self.data_file, parse_dates=['start_date', 'end_date'])
    #         print("✅ Data loaded successfully!")
    #     except:
    #         self.df = pd.DataFrame(columns=['start_date', 'end_date', 'flow', 'symptoms'])
    #         print("📝 New tracker created!")
    
    


    def save_data(self):
        """
        Encrypts the DataFrame data and saves it to the CSV file.
        This adapts the 'save_passwords' logic for DataFrame handling.
        """
        try:
            # Convert DataFrame to CSV string (in-memory)
            csv_string = self.df.to_csv(index=False)
            
            # Encode string to bytes
            csv_bytes = csv_string.encode('utf-8')
            
            # Encrypt the data bytes
            encrypted_data = self.cipher.encrypt(csv_bytes)
            
            # Write encrypted bytes to the file (binary write 'wb')
            with open(self.data_file, mode='wb') as f:
                f.write(encrypted_data)
            
            print("💾 Data encrypted and saved!")
            
        except Exception as e:
            print(f"🚨 ERROR in saving/encrypting data: {e}")


    def add_period(self, start, end, flow="Medium", symptoms=""):
        """Add new period entry and trigger secure save."""
        try:
            new_entry = pd.DataFrame({
                'start_date': [pd.to_datetime(start)],
                'end_date': [pd.to_datetime(end)],
                'flow': [flow],
                'symptoms': [symptoms]
            })
            self.df = pd.concat([self.df, new_entry], ignore_index=True)
            self.df = self.df.sort_values('start_date').reset_index(drop=True)
            
            # This is the key link to the secure save mechanism
            self.save_data()
            print("✅ Period entry added and securely saved!")
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")

    
    def view_data(self):
        #"""Display all records"""
        if self.df.empty:
            print("❌ No data available")
            return
        print("\n" + "="*150)
        print("📊 PERIOD RECORDS")
        print("="*150)
        print(self.df.to_string(index=False))
        print("="*150 + "\n")

    def check_anomalies(self):
        """Detect irregular cycles and alert user"""
        if len(self.df) < 2:
            return
        
        # Calculate all cycles
        cycles = []
        for i in range(1, len(self.df)):
            days = (self.df['start_date'].iloc[i] - self.df['start_date'].iloc[i-1]).days
            cycles.append(days)
        
        # Check for anomalies
        for i, cycle in enumerate(cycles):
            if cycle < 21:
                print(f"⚠️ ALERT: Cycle {i+1} is unusually short ({cycle} days)")
                print("   Consider consulting a healthcare provider.")
            elif cycle > 35:
                print(f"⚠️ ALERT: Cycle {i+1} is unusually long ({cycle} days)")
                print("   Consider consulting a healthcare provider.")
    
    def calculate_stats(self):
        #"""Calculate statistics using NumPy"""
        if len(self.df) < 2:
            print("⚠️  Need at least 2 periods for statistics")
            return
        
        # Calculate cycle lengths
        cycles = []
        for i in range(1, len(self.df)):
            days = (self.df['start_date'].iloc[i] - self.df['start_date'].iloc[i-1]).days
            cycles.append(days)
        cycles = np.array(cycles)
        
        # Calculate period durations
        durations = (self.df['end_date'] - self.df['start_date']).dt.days + 1
        durations = np.array(durations)
        
        print("\n" + "="*150)
        print("📈 STATISTICS")
        print("="*150)
        print(f"Total Periods: {len(self.df)}")
        print(f"Average Cycle: {np.mean(cycles):.1f} days")
        print(f"Cycle Range: {np.min(cycles)} - {np.max(cycles)} days")
        print(f"Average Duration: {np.mean(durations):.1f} days")
        print("="*50 + "\n")
        self.check_anomalies()
    
    def predict_next(self):
        #"""Predict next period using NumPy"""
        if len(self.df) < 2:
            print("⚠️  Need at least 2 periods for prediction")
            return
        
        # Calculate average cycle
        cycles = []
        for i in range(1, len(self.df)):
            days = (self.df['start_date'].iloc[i] - self.df['start_date'].iloc[i-1]).days
            cycles.append(days)
        
        avg_cycle = np.mean(cycles)
        last_date = self.df['start_date'].iloc[-1]
        predicted = last_date + timedelta(days=int(avg_cycle))
        
        print("\n" + "="*150)
        print("🔮 NEXT PERIOD PREDICTION")
        print("="*150)
        print(f"Predicted Date: {predicted.strftime('%Y-%m-%d')}")
        print(f"Based on {avg_cycle:.1f} day average cycle")
        print("="*150 + "\n")
    
    def visualize(self):
        #"""Create visualizations using Matplotlib"""
        if len(self.df) < 2:
            print("⚠️  Need at least 2 periods for charts")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('🌸 Period Tracker Dashboard 🌸', fontsize=16, fontweight='bold')
        
        # 1. Cycle Length Trend
        ax1 = axes[0, 0]
        cycles = []
        dates = []
        for i in range(1, len(self.df)):
            days = (self.df['start_date'].iloc[i] - self.df['start_date'].iloc[i-1]).days
            cycles.append(days)
            dates.append(self.df['start_date'].iloc[i])
        
        ax1.plot(dates, cycles, marker='o', color='#FF6B9D', linewidth=2)
        ax1.axhline(np.mean(cycles), color='red', linestyle='--', label=f'Avg: {np.mean(cycles):.1f}d')
        ax1.set_title('Cycle Length Over Time')
        ax1.set_ylabel('Days')
        ax1.legend()        #
        ax1.grid(True, alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # 2. Period Duration
        ax2 = axes[0, 1]
        durations = (self.df['end_date'] - self.df['start_date']).dt.days + 1
        labels = self.df['start_date'].dt.strftime('%b %Y')
        ax2.bar(labels, durations, color='#FFB6C1')
        ax2.set_title('Period Duration')
        ax2.set_ylabel('Days')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # 3. Flow Distribution
        ax3 = axes[1, 0]
        flow_counts = self.df['flow'].value_counts()
        colors = ['#FFE5EC', '#FFB6C1', '#FF1493']
        ax3.bar(flow_counts.index, flow_counts.values, color=colors)
        ax3.set_title('Flow Intensity')
        ax3.set_ylabel('Count')
        
        # 4. Symptom Frequency
        ax4 = axes[1, 1]
        symptom_dict = {}
        for symptoms in self.df['symptoms'].dropna():
            for s in symptoms.split(','):
                s = s.strip()
                if s:
                    symptom_dict[s] = symptom_dict.get(s, 0) + 1
        
        if symptom_dict:
            ax4.pie(symptom_dict.values(), labels=symptom_dict.keys(), 
                   autopct='%1.1f%%', colors=plt.cm.Pastel1(range(len(symptom_dict))))
            ax4.set_title('Symptom Distribution')
        else:
            ax4.text(0.5, 0.5, 'No symptoms recorded', ha='center')
            ax4.set_title('Symptom Distribution')
        
        plt.tight_layout()
        plt.show()
        print("📊 Charts displayed!")


def main():
    #"""Main program"""
    tracker = PeriodTracker()
    
    print("\n" + "="*150)
    print("🌸 PERIOD TRACKER - Mini Project 🌸")
    print("Using: Pandas, NumPy & Matplotlib")
    print("="*150)
    
    while True:
        print("\n📋 MENU:")
        print("1. Add Period Entry")
        print("2. View All Records")
        print("3. Show Statistics")
        print("4. Predict Next Period")
        print("5. Show Charts")
        print("6. Exit")
        
        choice = input("\n👉 Enter choice (1-6): ").strip()
        
        if choice == '1':
            print("\n--- Add Period Entry ---")
            start = input("Start Date (YYYY-MM-DD): ")
            end = input("End Date (YYYY-MM-DD): ")
            flow = input("Flow (Light/Medium/Heavy) [Medium]: ") or "Medium"
            symptoms = input("Symptoms (comma separated): ")
            tracker.add_period(start, end, flow, symptoms)
        
        elif choice == '2':
            tracker.view_data()
        
        elif choice == '3':
            tracker.calculate_stats()
        
        elif choice == '4':
            tracker.predict_next()
        
        elif choice == '5':
            tracker.visualize()
        
        elif choice == '6':
            print("\n👋 Thank you for using Period Tracker! 🌸")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")


# if __name__ == "__main__":
main()