# CIS-4930-Group
The initial file main.py is the starting and database testing file we are using to get a handle on pymongo and its operations as well as working with pandas and numpys to have
the graph based output we desire for the final program.
- We plan on using most of what's written here and optimizing it so that it works well and quickly with large datasets in
  a planned UI.
- Most testing functions and other testing data (such as the format of the Stats collection's datetime) will be removed or modified
  once we're comfortable with the output.
- The database will also be eventually updated to utilize the MongoDB cloud as to make it simpler for independent programming
  and using large sets of test data with the current functions.
- More functionality with MatPlotLib and including numpy arrays to handle large integer data is also planned.
- Also, please note that a lot of our work is done together in these early stages, so the GitHub history log will only reflect
  Independent work if not pushed by rl18c.

Format of Database:
The format of each part of the database is included in main.py, and below is a clearer look on the purpose of each.
Inventory: Is the current inventory of the location. It uses the "name" and "barcode" values as unique identifiers,
           and one can't add duplicates of barcode or name in this database.
Stats: Is the change of quantity over time of items. This has no unique identifier, but values of a given barcode are
       related. This database can only be added to when a change in the inventory database is made and otherwise
       is unmodifiable. It's used in tracking statistyics and for graphing relevant data.
NameBcode: Is for tracking unique name/barcode combinations in the inventory. Can be modified, but more depth
           is planned for this database. Will be used to get a name/barcode combination in larger datasets and for
	     automatically assigning barcodes for newly inserted items and tracking previous items that may have
	     been removed from the database.