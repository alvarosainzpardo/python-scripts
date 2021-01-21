#!/usr/bin/env python

from getopt import getopt, GetoptError
import sys
from os.path import basename
import string
import random

# Global variables for command line options
PASSWORD_NUMBER = 1
UPPERCASE_NCHARS = 3
LOWERCASE_NCHARS = 3
DIGIT_NCHARS = 3
SYMBOL_NCHARS = 1

def usage():
  """
  Prints usage

  """
  print(f'{basename(sys.argv[0])}, random password generator')
  print(f'Usage: {basename(sys.argv[0])} [OPTION]...')
  print('')
  print('Mandatory arguments to long options are mandatory for short options too.')
  print('')
  print('Options:')
  print('-h,  --help      print this help')
  print('-n <number>      number of passwords to generate')
  print('-u <number>      number of uppercase chars in password')
  print('-d <number>      number of digits in password')
  print('-l <number>      number of lowercase char in password')

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

def generate_password(uppercase_chars, lowercase_chars, digit_chars, symbol_chars):
  uppercase_random_chars = ''.join(random.choices(string.ascii_uppercase, k=uppercase_chars))
  lowercase_random_chars = ''.join(random.choices(string.ascii_lowercase, k=lowercase_chars))
  digit_random_chars = ''.join(random.choices(string.digits, k=digit_chars))
  symbol_random_chars = ''.join(random.choices('@%+\\/\'!#$^?:,(){}[]~-_.', k=symbol_chars))
  return uppercase_random_chars + digit_random_chars + lowercase_random_chars + symbol_random_chars

def main():
  global PASSWORD_NUMBER
  global UPPERCASE_NCHARS
  global LOWERCASE_NCHARS
  global DIGIT_NCHARS
  global SYMBOL_NCHARS

  try:
      opts, args = getopt(sys.argv[1:], 'hu:l:d:s:n:', ['help'])
  except GetoptError as e:
    usage_and_exit(str(e), 1)
  
  for op, val in opts:
    if op in ['-h', '--help']:
      usage_and_exit()
    elif op in ['-n']:
      try:
        PASSWORD_NUMBER = int(val)
      except Exception as e:
        usage_and_exit(str(e), 1)
    elif op in ['-u']:
      try:
        UPPERCASE_NCHARS = int(val)
      except Exception as e:
        usage_and_exit(str(e), 1)
    elif op in ['-l']:
      try:
        LOWERCASE_NCHARS = int(val)
      except Exception as e:
        usage_and_exit(str(e), 1)
    elif op in ['-d']:
      try:
        DIGIT_NCHARS = int(val)
      except Exception as e:
        usage_and_exit(str(e), 1)
    elif op in ['-s']:
      try:
        SYMBOL_NCHARS = int(val)
      except Exception as e:
        usage_and_exit(str(e), 1)
    else:
      usage_and_exit('Incorrect option', 1)

  for i in range(int(PASSWORD_NUMBER)):
    print(generate_password(UPPERCASE_NCHARS, LOWERCASE_NCHARS, DIGIT_NCHARS, SYMBOL_NCHARS))
  exit(0)

if __name__ == '__main__':
  main()
