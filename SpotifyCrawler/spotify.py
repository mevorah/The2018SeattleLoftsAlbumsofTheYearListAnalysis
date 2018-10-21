import requests
import simplejson as json

class Spotify(object):
	def __init__(self, api_key):
		self._api_key = api_key

	def _get_auth_header(self):
		return {'Authorization': "Bearer " + self._api_key}

	def _make_request(self, url, payload=None):
		auth = self._get_auth_header()
		response = requests.get(url, params=payload, headers=auth)

		if "200" not in str(response.status_code):
			print("[Problem] Request returned non-200 resonse. Url:" + url + " Payload:" + str(payload))
		
		if "502" in str(response.status_code):
			print("[Problem] Received a 502, retrying request.")
			response = requests.get(url, params=payload, headers=auth)

		response_json = json.loads(response.text)
		return response_json

	def get_album_id(self, artist, album):
		'''
		Performs a search given an artist and album
		name, and returns the best matched (if any)
		album id.
		'''
		url = 'https://api.spotify.com/v1/search'
		query = "album:" + album + " artist:" + artist
		payload = {'q': query, 'type': 'album', 'limit': 1}
		response = self._make_request(url, payload)

		if not response['albums']['items']:
			print "[NOT FOUND][album:" + album + " artist:" + artist + "]"
			return ""
		else:
			return response['albums']['items'][0]['id']

	def get_album(self, album_id):
		'''
		Fetches album data given an album id.
		'''
		url = "https://api.spotify.com/v1/albums/" + album_id
		response = self._make_request(url)
		return response

	def get_track_data(self, track_ids):
		'''
		Fetches track features for a list of track_ids. This
		function maintains the ordering of track_ids.
		'''
		url = "https://api.spotify.com/v1/audio-features"
		comma_separated_track_ids = ",".join(track_ids)
		payload = {'ids': comma_separated_track_ids}
		response = self._make_request(url, payload)
		track_data = [];
		for track in response['audio_features']:
			# remove spotify metadata attached and just
			# keep the features we care about
			del track['track_href']
			del track['analysis_url']
			del track['uri']
			del track['type']
			del track['id']
			track_data.append(track)
		return track_data

class Extractor(object):
	def __init__(self):
		return

	def get_track_ids(self, album):
		track_ids = []
		for track in album['tracks']['items']:
			track_ids.append(track['id'])
		return track_ids

	def get_track_names(self, album):
		track_names = []
		for track in album['tracks']['items']:
			track_names.append(track['name'])
		return track_names

	def get_album_info(self, album):
		album_info = {}
		album_info['release_date'] = album['release_date']
		album_info['genres'] = album['genres']
		album_info['label'] = album['label']
		album_info['total_tracks'] = album['total_tracks']
		return album_info


