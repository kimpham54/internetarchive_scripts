# This is how we get items from the Internet Archive
# https://archive.org/details/turkishhistoryfr01knol

from internetarchive import get_item
item = get_item('menusfromvarious00unse')
item.item_metadata.keys()
item.files
# dictionary


>>> type(item.files) is list
True
>>> type(item.files) is dict
False


>>> for k in item.files:
...    print(k)

# download a collection
# download an item
# script to scan compare checksum and pull items that are new
