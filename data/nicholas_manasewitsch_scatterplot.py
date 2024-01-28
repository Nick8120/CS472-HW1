import pandas as pd
import matplotlib.pyplot as plt

# Load CSV into a dataframe
df = pd.read_csv('authorsFileTouchesrootbeer.csv')

# set column names with the actual column names in CSV file
filename_column = 'Filename'
touches_column = 'Touches'
authors_column = 'Authors'

# Extract all authors and timestamps from the Authors column
df['Authors'] = df[authors_column].apply(lambda x: [tuple(map(str.strip, author.split('('))) for author in x.split('),')])
df = df.explode('Authors')
df[['Author', 'Timestamp']] = pd.DataFrame(df['Authors'].tolist(), index=df.index)

# Convert Timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.rstrip('Z)').str.replace('T', ' '), format='%Y-%m-%d %H:%M:%S')

# Calculate the span of weeks
df['Week'] = ((df['Timestamp'] - df['Timestamp'].min()) / pd.Timedelta('7D')).astype(int)

# Create scatterplot
plt.figure(figsize=(10, 6))

# Get a unique color for each author
unique_authors = df['Author'].unique()
color_map = {author: plt.cm.rainbow(i / len(unique_authors)) for i, author in enumerate(unique_authors)}

# Plot each author separately
for author in unique_authors:
    author_data = df[df['Author'] == author]
    color = color_map[author]
    plt.scatter(author_data[touches_column], author_data['Week'], label=author, color=color, alpha=0.5)

# Set plot labels and title
plt.xlabel('File Touches')
plt.ylabel('Week')
plt.title('File Touches Over Lifespan of scottyab/rootbeer Repository')

# Set axis limits and padding
plt.xlim(-1, 60)
plt.ylim(-10, 260)

# Adjust legend position to the right outside of the plot
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Show the plot
plt.show()