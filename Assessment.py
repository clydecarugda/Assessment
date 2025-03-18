import pandas as pd, json
from collections import defaultdict
from datetime import datetime

def LoadMoviesData(file_path):
  try:
    data = pd.read_csv(file_path)
    
    # Convert columns
    data = data.astype({'rank': 'int', 'year': 'int', 'imbd_votes': 'int', 'duration': 'int', 'imdb_rating': 'float'})
    
    # Add necessary columns
    if not 'extra_genres' in data.columns:
      data['extra_genres'] =[[] for _ in range(len(data))]
      
    if not 'rating_percentage' in data.columns:
      data['rating_percentage'] = None
  
    if not 'popularity_score' in data.columns:
      data['popularity_score'] = None
      
    if not 'duration_hours' in data.columns:
      data['duration_hours'] = None
      
    if not 'release_date' in data.columns:
      data['release_date'] = None
      
    if not 'reception' in data.columns:
      data['reception'] = [[] for _ in range(len(data))]
    
    # Create Array Fields
    data['cast_id'] = data['cast_id'].str.split(',')
    data['cast_name'] = data['cast_name'].str.split(',')
    data['writter_name'] = data['writter_name'].str.split(',')
    data['writter_id'] = data['writter_id'].str.split(',')
    
    data['cast'] = data.apply(lambda row: [{'id' : a, 'name' : b} for a, b in zip(row['cast_id'], row['cast_name'])], axis=1)
    data['writers'] = data.apply(lambda row: [{'id' : a, 'name' : b, 'valid' : False} for b, a in zip(row['writter_name'], row['writter_id'])], axis=1)
    data['director'] = data.apply(lambda row: {'id' : row['director_id'], 'name' : row['director_name']}, axis=1)

    return data
  
  except Exception as e:
    print(f'Error: {e}')
    exit
    
def ValidateWriter(writer_list, writers_json_data):
  for writer in writer_list:
    writer_id = writer['id']
    writer_name = writer['name']
    
    if writers_json_data.get(writer_id) == writer_name:
      writer['valid'] = True
      
  return writer_list

def EnrichDataGenre(data, genre_path, writters_path):    
  # Genre
  with open(genre_path, 'r') as genre_file:
    genre_json_data = json.load(genre_file)
    
    genre_list_dict = defaultdict(list)
    
    for genre, movie_title in genre_json_data.items():
      for movie_id in movie_title.keys():
        genre_list_dict[movie_id].append(genre)
        
  # Writters
  with open(writters_path, 'r') as writters_file:
    writters_json_data = json.load(writters_file)
  
  # Add extra_genres and validate writer
  for a, row in data.iterrows():
    # extra_genres
    m_id = row['id']
    data.at[a, 'extra_genres'] = genre_list_dict.get(m_id)
    
    # Writer
    data['writers'] = data['writers'].apply(lambda x: ValidateWriter(x, writters_json_data))
    
  return data

def DetermineCategory(rating_difference):
  if rating_difference > 0.5:
    return 'Above Average'
  elif rating_difference < -0.5:
    return 'Below Average'
  else:
    return 'Average'
    
def CalculateFields(data):
  year_average_rating_dict = data.groupby('year')['imdb_rating'].mean().to_dict()
  
  for a, row in data.iterrows():
    imdb_rating = row['imdb_rating']
    imbd_votes = row['imbd_votes']
    duration = row['duration']
    year = row['year']
    year_average_rating = year_average_rating_dict.get(year)
    
    # Calculate Rating Pecentage
    data.at[a, 'rating_percentage'] = round(imdb_rating * 10, 2)
    # Calculate Popularity Score
    data.at[a, 'popularity_score'] = round((imdb_rating * imbd_votes) / 1000.0, 2)
    # Convert duration to hours
    data.at[a, 'duration_hours'] = round(duration / 60, 2)
    # Format Release Date
    data.at[a, 'release_date'] = datetime(year, 1, 1).strftime('%Y-%m-%d')
    # Add reception data
    reception_rating_difference = imdb_rating - year_average_rating
    reception_category = DetermineCategory(reception_rating_difference)
    data.at[a, 'reception'] = {'year_average_rating': round(year_average_rating, 2), 'rating_difference': round(reception_rating_difference, 2), 'category': reception_category}
    
  return data

# Main --------------------------
# File Paths
movies_data_path = 'movies.csv'
genre_data_path = 'datasets/genre.json'
writters_data_path = 'datasets/writters.json'

movies_data = LoadMoviesData(movies_data_path)
movies_data = EnrichDataGenre(movies_data, genre_data_path, writters_data_path)
movies_data = CalculateFields(movies_data)

# Drop unnecessary columns & Rearranged columns
data_column_order = ['rank', 'id', 'name', 'year', 'imbd_votes', 'imdb_rating', 'certificate',
                     'duration', 'genre', 'img_link', 'cast', 'director', 'writers', 'extra_genres',
                     'rating_percentage', 'popularity_score', 'duration_hours', 'release_date', 
                     'reception']

movies_data = movies_data.drop(['cast_id', 'cast_name', 
                                'director_id', 'director_name', 
                                'writter_name', 'writter_id'], axis=1)

movies_data = movies_data[data_column_order]

# Export Data
movies_data_json = json.loads(movies_data.to_json(orient='records'))

with open('Output/movies_output.json', 'w') as f:
  json.dump(movies_data_json, f, indent=2, separators=(',', ': '))