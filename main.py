#!/usr/bin/python

import database
import csvFile
import getpass
# import of module to parse configuration files
# note that the module name will change  to configparser for Python3
import ConfigParser

CONFIGURATION_FILE	= "donation_import.cfg"
DEFAULT_HOST 		= "localhost"
DEFAULT_USER 		= "root"
#stub-start
#erase this!
DEFAULT_PASS 		= "password"
#stub-end
DEFAULT_DBNAME 		= "DatabaseName"
DEFAULT_CSVFILENAME = "CharityDataDownload.csv"

def readConfigurationFile(file):
	"""Reads database and csv file parameters from a given file """
	databaseSectionName = 'database';
	config = ConfigParser.ConfigParser()
	config.read('donation_import.cfg')
	host = config.get(databaseSectionName,'host')
	userName = config.get(databaseSectionName,'userName')
	password = config.get(databaseSectionName,'password')
	dbName = config.get(databaseSectionName,'dbName')

	csvFileName = config.get('csvFile','csvFileName')
        csvErrorFileName = config.get('csvFile','csvErrorFileName')

	# Following line is only used for debugging
	#print(",".join((host,userName,password,dbName,csvFileName)))

	return (host,userName,password,dbName,csvFileName,csvErrorFileName)


def changeCSVToDatabaseFormat(csvRecord):
	""" Change the CSV format to a more suitable format for database addition """

	donorInfo = database.DonorInfo()
	donorInfo.firstName = csvRecord.firstName
	donorInfo.lastName = csvRecord.lastName
	donorInfo.address = csvRecord.address
	donorInfo.city = csvRecord.city
	donorInfo.province = csvRecord.province
	donorInfo.postalCode = csvRecord.postalCode
	donorInfo.amountPaid = float(csvRecord.amountPaid)
	donorInfo.datePaid = csvRecord.datePaid

	return donorInfo


# Main function 
def executeAddTransaction(csvFileName, dbInfo):
        
        csvRows = csvFile.getRows(csvFileName)

	#csvObject = csvFile.openCsvFile(csvFileName)
	#if csvObject == False:
	#	return False
	#csvRecords = csvFile.getRecords(csvObject)

	for i,csvRow in enumerate(csvRows):
            if(i>0):
                csvRecord = csvFile.CSVRecord(csvRow)
		donorInfo = changeCSVToDatabaseFormat(csvRecord)
		database.addTransactionToDatabase(donorInfo, dbInfo)


# Call the main command

(raw_host,raw_user,raw_pass,raw_dbname,raw_csvFilename,csvErrorFileName) = readConfigurationFile(CONFIGURATION_FILE)

databaseInfo = database.DatabaseInfo(raw_host,raw_user,raw_pass,raw_dbname)

executeAddTransaction(raw_csvFilename, databaseInfo)
