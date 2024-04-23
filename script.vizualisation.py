import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'final\\fusion_fichier.xlsx'
excel_data = pd.read_excel(file_path, sheet_name=None)  # Change to your actual file path and sheet names

# Assume we're working with 'Sheet1'
vote_data = excel_data['Sheet1'][["Libellé de la commune", "Gauche_2017", "Milieu_2017", "Droite_2017", "Gauche_2022", "Milieu_2022", "Droite_2022"]]
grouped_vote_data = vote_data.groupby("Libellé de la commune").sum()

# Function to create a plot for each political orientation
def create_voting_trend_plot(data, columns, title, colors, file_name):
    plt.figure(figsize=(15, 5))
    data[columns].plot(kind='bar', color=colors)
    plt.title(title)
    plt.ylabel('Vote Count')
    plt.legend(columns)
    plt.xticks(rotation=90)  # Rotate the x-tick labels for visibility
    plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels
    file_path = f'/path/to/output/{file_name}'  # Change to your desired output path
    plt.savefig(file_path)
    plt.close()
    return file_path

# Create and save the plots
left_wing_path = create_voting_trend_plot(
    grouped_vote_data,
    ['Gauche_2017', 'Gauche_2022'],
    'Trends in Left-wing Voting',
    ['blue', 'lightblue'],
    'left_wing_voting_trends_readable.png'
)

center_path = create_voting_trend_plot(
    grouped_vote_data,
    ['Milieu_2017', 'Milieu_2022'],
    'Trends in Center Voting',
    ['orange', 'peachpuff'],
    'center_voting_trends_readable.png'
)

right_wing_path = create_voting_trend_plot(
    grouped_vote_data,
    ['Droite_2017', 'Droite_2022'],
    'Trends in Right-wing Voting',
    ['green', 'lightgreen'],
    'right_wing_voting_trends_readable.png'
)

print(left_wing_path, center_path, right_wing_path)
