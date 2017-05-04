# About this Repository

This repository is dedicated to KiCAD scripts that I use to make life easier. 
Each file is a self-contained runnable that performs a (useful) process. 

Simply pull whichever runnable file you need! It should be ready to go, out of the box. 
The following sections provide descriptions and deployment information for each of the KiCAD utilities included in this repository. 


## Utility #1: Edit All Schematic Entities - (aka EASE)

Have you ever wanted to edit the allinformation fields for all your project components simultaneously? Look no further!!

This script reads all KiCAD components and their associated fields from a project into a CSV document,
then reads the updated CSV document back into schematic files. (This can also double up as an awesome BOM builder)

### How To Use

BEFORE USING: 
* Make sure that all components in your KiCAD project are annotated with a unique reference name. The script will not work if
any duplicate reference names exist in the project.
* Ensure that all hierarchical schematic sheets are in the same folder as your project file.

STEP-BY-STEP:

1. Double click the runnable file and navigate to your kiCAD project from the file browser window that will pop up. 
1. All component fields in the the top level project schematic and all hierarchical schematic sheets will be read into a CSV file entitled "<schematic_name>_Editor.csv". This will be placed in the same directory as your project. 
1. The newly created CSV file should open automatically, you may edit the file in any of the following ways: 
    * Edit a cell in any column except for the first two columns (schematic name and reference name)
    * Sort the rows
    * Add component information to additional columns
    * DO NOT: Edit cells in the first two rows   
1. Once finished, save the CSV file and press "y" to overwrite your schematics
1. Your original schematics will be renamed as "<schematic_name>_old.sch" and placed in your kiCAD project folder. 

AFTER USING:
* If KiCAD was open at the time of editing, you will have to restart for any of the changes to take effect. 

### Compatibility and Versioning

Tested Operating Systems: Tested on Windows 10 and OSX 10.12.4 
Tested KiCAD Versions: Tested on Kicad v4.0.5 Release Build

Written with Python 3.0



## Authors

* **Brittany Scheid**

## License

This project is free for public use. 

