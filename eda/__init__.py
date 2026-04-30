import os

root_dir = "../"
data_dir = "data/"
clean_dir = "clean/"
joins_dir = "joins/"

root_dir = os.path.abspath(os.path.join(os.getcwd(), "..")) + os.sep
data_dir = data_dir
clean_dir = clean_dir

root_data_dir = os.path.join(root_dir, data_dir)
root_data_clean_dir = os.path.join(root_data_dir, clean_dir)
root_data_clean_joins_dir = os.path.join(root_data_clean_dir, joins_dir)


tableau_snake_case_names = {
    'all_categories_occupation': 'all_occupations',
    'total_all_usual_residents_aged_16_years_and_over_in_employment_the_week_before_the_census_x': 'all_occupations',
    '1._managers,_directors_and_senior_officials': 'managers_directors_and_senior_officials',
    '2._professional_occupations': 'professional_occupations',
    '3._associate_professional_and_technical_occupations': 'associate_prof_and_tech',
    '4._administrative_and_secretarial_occupations': 'admin_and_secretarial',
    '5._skilled_trades_occupations': 'skilled_trades_occupations',
    '6._caring,_leisure_and_other_service_occupations': 'caring_and_leisure',
    '7._sales_and_customer_service_occupations': 'sales_and_customer_service',
    '8._process,_plant_and_machine_operatives': 'process_plant_and_machine_operatives',
    '8._process_plant_and_machine_operatives': 'process_plant_and_machine_operatives',
    '9._elementary_occupations': 'elementary_occupations',
    'total_all_usual_residents_aged_16_years_and_over_in_employment_the_week_before_the_census_y': 'all_industries',
    'a_agriculture,_forestry_and_fishing': 'agriculture_forestry_and_fishing',
    'b_mining_and_quarrying': 'mining_and_quarrying',
    'c_manufacturing': 'manufacturing',
    'd_electricity,_gas,_steam_and_air_conditioning_supply': 'utilities_energy',
    'e__water_supply;_sewerage,_waste_management_and_remediation_activities': 'water_and_waste_management',
    'e_water_supply;_sewerage,_waste_management_and_remediation_activities': 'water_and_waste_management',
    'f_construction': 'construction',
    'g_wholesale_and_retail_trade;_repair_of_motor_vehicles_and_motorcycles': 'wholesale_and_retail',
    'g_wholesale_and_retail_trade;_repair_of_motor_vehicles_and_motor_cycles': 'wholesale_and_retail',
    'h_transport_and_storage': 'transport_and_storage',
    'i_accommodation_and_food_service_activities': 'accommodation_and_food',
    'j_information_and_communication': 'information_and_communication',
    'k_financial_and_insurance_activities': 'financial_and_insurance',
    'l_real_estate_activities': 'real_estate_activities',
    'm_professional,_scientific_and_technical_activities': 'professional_and_scientific',
    'n_administrative_and_support_service_activities': 'admin_and_support_services',
    'o_public_administration_and_defence;_compulsory_social_security': 'public_admin_and_defence',
    'p_education': 'education',
    'q_human_health_and_social_work_activities': 'health_and_social_work',
    'r,_s,_t,_u_other': 'other_services'
}


census_ethnicity_mapping_2011 = {
    'all_usual_residents': 'total_population',
    'white': 'white_total',
    'white_english_welsh_scottish_northern_irish_british': 'white_british',
    'white_irish': 'white_irish',
    'white_gypsy_or_irish_traveller': 'white_gypsy_traveller',
    'white_other_white': 'white_other',
    'mixed_multiple_ethnic_groups': 'mixed_total',
    'mixed_multiple_ethnic_groups_white_and_black_caribbean': 'mixed_white_black_caribbean',
    'mixed_multiple_ethnic_groups_white_and_black_african': 'mixed_white_black_african',
    'mixed_multiple_ethnic_groups_white_and_asian': 'mixed_white_asian',
    'mixed_multiple_ethnic_groups_other_mixed': 'mixed_other',
    'asian_asian_british': 'asian_total',
    'asian_asian_british_indian': 'asian_indian',
    'asian_asian_british_pakistani': 'asian_pakistani',
    'asian_asian_british_bangladeshi': 'asian_bangladeshi',
    'asian_asian_british_chinese': 'asian_chinese',
    'asian_asian_british_other_asian': 'asian_other',
    'black_african_caribbean_black_british': 'black_total',
    'black_african_caribbean_black_british_african': 'black_african',
    'black_african_caribbean_black_british_caribbean': 'black_caribbean',
    'black_african_caribbean_black_british_other_black': 'black_other',
    'other_ethnic_group': 'other_total',
    'other_ethnic_group_arab': 'other_arab',
    'other_ethnic_group_any_other_ethnic_group': 'other_remaining'
}


census_ethnicity_mapping_2021 = {
    'total_all_usual_residents': 'total_population',
    'white': 'white_total',
    'white_english,_welsh,_scottish,_northern_irish_or_british': 'white_british',
    'white_irish': 'white_irish',
    'white_gypsy_or_irish_traveller': 'white_gypsy_traveller',
    'white_roma': 'white_roma',
    'white_other_white': 'white_other',
    'asian,_asian_british_or_asian_welsh': 'asian_total',
    'asian,_asian_british_or_asian_welsh_bangladeshi': 'asian_bangladeshi',
    'asian,_asian_british_or_asian_welsh_chinese': 'asian_chinese',
    'asian,_asian_british_or_asian_welsh_indian': 'asian_indian',
    'asian,_asian_british_or_asian_welsh_pakistani': 'asian_pakistani',
    'asian,_asian_british_or_asian_welsh_other_asian': 'asian_other',
    'black,_black_british,_black_welsh,_caribbean_or_african': 'black_total',
    'black,_black_british,_black_welsh,_caribbean_or_african_african': 'black_african',
    'black,_black_british,_black_welsh,_caribbean_or_african_caribbean': 'black_caribbean',
    'black,_black_british,_black_welsh,_caribbean_or_african_other_black': 'black_other',
    'mixed_or_multiple_ethnic_groups': 'mixed_total',
    'mixed_or_multiple_ethnic_groups_white_and_asian': 'mixed_white_asian',
    'mixed_or_multiple_ethnic_groups_white_and_black_african': 'mixed_white_black_african',
    'mixed_or_multiple_ethnic_groups_white_and_black_caribbean': 'mixed_white_black_caribbean',
    'mixed_or_multiple_ethnic_groups_other_mixed_or_multiple_ethnic_groups': 'mixed_other',
    'other_ethnic_group': 'other_total',
    'other_ethnic_group_arab': 'other_arab',
    'other_ethnic_group_any_other_ethnic_group': 'other_remaining'
}