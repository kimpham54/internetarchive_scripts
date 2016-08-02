
# This is how we get items from the Internet Archive
# https://archive.org/details/turkishhistoryfr01knol

from internetarchive import get_item, download, search_items,configure
import ia_settings

def check_for_new_items(username,password,collection,collections_db):
    """username->(String) IA username
       password->(String) IA password
       collection->(String) IA identifier for the collection to watch
       collections_db->(String) file path of plain text database of collections to ignore.

       ident_1
       ident_d
       ident_3

       
       returns->(list) list of identifiers of new items in collection

       Checks if there is a new group of scans in the collection from a list in a text file"""

    configure(username,password) # Configure log in information for IA
    downloaded_collections = []
    with open(collections_db) as f:
        for line in f:
            downloaded_collections.append(line.rstrip("\n"))
    new_collections = []
    for book in get_item(collection).contents():
        if(book.identifier not in downloaded_collections):
            new_collections.append(book.identifier)
    return new_collections


def add_item_to_db(collections_db,new_items):
    """collections_db -> (String) filename of plain text db for ingested items
       new_items -> (list) List of string identifiers for scan groups

       Once items have been processed, they can be added to the collections database of downloaded collections"""

    with open(collections_db,"a") as f:
        for new_col in new_items:
            f.write(new_col +"\n")


def download_collection(username,password,collection,destination,glob="*",dry_run=False):

    configure(username,password)
    download(collection,destdir=destination,glob_pattern=glob,dry_run=dry_run)


if __name__ == "__main__":

#collection = 'booksgrouptest'
    collection = 'eightconceptsofb00gilb'
    username = ia_settings.ia_username
    password = ia_settings.ia_password
    md5_table = "test_md5.txt"
    dest="."

#print("Running dry run of download_new_items on %s"%(collection))
#    download_new_items(username,password,collection,md5_table, dest,dry_run=True)
    download_single_item(username,password,collection,dest)
    #book = 'menusfromvarious00unse'

    #item = get_item(book) # Gets book of this name

#print(item.item_metadata.keys())
#
## check type of variable
#print(type(item.files) is list)
##True
#print(type(item.files) is dict)
##False
##
### list all files in an object
#for k in item.files:
#    print(k)
#
## download a collection
#
#dest = "."

#item.download(checksum=True, destdir=dest)

# download an item
# script to scan compare checksum and pull items that are new
