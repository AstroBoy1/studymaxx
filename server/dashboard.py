import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load data from Excel sheet
excel_file = "proxy_data.csv"  # Replace with your Excel file name
df = pd.read_csv(excel_file)

# Convert 'Study Time' to total hours
def convert_to_hours(time_obj):
    if isinstance(time_obj, str):
        h, m, s = map(int, time_obj.split(':'))
    else:
        h, m, s = time_obj.hour, time_obj.minute, time_obj.second
    return h + m / 60 + s / 3600

df['StudyTime(Hours)'] = df['Study Time'].apply(convert_to_hours)

# Define a list of colors
colors = ['#646363', '#424242', '#212121']

# Ensure there are enough colors for all students by cycling through the list
unique_students = df['Student Name'].unique()
student_colors = {student: colors[i % len(colors)] for i, student in enumerate(unique_students)}

# Initialize the Dash app
#app = dash.Dash(__name__)
def create_dashboard(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')
    dash_app.layout = html.Div([
        html.Div([
            html.Label("Select Student:"),
            dcc.Dropdown(
                id='student-dropdown',
                options=[{'label': student, 'value': student} for student in df['Student Name'].unique()],
                value=df['Student Name'].unique()[0]  # Default selected student, the first student from the excel sheet.
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
                    color_discrete_sequence=[student_colors[selected_student]])  # Use the student's assigned color
        return fig

    @dash_app.callback(
        Output('leaderboard-bar-chart', 'figure'),
        Input('student-dropdown', 'value')
    )
    def update_leaderboard_chart(selected_student):
        student_totals = df.groupby('Student Name')['StudyTime(Hours)'].sum().reset_index()
        student_totals = student_totals.sort_values(by='StudyTime(Hours)', ascending=False)
        fig = px.bar(student_totals, x='Student Name', y='StudyTime(Hours)', title="Study Time Leaderboard",
                    color='Student Name', color_discrete_map=student_colors)  # Use the color mapping for all students
        return fig
    return dash_app

# if __name__ == '__main__':
#     print("Starting Dash application...")
#     app.run(debug=True)