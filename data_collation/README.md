# Script usage instructions:

Run the following scripts in order (make sure that you run them while located in the `/data_collation` directory):
1. `named_life_table_extraction.py`
2. `table_name_summary.py`
3. `named_data_collation.py`

The final result will be `life_tables_master.csv`, which collates the data from all life tables linked via https://www.cdc.gov/nchs/nvss/life-expectancy.htm#data into a single file.

In-file documentation explains details of each script's purpose. `fiddling.ipynb` and `raw_life_table_extraction.py` can also be consulted for context.