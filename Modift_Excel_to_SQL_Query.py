import pandas as pd

input_file_path = 'file path with extension'

df = pd.read_excel(input_file_path)

output_data = []


dates = df['Date'].unique()

for date in dates:
    date_df = df[df['Date'] == date]

    for index, row in date_df.iterrows():
        name = row["Name"]

        try:
            last_part = name.split()[-1]
            site = int(''.join(filter(str.isdigit, last_part)))
        except (ValueError, AttributeError):
            site = 0

        if "Site" in df.columns:

            site_value = row["Site"]
        else:
            site_value = site


        formatted_date = "-".join([str(int(part)) for part in date.strftime("%d-%m-%Y").split("-")])

        for time_interval, qty in row.items():
            if time_interval != "Name" and time_interval != "Site" and time_interval != "Date":
                time_parts = time_interval.split('-')

                if len(time_parts) == 2:
                    start_time, end_time = time_parts
                    time_number = int(start_time.split(':')[0])


                    main_query = f"INSERT INTO trStoreVisitors (CompanyCode, OfficeCode, StoreCode, CurrentDate, CurrentHour, InVisitorCount, OutVisitorCount) VALUES (1, '{site_value}', '{site_value}', '{formatted_date}', {time_number}, {qty}, {qty})"

                    output_data.append({
                        "Name": name,
                        "Site": site_value,
                        "Date": formatted_date,
                        "Time": f"{start_time}-{end_time}",
                        "Time #": time_number,
                        "Qty": qty,
                        "Main Query": main_query
                    })

output_df = pd.DataFrame(output_data)

output_file_path = 'File_name.xlsx'
output_df.to_excel(output_file_path, index=False)
