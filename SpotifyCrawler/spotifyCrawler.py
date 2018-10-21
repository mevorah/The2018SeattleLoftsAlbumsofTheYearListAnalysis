import argparse
from spotify import Spotify
from spotify import Extractor
import itertools
import csv

def print_csv(dictionary):
	keys = dictionary.keys()
	keys.sort()
	values = []
	for key in keys:
		values.append(str(dictionary[key]))
	comma_separated_values = ",".join(values)
	print(comma_separated_values)

def build_album_data(artist, album, album_info, track_names, track_data):
	'''
	Returns merged list of tracks with data replicated from common input.
	'''
	track_index = 0
	for track_name, track_datum in itertools.izip(track_names, track_data):
		# merge everything into track data
		track_datum['artist'] = artist
		track_datum['album'] = album
		track_datum['track_name'] = track_name
		track_datum['release_date'] = album_info['release_date']
		track_datum['genres'] = ",".join(album_info['genres'])
		track_datum['label'] = album_info['label']
		track_datum['total_tracks'] = album_info['total_tracks']
		track_datum['track_number'] = track_index
		track_index += 1
	return track_data

def get_album_data(artist, album):
	'''
	Fetches album data for artist and album. Returns a matrix in the following
	format:
	[artist],[album],[track name],[feature 1],[feature 2],...
	'''
	print("Artist:" + artist + " Album:" + album)
	album_id = spotify.get_album_id(artist, album)
	album_data = spotify.get_album(album_id)
	album_info = extractor.get_album_info(album_data)
	track_names = extractor.get_track_names(album_data)
	track_ids = extractor.get_track_ids(album_data)
	track_data = spotify.get_track_data(track_ids)
	album_and_track_data = build_album_data(artist, album, album_info, track_names, track_data)
	return album_and_track_data

parser = argparse.ArgumentParser(description='Fetches an album from spotify and transforms its data into a 1-dimension matrix.')
parser.add_argument('--api-key', help='(Required) Spotify API key:\https://developer.spotify.com/console/get-album-tracks/')
parser.add_argument('--artist', help='Artist name')
parser.add_argument('--album', help='Album name')
parser.add_argument('--input', help='Input file name in format [album] [artist]')
parser.add_argument('--output', help='Output filename')

args = parser.parse_args()
api_key = args.api_key
artist_name = args.artist
album_name = args.album
input_file_name = args.input
output_file_name = args.output

if api_key == None:
	print("Get the api-key from:")
	print("https://accounts.spotify.com/authorize?client_id=500403bfc1ab4026a50f88bb0366066e&redirect_uri=https://seattlelofts.design/callback&scope=user-read-private%20user-read-email&response_type=token&state=123")
	exit();

spotify = Spotify(api_key)
extractor = Extractor()

if input_file_name:
	input_csv = csv.reader(open(input_file_name))
	for row in input_csv:
		print("Reading file")
elif artist_name and album_name: 
	album_data = get_album_data(artist_name, album_name)
	for track in album_data:
		print_csv(track)
else:
	print("[Problem] No input file or artist/album specified. You must choose one. Input file takes priority if both are specified.")
