# 🌸 Privacy-First Menstrual Health Tracker

A secure, encrypted period tracking application with statistical analysis and data visualization 

> 🚧 **Status:** Active Development | **Latest:** Added AES-256 encryption (Nov 2024)

## 💡 Why This Project?

After researching how mainstream period tracking apps monetize sensitive health data (selling to advertisers, insurance companies), I built a **privacy-first alternative** that:
- ✅ **Zero Data Collection** - Everything stays on your device
- ✅ **Military-Grade Encryption** - AES-256 Fernet encryption
- ✅ **No Internet Required** - Fully offline application
- ✅ **User Ownership** - You control your data, not corporations

### The Problem
- Popular period apps sell anonymized health data
- Insurance companies use this data for premium calculations
- Advertisers target based on cycle phases
- **Your health data becomes a product**

### My Solution
Build a tool that prioritizes **privacy over profit**.

---

## ✨ Current Features

### 🔒 Security Layer (Recently Added!)
- **AES-256 Encryption** - Health data encrypted at rest
- **Automatic Key Management** - Secure key generation
- **In-Memory Processing** - No plaintext ever touches disk
- **Error Recovery** - Graceful handling of decryption failures

### 📊 Health Analytics
- **Cycle Tracking** - Record dates, flow intensity, symptoms
- **Statistical Analysis** - NumPy-powered calculations
  - Average cycle length
  - Cycle variability (min/max/range)
  - Period duration trends
- **Predictive Modeling** - Next period predictions based on history
- **Data Visualization** - 4 interactive Matplotlib charts:
  - Cycle length trends over time
  - Period duration bar chart
  - Flow intensity distribution
  - Symptom frequency analysis

### 💾 Data Management
- **Local Storage** - CSV-based (encrypted)
- **Pandas Integration** - Efficient data manipulation
- **Auto-Save** - Data encrypted after each entry

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Encryption | Cryptography (Fernet) | AES-256 + HMAC-SHA256 |
| Data Analysis | Pandas | DataFrame operations |
| Statistics | NumPy | Cycle calculations |
| Visualization | Matplotlib | Chart generation |
| Language | Python 3.x | Core implementation |

---

## 🚀 Installation & Usage

### Prerequisites
```bash
Python 3.7+
pip install -r requirements.txt
```

### Quick Start
```bash
git clone https://github.com/nsneha16/period-tracker.git
cd period-tracker
pip install -r requirements.txt
python period_tracker.py
```

### First Run
- Program auto-generates encryption key (`secret.key`)
- ⚠️ **Keep this file safe!** - Required to decrypt your data
- Data stored in encrypted `period_data.csv`

### Menu Options
```
1. Add Period Entry    → Record new cycle data
2. View All Records    → Display encrypted data (decrypted in memory)
3. Show Statistics     → Calculate cycle patterns
4. Predict Next Period → Analyzes your history to predict next date
5. Show Charts         → Visual analytics dashboard
6. Exit                → Secure shutdown
```

---

## 🔐 Security Architecture
```
User Input
    ↓
[In-Memory DataFrame]
    ↓
pandas.to_csv() → CSV String
    ↓
.encode('utf-8') → Bytes
    ↓
Fernet.encrypt() → Encrypted Bytes
    ↓
File Write (binary) → period_data.csv
    ↓
[Disk: Encrypted Only]

Reverse process for reading!
```

### Why This Approach?
- **Plaintext never touches disk** - Only encrypted data written
- **Memory-safe** - io.StringIO for in-memory CSV processing
- **Key protection** - Separate key file (future: master password)

---

## 📚 What I Learned

### Technical Deep Dives
1. **Encryption Integration**
   - Adapting Fernet for DataFrame workflows
   - Bytes ↔ String conversions with encoding
   - Error handling for decryption failures

2. **Health Data Analytics**
   - Time-series analysis with irregular intervals
   - Statistical anomaly detection strategies
   - Meaningful health data visualization

3. **Privacy-First Design**
   - Local-first architecture principles
   - Encryption at rest best practices
   - User data ownership models

### Challenges Overcome
- **Date Handling**: Computing cycles across variable timeframes
- **Encryption + Pandas**: Merging binary encryption with text CSV
- **Data Integrity**: Ensuring encrypted file doesn't corrupt
- **UX Balance**: Security without sacrificing usability

---

## 🚧 Roadmap (Actively Developing)

### ✅ Completed
- [x] Core tracking functionality
- [x] Statistical analysis (NumPy)
- [x] Data visualizations (Matplotlib)
- [x] **AES-256 Encryption** (Nov 2024)
- [x] Encrypted save/load mechanisms

### 🔜 Next Sprint (Planned)
- [ ] **Master Password** - PBKDF2 key derivation (Week 1)
- [ ] **Anomaly Detection** - Alert for irregular cycles (Week 1)
- [ ] **Anonymous Export** - Doctor-shareable reports (Week 2)
- [ ] **Backup/Restore** - Encrypted backup functionality (Week 2)

### 🎯 Future Enhancements
- [ ] Password strength indicator
- [ ] Symptom correlation analysis
- [ ] Fertility window calculations
- [ ] Mood tracking integration
- [ ] Web interface (Flask)
- [ ] Multi-user support (family sharing)
- [ ] Doctor portal (read-only access with consent)

---

### Industry Examples
- **Clue**: Privacy-focused but requires internet
- **My Approach**: Zero data sharing, fully offline

---

## ⚠️ Important Disclaimers

### Medical
This is an **educational project** for tracking purposes only.
- Not intended for medical diagnosis
- Not suitable for contraceptive planning
- Consult healthcare professionals for medical advice

### Security
While using industry-standard encryption:
- Key stored locally (not ideal for production)
- Single-user device assumed
- For production use, consider: hardware security modules, cloud backup with client-side encryption

---

## 🤝 Contributing & Feedback

This is a learning project, but suggestions welcome!

**Areas for Feedback:**
- Security architecture improvements
- Health data privacy best practices
- UX enhancements for sensitive data display
- Statistical analysis suggestions

---

## 📊 Project Stats

- **Lines of Code**: ~200
- **Functions**: 8
- **Dependencies**: 4 (pandas, numpy, matplotlib, cryptography)
- **Test Coverage**: Manual testing (automated tests planned)
- **Development Time**: 2 weeks (ongoing)

---

## 👤 Author

**Sneha Namdeo**  
B.Tech Student | Passionate about Privacy & Health Tech

- 🔗 GitHub: [@nsneha16](https://github.com/nsneha)

---

## 📝 License Note

Educational project - free to use for learning.  
Built with awareness of health data privacy.

---


⭐ **If you care about health data privacy, star this repo!**

🔒 **Your health data should be yours alone.**
```

---

## 📋 requirements.txt (Updated)
```
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
cryptography==41.0.7