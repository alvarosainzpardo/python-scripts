#!/usr/bin/env python

from getopt import getopt, GetoptError
import requests
import re
import sys
from os.path import basename

ALBUM_ARTIST = ''
ALBUM_TITLE = ''
NO_CD_NUMBER = False

def usage():
  """
  Prints usage

  """
  print('discogs.py, retrieve information about Discogs resources')
  print(f'Usage: {basename(sys.argv[0])} [OPTION]... [RESOURCE_ID]...')
  print('')
  print('Mandatory arguments to long options are mandatory for short options too.')
  print('')
  print('Options:')
  print('-h,  --help                    print this help')
  print('-A,  --album-artist=ARTIST(S)  override album artist(s)')
  print('-T,  --album-title=TITLE  override album title')
  print('-n,  --no-cd-number            in multi cd albums, don\'t print cd number')

def usage_and_exit(msg='', exit_code=0):
  """
  Print usage message and exit"
  :param msg: optional error message to print
  :param exit_code: optional program exit code
  """

  if msg != '':
    print('Error: ' + msg)
    print()

  usage()
  sys.exit(exit_code)


def print_metadata(resource_id):
  response = requests.get(f"https://api.discogs.com/releases/{resource_id}")
  if response.ok:
    response = response.json()
    album_artists = ALBUM_ARTIST if ALBUM_ARTIST else ', '.join([x['name'] for x in response['artists']])
    album_title = ALBUM_TITLE if ALBUM_TITLE else response['title']
    for track in response['tracklist']:
      m = re.match('(\d*)-(\d*)', track['position'])
      if NO_CD_NUMBER and m:
        tracknum = m.group(2)
      else:
        tracknum = track['position']
      track_artists = ', '.join([x['name'] for x in track['artists']]) if 'artists' in track else album_artists
      print(f"{tracknum}; {track_artists}; {track['title']}; {album_artists}; {album_title}; {response['year']}")
    return True
  else:
    print('Error: resource id invalid or not found')
    return False

def main():
  global ALBUM_ARTIST
  global ALBUM_TITLE
  global NO_CD_NUMBER

  try:
    opts, args = getopt(sys.argv[1:], 'hnA:T:', ['help', 'no-cd-number', 'album-artist=', 'album-title='])
  except GetoptError as err:
    usage_and_exit(str(err), 1)
  
  for op, val in opts:
    if op in ['-h', '--help']:
      usage_and_exit()
    elif op in ['-n', '--no-cd-number']:
      NO_CD_NUMBER = True
    elif op in ['-A', '--album-artist']:
      ALBUM_ARTIST = val
    elif op in ['-T', '--album-title']:
      ALBUM_TITLE = val
    else:
      usage_and_exit('', 1)

  if not len(args) > 0:
    usage_and_exit('resource id arg missing', 1)

  for arg in args:
    print_metadata(arg)
  exit(0)

if __name__ == '__main__':
  main()
