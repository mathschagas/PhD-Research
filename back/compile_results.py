# Read files from results folder
import pandas as pd

ucbr_dir = "results/u-cbr"
random_dir = "results/random"

scenarios = [
    "NoConstraints",
    "1Constraint",
    "2Constraints",
    "3Constraints",
    "HardConstraints"
]

uncertainties = [
    "internal_failure_drone",
    "internal_failure_car",
    "bad_weather",
    "restricted_area",
    "traffic_jam",
]

for uncertainty in uncertainties:
    output_filename = f"{uncertainty}.xlsx"
    for scenario in scenarios:
        results_dfs = []
 
        # File names for each simulation setting
        random_filename = f"{random_dir}/transformed_{scenario}Bin.xlsx"
        ucbr_bin_filename = f"{ucbr_dir}/transformed_{scenario}Bin.xlsx"
 
        # Instantiate each file into a df and append to results_dfs
        results_dfs.append(pd.read_excel(random_filename))
        results_dfs.append(pd.read_excel(ucbr_bin_filename))

        if scenario == "NoConstraints":
            ucbr_wp_filename = f"{ucbr_dir}/transformed_NoConstraintsWeightedPrice.xlsx"
            results_dfs.append(pd.read_excel(ucbr_wp_filename))
            ucbr_wt_filename = f"{ucbr_dir}/transformed_NoConstraintsWeightedTimeToDeliver.xlsx"
            results_dfs.append(pd.read_excel(ucbr_wt_filename))
        else:
            ucbr_likert_filename = f"{ucbr_dir}/transformed_{scenario}Likert.xlsx"
            results_dfs.append(pd.read_excel(ucbr_likert_filename))

        for df in results_dfs:
            # Mission_Completed
            mc_yes_count = df['Mission_Completed'].value_counts().get('Yes', 0)
            mc_total = df['Mission_Completed'].count()
            mc_ratio = f"{mc_yes_count}/{mc_total}"
            mc_percentage = (mc_yes_count / mc_total) * 100 if mc_total > 0 else 0
            mc_fpercentage = f"{mc_percentage:.2f}%"

            # Component Types
            drone_amount = df['drone'].value_counts().get('drone', 0)
            car_amount = df['car'].value_counts().get('car', 0)
            bicycle_amount = df['bicycle'].value_counts().get('bicycle', 0)
            truck_amount = df['truck'].value_counts().get('truck', 0)
            pedestrian_amount = df['pedestrian'].value_counts().get('pedestrian', 0)
            types_total = len(df)
            if uncertainty == "internal_failure_drone" or uncertainty == "bad_weather":
                drone_ratio = f"{drone_amount}/45"
                drone_percentage = (drone_amount / 45) * 100 if types_total > 0 else 0
                drone_fpercentage = f"{drone_percentage:.2f}%"
                car_ratio = f"{car_amount}/36"
                car_percentage = (car_amount / 36) * 100 if types_total > 0 else 0
                car_fpercentage = f"{car_percentage:.2f}%"
            else:
                car_ratio = f"{car_amount}/45"
                car_percentage = (car_amount / 45) * 100 if types_total > 0 else 0
                car_fpercentage = f"{car_percentage:.2f}%"
                drone_ratio = f"{drone_amount}/36"
                drone_percentage = (drone_amount / 36) * 100 if types_total > 0 else 0
                drone_fpercentage = f"{drone_percentage:.2f}%"
            bicycle_ratio = f"{bicycle_amount}/27"
            bicycle_percentage = (bicycle_amount / types_total) * 100 if types_total > 0 else 0
            bicycle_fpercentage = f"{bicycle_percentage:.2f}%"
            truck_ratio = f"{truck_amount}/18"
            truck_percentage = (truck_amount / types_total) * 100 if types_total > 0 else 0
            truck_fpercentage = f"{truck_percentage:.2f}%"
            pedestrian_ratio = f"{pedestrian_amount}/9"            
            pedestrian_percentage = (pedestrian_amount / types_total) * 100 if types_total > 0 else 0
            pedestrian_fpercentage = f"{pedestrian_percentage:.2f}%"

            print('!')
            

# Compile results into a single dataframe


# Save the dataframe as a xlsx file