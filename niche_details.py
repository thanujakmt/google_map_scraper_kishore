country = 'australia'
niche = 'nutritionist'
category = niche
country_code = 'au'
location_table = f'{country_code}_{niche}_locations'

gmbDataTableName = f'{country_code}_{category}_business_data'
location_in_progress_table = 'location_in_progress'
data_file_name = 'data.csv'
instance_id = 1

#note i changed pincode in code and pin_code in searchbusinessdata

collection_type = 2  #1 = Entire Database, 2 = State Wise





#<-------Databse Credential----------->

db_credential = {"dentist":{"user":"dentist","password":"EvenD!ngo52","database":"dentist_business_db"},
                "daycare":{"user":"daycare","password":"$illyAnt88","database":"daycare_business_db"},
                "remodeler":{"user":"remodeler","password":"$mallFork11","database":"remodeler_business_db"},
                "physiotherapist":{"user":"physiotherapist","password":"l@zyChalk74","database":"physiotherapist_business_db"},
                "chiropractor":{"user":"chiropractor","password":"longR@ad44","database":"chiropractor_business_db"},
                "mental_health_service":{"user":"mentalhealthservice","password":"g@ldNorth88","database":"mental_health_service_business_data"},
                "acupuncturists":{"user":"usa_acupuncturists_db","password":"smallOl!ve26","database":"usa_acupuncturists_db"},
                "yoga_studio":{"user":"usa_yoga_db","password":"SignBox76","database":"usa_yoga_db"},
                "massage_therapist" :{"user":"massage_therapist_business_db","password":"he@vyCamp24","database":"massage_therapist_business_db"},
                "naturopathic_practitioner" :{"user":"naturopathic_practitioner","password":"LionC@ve74","database":"naturopathic_practitioner_business_db"},
                "nutritionist" : {"user":"nutritionist_business_db","password":"wi$eFeast47","database":"nutritionist_business_db"}
                }
