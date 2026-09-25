# Legislative Data


```bash
cd quorum_challenge
python -m legislative_report
python -m legislative_report --data-dir data --output-dir output
```


## File Structure
```
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