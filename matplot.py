import pandas as pd
import matplotlib.pyplot as plt
colnames = ['Sample','Line current RMS','Voltage RMS','Line mean active power','Line mean reactive power','Voltage frequency','Line power factor','Phase angle','Line mean apparant power','Forward active energy','Reverse active energy','Absolute active energy','Forward reactive energy','Reverse reactive energy','Absolute reactive energy','Metering status','System status','Temperature','Humidity','Timestamp','Unknown' ]
available_y_data_columns = colnames

def filter_csv_by_timestamp(filename, start_timestamp, end_timestamp, timetitle, output_filename=None):

# Define the start and end timestamps for the desired range (inclusive)


# Read the CSV file using pandas
    data = pd.read_csv(filename, header=None, names=colnames)

#filter values from device glitch
    values_to_remove = ["-3737246-12-13T17:53","-3526451-11-15T13:12"]
    data = data[~data["Timestamp"].isin(values_to_remove)]

# Convert the timestamp column to datetime format
    data[timetitle] = pd.to_datetime(data[timetitle], utc=True)  # Assuming "timestamp" is the column name

# Create a boolean mask to select rows within the desired range
    mask = (data[timetitle] >= start_timestamp) & (data[timetitle] <= end_timestamp)

# Extract the desired rows
    filtered_data = data[mask].sort_values(by=timetitle)
    
# You can now use the filtered_data dataframe for further analysis or write it to a new CSV file

# Optional: Write the filtered data to a new CSV file
    filtered_data.to_csv("filtered_data.csv", index=False)

    print("Rows within the specified timestamp range have been extracted!")

    if output_filename:
        filtered_data.to_csv(output_filename, index=False)

    return filtered_data


# Define the filename of your CSV files
filename39 = "/Users/timothygilda/Desktop/B8D61A015A39-2.csv"
filename85 = "/Users/timothygilda/Desktop/B8D61A016A85-2.csv"

# Define default output filename (optional)
default_output_filename = "filtered_data.csv"


start_timestamp = "2024-05-17T11:30:00Z"
end_timestamp = "2024-05-24T12:10:00Z"
timetitle='Timestamp' 
voltagetitle='Voltage RMS'

# Call the function with modified arguments (assuming you want to use the filtered data)
filtered_data39 = filter_csv_by_timestamp(filename39, start_timestamp, end_timestamp, timetitle, output_filename='filtered_data39.csv')
filtered_data85 = filter_csv_by_timestamp(filename85, start_timestamp, end_timestamp, timetitle, output_filename='filtered_data85.csv')
filtered_data39[voltagetitle] = filtered_data39[voltagetitle] / 1000
filtered_data85[voltagetitle] = filtered_data85[voltagetitle] / 1000


print("Filtered data for different time range saved to filtered_data.csv")

plt.plot(filtered_data39['Timestamp'],filtered_data39['Line current RMS'], label='Device 39')
plt.plot(filtered_data85['Timestamp'],filtered_data85['Line current RMS'], label='Device 85')
plt.ylim(-1, 40)
plt.xticks(rotation=45)
plt.xlabel("Timestamp")
plt.ylabel("Line Current RMS (mA)")
plt.legend()
plt.show(block=True)