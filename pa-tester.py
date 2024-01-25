#!/usr/bin/env python3

import sys
import re

def main():
	""" This script reads a text from standard input,
	analyzes the validity of a password in each line,
	if valid assesses the strength of the password,
	and writes results of the password analysis into
	the standard output  """

	# if arguments provided, show error message
	if len(sys.argv) != 1:
		print("No arguments should be provided.")
		print("Usage: %s" % sys.argv[0])
		return 1;
	
	
	lines = sys.stdin
	
	for pw in lines:
		pw = pw.strip()

		# FIRST CHECK VALIDITY
		if not length_valid(pw) or not ascii_valid(pw):
			# NOT VALID :(
			strength = 0
			if not length_valid(pw) and not ascii_valid(pw):
				print(f"{strength},INVALID,TOO_SHORT,NONASCII")
			elif not length_valid(pw):
				print(f"{strength},INVALID,TOO_SHORT")
			else:
				print(f"{strength},INVALID,NONASCII")
		else:
			# PASSWORD IS VALID!
			strength = 1
			result = ""
			if has_uppercase(pw):
				strength += 1
				result += ",UPPERCASE"
			if has_lowercase(pw):
				strength += 1
				result += ",LOWERCASE"
			if has_number(pw):
				strength += 1
				result += ",NUMBER"
			if has_special(pw):
				strength += 1
				result += ",SPECIAL"
			if has_sequence(pw):
				strength -= 1
				result += ",sequence"

			strengthreport = strength_report(strength)

			print(f"{strength},{strengthreport}{result}")

	return 0


# ATTRIBUTE CHECKS

def length_valid(password):
    return bool(re.match(r'^.{8,}$', password))

def ascii_valid(password):
	return bool(re.match(r'^[\x00-\x7F]+$', password))

def has_uppercase(password):
	return bool(re.search(r'[A-Z]', password))

def has_lowercase(password):
	return bool(re.search(r'[a-z]', password))

def has_number(password):
	return bool(re.search(r'\d', password))

def has_special(password):
    special_characters = r'[!#$%&()*+,\-./:;<=>?@[\]^_`{|}~]'
    return bool(re.search(special_characters, password))

def has_sequence(password):
    # Define a regular expression to check for three consecutive repeated characters
    sequence_pattern = re.compile(r'(.)\1\1')
    return bool(sequence_pattern.search(password))

def strength_report(strength):
	if strength <= 1:
		return "VERY_WEAK"
	if strength == 2:
		return "WEAK"
	if strength == 3:
		return "MEDIUM"
	if strength == 4:
		return "STRONG"
	else:
		return "VERY_STRONG"

if __name__ == "__main__":
	main()
