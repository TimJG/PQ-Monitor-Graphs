import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import webbrowser
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


start_timestamp = "2024-05-16T00:00:00Z"
end_timestamp = "2024-06-20T23:59:59Z"
timetitle='Timestamp' 
voltagetitle='Voltage RMS'

# Call the function with modified arguments (assuming you want to use the filtered data)
filtered_data39 = filter_csv_by_timestamp(filename39, start_timestamp, end_timestamp, timetitle, output_filename='filtered_data39.csv')
filtered_data85 = filter_csv_by_timestamp(filename85, start_timestamp, end_timestamp, timetitle, output_filename='filtered_data85.csv')
filtered_data39[voltagetitle] = filtered_data39[voltagetitle] / 1000
filtered_data85[voltagetitle] = filtered_data85[voltagetitle] / 1000


print("Filtered data for different time range saved to filtered_data.csv")


app = Dash(__name__)

app.layout = html.Div([
    html.Header("PQ Monitors Data"),
    dcc.Dropdown(
        id='y-axis-data-dropdown',
        options=[{'label': col, 'value': col} for col in colnames],
        value=colnames[2]  # Initial selection (assuming 3rd element)
    ),
    dcc.Graph(id='graph')  # Add the graph component
])

@callback(
    Output('graph', 'figure'),  # Update the output to 'graph' for visualization
    Input('y-axis-data-dropdown', 'value')
)

def update_plot(selected_y_data):

  trace1 = go.Scatter(
      x=filtered_data39['Timestamp'],
      y=filtered_data39[selected_y_data],  # Use selected data column
      name="Data from " + filename39.split("/")[-1]
  )

  trace2 = go.Scatter(
      x=filtered_data85['Timestamp'],
      y=filtered_data85[selected_y_data],  # Use selected data column
      name="Data from " + filename85.split("/")[-1]
  )

  fig = go.Figure(data=[trace1, trace2])  # Add both traces to the figure

  # Set axis titles
  fig.update_xaxes(title_text="Time Stamp (s)")
  fig.update_yaxes(title_text="Voltage RMS (V)")  # Update y-axis title based on selection
  #fig.update_layout(title_text="PQ Monitors " + selected_y_data + " vs. Time ")

  return fig



# Define the URL of the website you want to launch
url = "http://127.0.0.1:8050/"  # Replace with the desired website URL

# Open the website in the default web browser
webbrowser.open(url)

print("Website launched:", url)

if __name__ == "__main__":
    app.run_server(debug=True)
