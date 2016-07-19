# Purpose of this file is to link all of the Internet Archive 
# files together into a pipeline to process the Harley-Spiller 
# collection.
#
#

import ia_getitems, ia_split, ia_redmine, ia_settings


# **************************
# CHECK FOR NEW COLLECTIONS
# **************************

collection_id = 'booksgrouptest' # The collection to watch
collections_db = 'harley_spiller_collections.txt' # The text file containing the subcollection (scan boxs, books?) that have already been processed

new_collections = ia_getitems.check_for_new_items(ia_settings.ia_username,ia_settings.ia_password,collection_id,collections_db)

if (len(new_colllections) == 0):
    # No new collections to process!
    return

# **************************
# DOWNLOAD COLLECTION
# **************************

dry_run=False

for col in new_collections:
    ia_getitems.download_collection(ia_settings.ia_username,ia_settings.ia_password,col,dry_run)

# **************************
# UNTAR the jp2 archive
# **************************


# **************************
# Split the archive into multiple folders and move the jp2 files
# Also generate the MODS files
# **************************

# **************************
# Open redmine ticket
# **************************

redmine_url = "https://digitalscholarship.utsc.utoronto.ca/redmine/"
#project_id = "digital-collections-working-group"
project_id = "kim-pham"
issue_subject = "Harley-Spiller Collection new items"
assign_to = "cadenarmstrong"
print(new_collections)
issue_description = "The following items are new and have been processed:\n"
for col in new_collections:
    issue_description += col + "\n"
ia_redmine.create_redmine_issue(ia_settings.redmine_username,ia_settings.redmine_password,redmine_url,project_id,issue_subject,issue_description)

# **************************
# SAVE COLLECTIONS TO DATABASE
# **************************

ia_getitems.add_item_to_db(collections_db,new_collections)


