# Debt-Collection_repo

Data Pipeline for Debt Collection Letters is a robust data processing system designed to collect raw debtor accounts' data and transform it into a comprehensive final file which contains all essential debtor information and presents various payment scenarios, including full or payments in installments over three or twelve consecutive months.
Throughout this process debtor accounts undergo thorough cleaning and their addresses are carefully verified through Credit Reporting companies such as Experian, Transunion etc. This cleaning and verification ensures precise delivery of collection letters.

## Key components and features:

### Data Ingestion: 

The pipeline begins by extracting raw debtor accounts information from a CSV file. For each debtor account debt percentages are retrieved from both, a file and for certain clients, from an SQL database. 

### Data Transformation: 

The collected data have some missing fields. These missing fields -- debt amounts for multiple payment scenarios -- are calculated using debt percentages. 

### Data Verification: 

Calculated fields are then compared with original debt amounts. The system reports if there are mismatches in computed debt amounts and amounts in original data. It also has a feature to update debt percentages to match computed debt amounts with originals.

### Data Cleaning: 

Debtor accounts undergo rigorous data cleaning to eliminate inaccuracies. Some fields are designated for implementing checkpoints on the data. If any account fails to satisfy the specified criteria, it is removed and a summary is generated for deleted accounts. The system also identifies and reports any anomaly, error, or inconsistency in any field to ensure the reliability of the final dataset.

### Data Summary: 

Generates a workbook file containing all data including checkpoints for review purposes. The workbook file also contains a worksheet of pivot table which summarizes accounts count by ClientCodes for approval.

### Address Verification:

After approval, debtor addresses undergo systematic verification to ensure the precise delivery of collection letters. This verification process involves the creation of a CSV file containing necessary debtor details, which is then forwarded to an external vendor (TransUnion/Experian). Subsequently, a file containing the verified addresses is received and integrated into the original dataset.

### Address Cleaning and Concluding Data: 

Additional data cleaning is performed by examining each address field against specified criteria. Any account that does not meet these criterias is removed, also accounts having exact duplicate addresses are also removed. Resulting in final CSV file which contains accurate debtor account information ready for PCI Group to print and mail.
