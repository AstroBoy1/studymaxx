import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load data from Excel sheet
# excel_file = "proxy_data.xlsx"
# df = pd.read_excel(excel_file)
# Define the data as a list of dictionaries
data = [
    {"Student Name": "Havel", "Subject": "CS 391", "Study Time": "01:00:00"},
    {"Student Name": "Havel", "Subject": "MRKT 237", "Study Time": "01:00:00"},
    {"Student Name": "Havel", "Subject": "MTH 254", "Study Time": "02:30:00"},
    {"Student Name": "Havel", "Subject": "PH 212", "Study Time": "03:15:00"},
    {"Student Name": "Josh", "Subject": "WR 121", "Study Time": "01:00:00"},
    {"Student Name": "Josh", "Subject": "BA 348", "Study Time": "02:30:00"},
    {"Student Name": "Josh", "Subject": "CS 340", "Study Time": "03:15:00"},
    {"Student Name": "Josh", "Subject": "BANA 270", "Study Time": "01:00:00"},
    {"Student Name": "Kai", "Subject": "CS 162", "Study Time": "05:20:00"},
    {"Student Name": "Kai", "Subject": "MTH 251", "Study Time": "04:00:00"},
    {"Student Name": "Kai", "Subject": "MRKT 237", "Study Time": "05:20:00"},
    {"Student Name": "Kai", "Subject": "CS 271", "Study Time": "04:00:00"},
    {"Student Name": "Omori", "Subject": "MTH 251", "Study Time": "03:15:00"},
    {"Student Name": "Omori", "Subject": "CS 162", "Study Time": "02:00:00"},
    {"Student Name": "Omori", "Subject": "AI 537", "Study Time": "03:15:00"},
    {"Student Name": "Omori", "Subject": "AI 541", "Study Time": "02:00:00"},
    {"Student Name": "Owen", "Subject": "BIO 101", "Study Time": "00:10:00"},
    {"Student Name": "Owen", "Subject": "CS 271", "Study Time": "01:00:00"},
    {"Student Name": "Owen", "Subject": "MTH 361", "Study Time": "05:00:00"},
    {"Student Name": "Owen", "Subject": "BA 348", "Study Time": "00:10:00"},
    {"Student Name": "Paul", "Subject": "CS 340", "Study Time": "01:00:00"},
    {"Student Name": "Paul", "Subject": "BANA 270", "Study Time": "05:00:00"},
    {"Student Name": "Paul", "Subject": "BANA 372", "Study Time": "02:00:00"},
    {"Student Name": "Paul", "Subject": "MTH 241", "Study Time": "01:00:00"},
    {"Student Name": "Paul", "Subject": "BANA 472", "Study Time": "02:00:00"},
    {"Student Name": "Paul", "Subject": "BA 348", "Study Time": "01:00:00"},
    {"Student Name": "Tri", "Subject": "CS 340", "Study Time": "04:00:00"},
    {"Student Name": "Tri", "Subject": "BANA 270", "Study Time": "04:00:00"},
    {"Student Name": "Vi", "Subject": "MTH 241", "Study Time": "02:30:00"},
    {"Student Name": "Vi", "Subject": "BANA 472", "Study Time": "05:20:00"},
    {"Student Name": "Vi", "Subject": "BA 348", "Study Time": "00:09:00"},
    {"Student Name": "Vi", "Subject": "CS 162", "Study Time": "02:00:00"},
    {"Student Name": "Vi", "Subject": "ENG 100", "Study Time": "02:30:00"},
    {"Student Name": "Vi", "Subject": "BANA 450", "Study Time": "05:20:00"},
    {"Student Name": "Vi", "Subject": "CS 271", "Study Time": "00:09:00"},
]

# Create a DataFrame from the data
df = pd.DataFrame(data)
# Convert 'Study Time' to total hours
def convert_to_hours(time_obj):
    if isinstance(time_obj, str):
        h, m, s = map(int, time_obj.split(':'))
    else:
        h, m, s = time_obj.hour, time_obj.minute, time_obj.second
    return h + m / 60 + s / 3600

df['StudyTime(Hours)'] = df['Study Time'].apply(convert_to_hours)

# Function to create the Dash app
def create_dashboard(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')

    dash_app.layout = html.Div([
        html.Div([
            html.Label("Select Student:"),
            dcc.Dropdown(
                id='student-dropdown',
                options=[{'label': student, 'value': student} for student in df['Student Name'].unique()],
                value=df['Student Name'].unique()[0]  # Default selected student
            ),
        ]),
        dcc.Graph(id='study-time-bar-chart'),
        dcc.Graph(id='leaderboard-bar-chart'),
    ])

    @dash_app.callback(
        Output('study-time-bar-chart', 'figure'),
        Input('student-dropdown', 'value')
    )
    def update_study_time_chart(selected_student):
        filtered_df = df[df['Student Name'] == selected_student]
        fig = px.bar(filtered_df, x='Subject', y='StudyTime(Hours)', title=f"Study Time for {selected_student}",
                     color_discrete_sequence=['#2d2d2d'])  # Set bar color to charcoal grey
        return fig

    @dash_app.callback(
        Output('leaderboard-bar-chart', 'figure'),
        Input('student-dropdown', 'value')
    )
    def update_leaderboard_chart(selected_student):
        student_totals = df.groupby('Student Name')['StudyTime(Hours)'].sum().reset_index()
        student_totals = student_totals.sort_values(by='StudyTime(Hours)', ascending=False)
        fig = px.bar(student_totals, x='Student Name', y='StudyTime(Hours)', title="Study Time Leaderboard",
                     color_discrete_sequence=['#2d2d2d'])  # Set bar color to charcoal grey
        return fig

    return dash_app