# Travel Calcultor

## 🔍 Overview

The Travel Cost Estimator simplifies trip planning by using FY25 GSA per diem rates and City Pair Program airfare data to provide accurate, policy-compliant cost estimates for lodging, meals, and flights. It supports both CONUS and OCONUS trips, helping travelers quickly calculate realistic, budget-friendly expenses without manual effort.


## 📁 Project Structure

```text
Travel-cost/
├── data/
│   ├── airfare_2025.csv         # Database of airfares
│   └── FY2025_PerDiemRates.csv  # Database of per diem rate
├── src/
│   ├── main.py                  # Main programme
│   └── pages/
│        ├── home_page.py        # Home interface
│        ├── airfare_page.py     # Airfare interface
│        └── perdiem_page.py     # Perdiem interface
├──README.md                     # Project overview and metadata
├──.gitignore                    # Files ignored by Git
└── requirements.txt             # External Python packages your project needs to run
```

## 📌 Objectives

- Easily estimate travel costs (Per Diem + Airfare) using accurate data from FY25 GSA rates
- Provide budget-friendly estimates aligned with travel policies.
- Eliminate manual calculation errors by automating the entire process
- Support multiple destinations combining the latest Per Diem and City Pair Airfare data.

## 🧰 Tools and Technologies

- **Framework:** `Streamlit` is used to build an interactive and user-friendly web interface for the travel cost estimator  
- **Data Sources:** FY25 GSA Per Diem rates & City Pair Program airfare  
- **IDE:** Visual Studio Code
## 💻 Data Sources
- FY25 GSA Per Diem rates: https://www.gsa.gov/travel/plan-book/per-diem-rates
- City Pair Program airfare: https://www.gsa.gov/travel/plan-a-trip/transportation-airfare-rates-pov-rates-etc/airfare-rates-city-pair-program
## 📕 Language
- Python 
 
## 📄 List of game features

| Feature                     | Description |
|-----------------------------|-------------|
| **Per Diem Calculation**    | Automatically calculates lodging and M&IE costs based on selected location and travel dates. |
| **Airfare Lookup**          | Provides realistic airfare estimates using City Pair Program data. |
| **Three-Page Navigation**     | Separate pages for Home, Per Diem, Airfare estimation for better user experience. |
| **Reset & Search Functions**| Allows resetting selections (state, city, dates) and performing fresh cost calculations. |
| **Error Handling**          | Validates inputs and displays helpful messages. |


## 🕹️ Instructions
- Select **State** and **City** for per diem rates.
- Choose **Travel start dates** and **Travel end dates**.
- Look up **airfare** between origin and destination.
- Use **Search** to calculate, and **Reset** to clear all inputs.

## 👥 Author

  **Thanh Phong**

## 🤖 Project Setup
### Global Environment Setup
1. Install Python: <br>
Download and install Python (version 3.8 or higher).
2. Clone, fork or download the project:
- Open Command Prompt (CMD) or Terminal
```
git clone https://github.com/phongthanh1412/Travel-calculator.git
```
- Navigate to your project
```
cd ~\Travel-cost\src
```
3. Install dependencies
```
pip install -r requirements.txt
```
### Virtual Environment Setup
1. Install Python: <br>
Download and install Python (version 3.8 or higher).
2. Clone, fork or download the project: <br>
- Open Command Prompt (CMD) or Terminal.
```
git clone https://github.com/phongthanh1412/Travel-calculator.git
```
- Navigate to your project
```
cd ~Travel-cost\src
```
3. Set up a virtual environment
```
python -m venv venv
```
4. Activate virtual environment
```
venv\Scripts\activate
```
5. Deactivate virtual environment
```
deactivate
```
6. Install dependencies
```
pip install -r requirements.txt
```
### Run Code
1. Navigate to the project 
```
cd ~\Travel-cost\src
```
2. Run the project
```
python -m streamlit run main.py
```
This will launch the Streamlit server, and you can access the application through your web browser at Local `http://localhost:8501` or Network `http://192.168.1.8:8501`.
## ⛑️Contribute
- If you discover solutions or improvements to this project, contribute and build a better application. You are welcome. Thank you!
## 📚 Appendix 
### Dependencies
- `pandas` is used to efficiently load, filter, and manipulate travel and airfare datasets (CSV files) for accurate rate lookups and expense calculations.
- `os` accesses operating system functions like file paths.
- `datetime` manages date and time information when recording game time or move timestamps
### References
- https://www.gsa.gov/travel/plan-a-trip
- https://github.com/nelkalm/travel_cost_calculator
