# CIS-4930-Group


Problem Being Solved		       
=================================
A system to manage individual user's Inventory databases. Statistical representation of stock and
profit analysis overtime.

GUI Description
=================================
Login Screen : 	- Can create new User (Creates personal DB Collections)
		- Can login with existing User
		- Can delete existing User
Main Window  : 	- Browse Inventory records and make modifications
		- Add new Item to inventory
		- Export data to excel spreadsheet / Import data from excel spreadsheet
		- Create an excel spreadsheet template to be edited/imported
		- Can Graph the Current Selected Item / Graph All Items
Graph Window : 	- Graph Stock Changes / Graph Calculated Profit  (Both based off quantity changes)

Notes :	- When trying to run the database on FSU's internet, we realized a VPN is required.
		- A login for testing used by us was: Username: test1 Password: test1


Final List of Libraries Used		
=================================
-pymongo
-MatPlotlib
-random
-datetime
-sys
-dnspython
-tkinter
-tkcalendar
-numpy
-pandas
-bcrypt


Other Resources		
=================================
No other resources were used.


Separation of Work	
=================================
Aaron Peronto
	- Developed entire User login system.
		- Login GUI Design
		- Individual user collection creation
		- Maintain correct collection in main inventory GUI

Robert Lovern 
	- Managed/Created most of the code interacting directly with DB collections
	- Handled statistical analysis of user's DB information
		- Logic to calculate Stock/Profit changes 
		- Used these statistics to plot on Graph
	- Handled graph generation

Cory Avrutis
	- Handled design layout for GUI
	- Oversaw the structuring of GUI code
		- Organized via Object-Oriented approach
	- Visualized and implemented all necessary graphical changes when required
		- Widget Placement / Functionality / Type  
	- Managed the interaction of widgets with actual DB operations
		- DB operation logic ported from Robert's implementation
	- Assisted in user password hashing


Extra Features from Proposal	
=================================

A change we made from our proposal was how the user can view the inventory metrics,
mainly in the change from a simple printout detailing their statistics. We decided to shift
into using graphs and adding in an optional export/import functionality to allow the user
more control over the database if they want it. Another major change was our inclusion of
login functionality. We decided that having multiple collections would help us with
testing, and since many applications of today have this functionality, we decided to
research and include it in our app.


Format of Database
=================================

The format of each part of the database is included in main.py, and below is a clearer 
look on the purpose of each.

 -Inventory: Is the current inventory for a user. It uses the "name" and "barcode" values as unique identifiers,
             and one can't add duplicates of barcode or name in this database.
 
 -Stats: Is the change of quantity over time of items. This has no unique identifier, but values of a given barcode are
         related. This database can only be added to when a change in the inventory database is made and otherwise
         is unmodifiable. It's used in tracking statistics and for graphing relevant data.
 
 -NameBcode: Is for tracking unique name/barcode combinations in the inventory. Will be used to get a name/barcode 
	     combination in larger datasets and for automatically assigning barcodes for newly inserted items and 
	     tracking previous items that may have been removed from the database.

NOTE: Each user will have their own unique set of these 3 collections.