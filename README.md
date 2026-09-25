# Legislative Data

## Running the scripts
```bash
source venv/bin/activate
python -m legislative_report
or
python -m legislative_report --data-dir data --output-dir output
```


## File Structure
```bash
ligislativedata/
├── .github/
│   ├── ci.yml
├── legislative_report/
│   ├── __init__.py
│   ├── __main__.py               
│   ├── constants.py               
│   ├── models.py                  
│   ├── reader.py                  
│   ├── report_builder.py          
│   ├── writer.py                  
│   └── cli.py
├── tests/
│   ├── test_reader.py                         
├── data/                          
├── output/                        
└── README.md
```


## How to Prepare the Environment and Run the Tests
1. **Create the virtual environment in the project root:**
```bash
python -m venv venv
```

2. **Activate the virtual environment:**
* **Linux / Mac:**
```bash
source venv/bin/activate
```

* **Windows:**
```cmd
venv\Scripts\activate
```

3. **Install the application dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the test suite:**
```bash
pytest tests/
```