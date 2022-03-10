from bs4 import BeautifulSoup
import requests 
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '6dfd8982a82a48169560ecef000624bb'
PSWD ='6aa927a814a6405ea8a085c158316a74'
# SCOPE= 'playlist-modify-private'

date = input('Please enter date of your choice in YYYY-MM-DD format')
response = requests.get(f'https://www.billboard.com/charts/hot-100')
soup = BeautifulSoup(response.text ,'html.parser')

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope ='playlist-modify-private', 
        redirect_uri="https://example.com",
        client_id = CLIENT_ID ,
        client_secret = PSWD ,
        show_dialog = True,
        cache_path="token.txt")
        )
user_id = sp.current_user()["id"]

songs_list = [s.get_text()  for s in soup.find_all(name='span' , class_ = 'chart-element__information__song text--truncate color--primary')]
year = date.split('-')[0]
print(year)
# print(songs_list)
songs_uri =[]
for song in songs_list[:10]:
    print(song)
    res = sp.search(q=f'track:{song} year:{year}' , type ='track')
    try:
        print(res['tracks']['items'][0]['uri'])
        songs_uri.append(res['tracks']['items'][0]['uri'])
    except:
        print(f"Song {song}not found")

play_list = sp.user_playlist_create(user_id,name = 'Test101', description = 'Test Playlist of top 100' , public = False )
play_list_id = play_list['id']
# print(play_list)
# print(songs_uri)
s = sp.user_playlist_add_tracks(user_id,play_list_id,songs_uri)