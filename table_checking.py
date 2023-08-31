import os
import time
import json
from databaseConnection import dbConnection
# from niche_details import country_code


def check_table_is_exist(table_name,myCursor):
        query = f'show tables like "%{table_name}%"'
        try:
                myCursor.execute(query)
                table = myCursor.fetchall()
        except:
                try:
                        myDatabase, myCursor = dbConnection()
                        myCursor.execute(query)
                        table = myCursor.fetchall()
                except Exception as e:
                        print(e)


        if len(table) == 0:
                print('no')
                return False
               
        else:
                return True

def create_table(category,myCursor,myDatabase,country,country_code):
        query = f'''CREATE TABLE `{country_code}_{category}_business_data` (
  `gl_id` int NOT NULL AUTO_INCREMENT,
  `gl_website` varchar(255) DEFAULT NULL,
  `gl_unique_website_flag` tinyint(1) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `description` text,
  `gl_business_name` varchar(255) DEFAULT NULL,
  `gl_ratings` varchar(255) DEFAULT NULL,
  `gl_telephone` varchar(255) DEFAULT NULL,
  `telephone_type` varchar(255) DEFAULT NULL,
  `gl_address` varchar(255) DEFAULT NULL,
  `gl_gmb_photos_count` varchar(255) DEFAULT NULL,
  `gl_reviews` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `gmb_category` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `email_done_flag` tinyint(1) DEFAULT NULL,
  `custom_scrapped_email_done_flag` tinyint(1) DEFAULT NULL,
  `pincode` int DEFAULT NULL,
  `pincode_done_flag` tinyint(1) DEFAULT NULL,
  `gl_url` varchar(600) DEFAULT NULL,
  `gl_url_done_flag` tinyint(1) DEFAULT NULL,
  `country_code` int DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `country_done_flag` tinyint(1) DEFAULT NULL,
  `state_code` int DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `state_done_flag` tinyint(1) DEFAULT NULL,
  `district_code` int DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `district_done_flag` tinyint(1) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `se_is_qualified_flag` tinyint(1) DEFAULT NULL,
  `se_title` varchar(255) DEFAULT NULL,
  `se_categories` varchar(255) DEFAULT NULL,
  `se_domain_authority` int DEFAULT NULL,
  `se_page_authority` int DEFAULT NULL,
  `se_total_backlinks` int DEFAULT NULL,
  `se_quality_backlinks` int DEFAULT NULL,
  `se_quality_backlinks_percentage` varchar(255) DEFAULT NULL,
  `se_moztrust` int DEFAULT NULL,
  `se_spam_score` int DEFAULT NULL,
  `se_trust_flow` int DEFAULT NULL,
  `se_citation_flow` int DEFAULT NULL,
  `se_indexed_urls` int DEFAULT NULL,
  `se_do_follow_links` varchar(255) DEFAULT NULL,
  `se_no_follow_links` varchar(255) DEFAULT NULL,
  `total_seo_request_send` int DEFAULT NULL,
  `se_done_flag` tinyint(1) DEFAULT NULL,
  `ws_urls` int DEFAULT NULL,
  `ws_blogs` int DEFAULT NULL,
  `ws_total_word_count` int DEFAULT NULL,
  `ws_avg_blog_word_count` int DEFAULT NULL,
  `ws_done_flag` tinyint(1) DEFAULT NULL,
  `request_response_code` int DEFAULT NULL,
  `is_business_site` tinyint(1) DEFAULT NULL,
  `web_technologies` varchar(555) DEFAULT NULL,
  `is_wordpress` tinyint(1) DEFAULT NULL,
  `wp_plugins` varchar(555) DEFAULT NULL,
  `state_start_flag` tinyint(1) DEFAULT NULL,
  `gmp_coordinate` text,
  `gmb_images` json DEFAULT NULL,
  `custom_website_flag` tinyint(1) DEFAULT NULL,
  `verified_email_id` json DEFAULT NULL,
  `verified_email_id_start_flag` tinyint(1) DEFAULT NULL,
  `verified_email_id_flag` tinyint(1) DEFAULT NULL,
  `https_flag` tinyint(1) DEFAULT NULL,
  `http_flag` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`gl_id`),
  UNIQUE KEY `gl_id_UNIQUE` (`gl_id`),
  UNIQUE KEY `gl_url_UNIQUE` (`gl_url`)
)
        '''
        
        
        location_table_query = f'CREATE TABLE {country_code}_{category}_locations AS SELECT * FROM {country_code}_locations'

        alter_query = f'''ALTER TABLE `{country_code}_{category}_locations` 
                        ADD COLUMN `location_flag_stop` TINYINT(1) NULL AFTER `city`,
                        ADD COLUMN `location_flag_start` TINYINT(1) NULL AFTER `location_flag_stop`;
                        '''

        try:
                #<-------------creating data table--------------->
                myCursor.execute(query)
                myDatabase.commit()
                #<---------creating location table and copying all data from usa_location_meta_data------------>
                myCursor.execute(location_table_query)
                myDatabase.commit()
                time.sleep(5)
                #<--------drop and re-create start and stop flag------->
                myCursor.execute(alter_query)
                myDatabase.commit()
        
        except:
                try:
                        myDatabase,myCursor = dbConnection()
                        #<-------------creating data table--------------->
                        myCursor.execute(query)
                        myDatabase.commit()
                        #<---------creating location table and copying all data from usa_location_meta_data------------>
                        # myCursor.execute(location_table_query)
                        # myDatabase.commit()
                        time.sleep(5)
                        #<--------drop and re-create start and stop flag------->
                        myCursor.execute(alter_query)
                        myDatabase.commit()
                except Exception as e:
                        print(e)

        
def is_table_exist_and_create(myDatabase,myCursor,category,country_code, country):
        table_name = f'{country_code}_{category}_business_data'
        is_exist_table = check_table_is_exist(table_name= table_name,myCursor= myCursor)
        print(is_exist_table)
        if not is_exist_table:
                create_table(category= category,myCursor= myCursor, myDatabase= myDatabase,country= country , country_code= country_code)
                print(f'{table_name} is created')
        else:
                print('Tables Already Exist')

if __name__ == '__main__':
        # chiropractor
        myDatabase, myCursor = dbConnection()
        category= 'dentist'
        is_table_exist_and_create(myDatabase,myCursor,category)
        



#         ALTER TABLE `usa_dent_db`.`dentist_locations` 
# DROP COLUMN `chiropractor_flag_stop`,
# DROP COLUMN `chiropractor_flag_start`;




































# # with open('address.txt','w') as f:
# #         f.write('address')
# #         f.close()
# # # time.sleep(5)
# # os.remove('address.txt')
# with open('address.txt','r') as f:
#         loc = f.readline()
        
#         f.close()
# # print(loc)
# add = '{"aaa": 1}'
# loc = loc.replace("'","\"")
# # print(add)
# dictt = json.loads(loc)
# # print(add)

# # print(dictt)
# print(type(dictt))
# print(dictt['district'])

# if os.path.exists(os.path.join(os.getcwd(),'address.txt')):
#         print("yes")
#         # address = fetch_address_from_address_text_file()
#         # loc['address'] = address