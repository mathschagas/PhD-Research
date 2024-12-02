# Read files from results folder
import pandas as pd


# Directories
ucbr_dir = "results/u-cbr"
random_dir = "results/random"

# Scenarios
scenarios = [
    "NoConstraints",
    "1Constraint",
    "2Constraints",
    "3Constraints",
    "HardConstraints"
]

# Uncertainties
uncertainties = [
    "internal_failure_drone",
    "internal_failure_car",
    "bad_weather",
    "restricted_area",
    "traffic_jam",
]


def get_component_type_values(uncertainty, df, type):
    """Get the values for each component type"""

    initial_is_drone = (uncertainty == "internal_failure_drone") or (uncertainty == "bad_weather")
    
    amount = df['Best_Component_Type'].value_counts().get(type, 0)
    
    if type == 'drone':
        if initial_is_drone:
            total = 45
        else:
            total = 36
    elif type == 'car':
        if initial_is_drone:
            total = 36
        else:
            total = 45
    elif type == 'bicycle':
        total = 27
    elif type == 'truck':
        total = 18
    elif type == 'pedestrian':
        total = 9
    else:
        total = 0
    
    type_ratio = f"{amount}/{total}"
    type_percentage = (amount / total) * 100 if total > 0 else 0
    type_fpercentage = f"{type_percentage:.2f}%"

    completed_missions = df[(df['Best_Component_Type'] == type) & (df['Mission_Completed'] == 'Yes')]
    completed_missions_percentage = (len(completed_missions) / amount) * 100 if amount > 0 else 0
    completed_missions_fpercentage = f"{completed_missions_percentage:.2f}%"
    completed_missions_ratio_percentage = f'{len(completed_missions)}/{amount} ({completed_missions_fpercentage})'
    
    return type_ratio, type_fpercentage, completed_missions_ratio_percentage


def get_component_completed_mission(df):
    """Get the values of completed missions"""
    total = len(df)
    mc_yes_count = df['Mission_Completed'].value_counts().get('Yes', 0)
    mc_ratio = f"{mc_yes_count}/{total}"
    mc_percentage = (mc_yes_count / total) * 100 if total > 0 else 0
    mc_fpercentage = f"{mc_percentage:.2f}%"
    return mc_ratio, mc_fpercentage


def get_component_cbr_attribute_values(df, attribute):
    """Get the values for each component CBR attribute"""
    min = df[f'_cbr_{attribute}'].min()
    max = df[f'_cbr_{attribute}'].max()
    avg = df[f'_cbr_{attribute}'].mean()
    return min, max, avg


def get_component_penalty_values(df, constraint):
    """Get the values for each component penalty"""
    total = len(df)
    column_name = f'_raw_penalty_{constraint}'
    if column_name not in df.columns:
        return 'N/A', 'N/A'
    penalty_amount = df.get(column_name, pd.Series([0])).sum()
    penalty_ratio = f"{round(penalty_amount)}/{total}"
    penalty_percentage = (penalty_amount / total) * 100 if total > 0 else 0
    penalty_fpercentage = f"{penalty_percentage:.2f}%"
    return penalty_ratio, penalty_fpercentage


