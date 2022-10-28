searchAddressQuery = f'select pincode,location from usa_location_meta_data where state = "{state}" and district = "{district}"'
districtQuery = f'select district_name from district where state_name = "{state}" and country_name = "{country}"'
stateQuery = f'select state_name from state where country_name = "{country}"'