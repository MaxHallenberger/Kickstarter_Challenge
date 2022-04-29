### Target

state (str) : gives information about the status of the project; includes Successful, failed, live



### Important

converted_pledged_amount (int) : pledged amount (converted to usd)


country (str) : Country of origin of the project



currency (str) : code indicating the currency


category (dict) : Contains a variety of data including id, name, slug, and url etc., cluttered - extract categories and delete rest



deadline (int) : unix time stamp for the deadline date


disable_communication (bool) : True, false depending if the creator communicates with backers


goal (float) : How much has to be donated for a project to be successful


launched_at (float) : Unix timestamp indicating the date of launch



staff_pick (bool) : True or False depending if the project is picked by the staff


state_changed_at (str) : Unix timestamp when the state of the project changed


usd_pledged (float) : How much was pledged in terms of USD



### Delete 

blurb (str) : Short summary of the project by the creator


currency_symbol (str) : symbol for the currency


id (str) : Project id


backers_count (int) : Number of people backing the kickstarter


is_backing (object) : Describes if a creator is also backing other projects 


permissions (object) : Almost only zero values, gets kicked (meaning unknown)


is_starred (object) : Almost only zero values, gets kicked (meaning unknown)


urls (dict) : Dictionary including the url of the project 


source_url (dict) : Dictionary including the source url of the project


slug (str) : Includes a short abbreviation of the project


name (str) : Name of the project 


static_usd_rate (float) : exchange rate applied for the project


profile (dict) : User information


friends (int) : includes the number of friends a creator has, almost no values


spotlight (dict) : Spotlight page for funded projects


is_starrable (bool) : If a project can be bookmarked


photo (dict) : dictionary containing the rel. file path of a project image


pledged (int) : amount of money pledged to the project (redundant with converted value)


usd_type (str) : International vs. domestic


creator (dict) : dictionary containing the user information of the creator, seems mostly irrelevant


created_at (int) : unix timestamp indicating the time of creation, not needed


location (dict) : Dictionary containing the location information of a creator, only country is needed, so delete

