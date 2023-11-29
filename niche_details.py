
country = 'united states of america'
niche = 'sound_healing'
category = niche
country_code = 'usa'
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
                "nutritionist" : {"user":"nutritionist_business_db","password":"wi$eFeast47","database":"nutritionist_business_db"},
                "meditation" : {"user":"meditation_business_db","password":"R!verFlow75","database":"meditation_business_db"},
                "ayurveda" : {"user":"ayurveda_business_db","password":"g@ldSand14","database":"ayurveda_business_db"},
                "energy_healer" : {"user":"energy_healer","password":"h@ppyTime34","database":"energy_healer_business_db"},
                "functional_medicine" : {"user":"functional_medicine","password":"curlyB!rd85","database":"functional_medicine_business_db"},
                "herbal_medicine" : {"user":"herbal_medicine","password":"lushAl@rm88","database":"herbal_medicine_business_db"},
                "reiki_healers" : {"user":"reiki_healers","password":"C@melRoad76","database":"reiki_healers_business_db"},
                "sound_therapy" : {"user":"sound_therapy","password":"sh!nyBeam15","database":"sound_therapy_business_db"},
                "Hypnotherapy" : {"user":"Hypnotherapy","password":"GoatH!ll76","database":"Hypnotherapy_business_db"},
                "reflexology" : {"user":"reflexology","password":"f@ncyKoala45","database":"reflexology_business_db"},
                "sound_healing" : {"user":"sound_healing","password":"sl!mSpring95","database":"sound_healing_business_db"}
                }