def compile_results():
    """Compile results from the results folder"""
    for uncertainty in uncertainties:
        output_filename = f"{uncertainty}.xlsx"
        writer = pd.ExcelWriter(output_filename, engine='openpyxl')

        for scenario in scenarios:
            results_dfs = {}
    
            # File names for each simulation setting
            random_filename = f"{random_dir}/transformed_{scenario}Bin.xlsx"
            ucbr_bin_filename = f"{ucbr_dir}/transformed_{scenario}Bin.xlsx"
    
            # Instantiate each file into a df and append to results_dfs
            results_dfs['Random'] = pd.read_excel(random_filename)
            results_dfs['U-CBR Bin'] = pd.read_excel(ucbr_bin_filename)

            if scenario == "NoConstraints":
                ucbr_wp_filename = f"{ucbr_dir}/transformed_NoConstraintsWeightedPrice.xlsx"
                results_dfs['U-CBR Price'] = pd.read_excel(ucbr_wp_filename)
                ucbr_wt_filename = f"{ucbr_dir}/transformed_NoConstraintsWeightedTimeToDeliver.xlsx"
                results_dfs['U-CBR Time'] = pd.read_excel(ucbr_wt_filename)
            else:
                ucbr_likert_filename = f"{ucbr_dir}/transformed_{scenario}Likert.xlsx"
                results_dfs['U-CBR Likert'] = pd.read_excel(ucbr_likert_filename)

            scenario_outputs = []
            for df_name, df in results_dfs.items():
                # Mission_Completed
                mc_ratio, mc_fpercentage = get_component_completed_mission(df)

                # Component Types
                drone_ratio, drone_fpercentage, drone_success_rate = get_component_type_values(uncertainty, df, 'drone')
                car_ratio, car_fpercentage, car_success_rate = get_component_type_values(uncertainty, df, 'car')
                bicycle_ratio, bicycle_fpercentage, bicycle_success_rate = get_component_type_values(uncertainty, df, 'bicycle')
                truck_ratio, truck_fpercentage, truck_success_rate = get_component_type_values(uncertainty, df, 'truck')
                pedestrian_ratio, pedestrian_fpercentage, pedestrian_success_rate = get_component_type_values(uncertainty, df, 'pedestrian')
                
                # Time to Deliver and Price
                time_to_deliver_min, time_to_deliver_max, time_to_deliver_avg = get_component_cbr_attribute_values(df, 'time_to_deliver')
                price_min, price_max, price_avg = get_component_cbr_attribute_values(df, 'price')

                # Penalty for not delivering on time, price too high, and not using secure container
                penalty_time_to_deliver_ratio, penalty_time_to_deliver_fpercentage = get_component_penalty_values(df, 'time_to_deliver')
                penalty_price_ratio, penalty_price_fpercentage = get_component_penalty_values(df, 'price')
                penalty_secure_container_ratio, penalty_secure_container_fpercentage = get_component_penalty_values(df, 'secure_container')

                # Append to scenario_outputs
                scenario_outputs.append({
                    'Approach': df_name,
                    'Mission Completed (%)': f'{mc_ratio} ({mc_fpercentage})',
                    'Drone (%)': f'{drone_ratio} ({drone_fpercentage})',
                    'Drone Success Rate (%)': drone_success_rate,
                    'Car (%)': f'{car_ratio} ({car_fpercentage})',
                    'Car Success Rate (%)': car_success_rate,
                    'Bicycle (%)': f'{bicycle_ratio} ({bicycle_fpercentage})',
                    'Bicycle Success Rate (%)': bicycle_success_rate,
                    'Truck (%)': f'{truck_ratio} ({truck_fpercentage})',
                    'Truck Success Rate (%)': truck_success_rate,
                    'Pedestrian (%)': f'{pedestrian_ratio} ({pedestrian_fpercentage})',
                    'Pedestrian Success Rate (%)': pedestrian_success_rate,
                    'Time to Deliver': f'MIN = {time_to_deliver_min}\nMAX = {time_to_deliver_max}\nAVG = {round(time_to_deliver_avg, 2)}'.replace(',', '.'),
                    'Price': f'MIN = {price_min}\nMAX = {price_max}\nAVG = {round(price_avg, 2)}'.replace(',', '.'),
                    'Time to Deliver > 60 (%)': f'{penalty_time_to_deliver_ratio} ({penalty_time_to_deliver_fpercentage})',
                    'Price > 100 (%)': f'{penalty_price_ratio} ({penalty_price_fpercentage})',
                    'Secure Container == FALSE (%)': f'{penalty_secure_container_ratio} ({penalty_secure_container_fpercentage})',
                })
            
            # Write to Excel
            scenario_df = pd.DataFrame(scenario_outputs).transpose()
            scenario_df.to_excel(writer, sheet_name=scenario, index=True)
           
        writer.close()
 

if __name__ == "__main__":
    compile_results()