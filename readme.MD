ASSESMENT PROBLEM STATEMENT:
https://docs.google.com/document/d/1EB-L2Vc4vI_Xi68gu1-TcgcEXl8E-kqPIRoh9_SYZZQ/edit?usp=sharing

Please note db file is commited
Current Database state is the state after testing scenerios's given under SPLIT section in ASSESSMENT PROBLEM STATEMENT, you erase the data in main_transation table to perform tests from scratch. 


- APIs which enable addition of above mentioned 3 types of transactions.
```
endpoint: http://127.0.0.1:8000/api/transaction/
method: POST
payload sampales: 
buy: {
            "trade_type": "BUY",
            "qty": 100,
            "price": 200,
            "split_ratio": null,
            "date": "2023-06-20"
    }

sell: {
            "trade_type": "SELL",
            "qty": 100,
            "price": 200,
            "split_ratio": null,
            "date": "2023-06-20"
    }

split: {
            "trade_type": "SPLIT",
            "qty": null,
            "price": null,
            "split_ratio": 5,
            "date": "2023-06-20"
        }
```



- An API which returns average buy price and balance quantity after any day.

```
endpoint: http://127.0.0.1:8000/api/holding/{date}/
sample for date 2023-06-16: http://127.0.0.1:8000/api/holding/2023-06-16/

```