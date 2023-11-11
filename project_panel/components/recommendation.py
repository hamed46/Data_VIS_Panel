from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from components.dataread import read_csv


class MusicRecommender:
    def __init__(self, dataset_path):
        self.music_df = read_csv(dataset_path)
        self.music_features = self.music_df[['danceability', 'energy', 'key',
                                             'loudness', 'mode', 'speechiness', 'acousticness',
                                             'instrumentalness', 'liveness', 'valence', 'tempo']].values
        self.scaler = MinMaxScaler()
        self.music_features_scaled = self.scaler.fit_transform(self.music_features)

    def content_based_recommendations(self, input_song_name, num_recommendations=5):
        if input_song_name not in self.music_df['track_name'].values:
            print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
            return None

        input_song_index = self.music_df[self.music_df['track_name'] == input_song_name].index[0]
        similarity_scores = cosine_similarity([self.music_features_scaled[input_song_index]], self.music_features_scaled)
        similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]
        return self.music_df.iloc[similar_song_indices][['track_name', 'artists', 'album_name', 'popularity']]

    def hybrid_recommendations(self, input_song_name, num_recommendations=5, alpha=0.5):
        if input_song_name not in self.music_df['track_name'].values:
            print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
            return None

        content_based_rec = self.content_based_recommendations(input_song_name, num_recommendations)
        popularity_score = self.music_df.loc[self.music_df['track_name'] == input_song_name, 'popularity'].values[0]
        weighted_popularity_score = popularity_score

        hybrid_rec = content_based_rec.copy()
        hybrid_rec = hybrid_rec.append({
            'track_name': input_song_name,
            'artists': self.music_df.loc[self.music_df['track_name'] == input_song_name, 'artists'].values[0],
            'album_name': self.music_df.loc[self.music_df['track_name'] == input_song_name, 'album_name'].values[0],
            'popularity': weighted_popularity_score
        }, ignore_index=True)

        hybrid_rec = hybrid_rec.sort_values(by='popularity', ascending=False)
        hybrid_rec = hybrid_rec[hybrid_rec['track_name'] != input_song_name]

        return hybrid_rec

