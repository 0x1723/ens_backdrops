import math
import sha3
from flask import Flask
# 29854512495791625746775787986622618014961884325760779223777139961252634542538
# 8041138228694525761558183838270953836344146325640581694807278233190101011603

app = Flask(__name__)

S=1000
# Assumptions:
# name doesn't have more than 256 characters

digit_colors = ["white", "red", "orange", "yellow", "green", "blue", "indigo", "violet", "grey", "black"]
vowels = ["a", "e", "i", "o", "u", "y"]
consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z"]
alphabet = [""] + vowels + consonants
alphabet = sorted(alphabet)
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
alphanumerics = [""] + vowels + consonants + digits
alphanumerics = sorted(alphanumerics)

scrabblemeter_dict = {
	"a": 1,
	"b": 3,
	"c": 3,
	"d": 2,
	"e": 1,
	"f": 4,
	"g": 2,
	"h": 4,
	"i": 1,
	"j": 8,
	"k": 5,
	"l": 1,
	"m": 3,
	"n": 1,
	"o": 1,
	"p": 3,
	"q": 10,
	"r": 1,
	"s": 1,
	"t": 1,
	"u": 1,
	"v": 4,
	"w": 4,
	"x": 8,
	"y": 4,
	"z": 10
}

def get_h_accent(h, factor=180):
	if 0 <= h <= 360:
		if h+factor <= 360:
			return h+factor
		else:
			return h-factor
	else:
		raise("Value of H must be between 0 and 360")

def hsl_to_rgb(hsl):
	c = (1 - abs((2*hsl["l"]) - 1)) * hsl["s"]
	x = c * (1 - abs(((hsl["h"]/60) % 2) - 1))
	m = hsl["l"] - c/2
	temp_rgb = {}
	rgb = {}
	if 0 <= hsl["h"] < 60:
		temp_rgb["r"] = c
		temp_rgb["g"] = x
		temp_rgb["b"] = 0
	elif 60 <= hsl["h"] < 120:
		temp_rgb["r"] = x
		temp_rgb["g"] = c
		temp_rgb["b"] = 0
	elif 120 <= hsl["h"] < 180:
		temp_rgb["r"] = 0
		temp_rgb["g"] = c
		temp_rgb["b"] = x
	elif 180 <= hsl["h"] < 240:
		temp_rgb["r"] = 0
		temp_rgb["g"] = x
		temp_rgb["b"] = c
	elif 240 <= hsl["h"] < 300:
		temp_rgb["r"] = x
		temp_rgb["g"] = 0
		temp_rgb["b"] = c
	elif 300 <= hsl["h"] <= 360:
		temp_rgb["r"] = c
		temp_rgb["g"] = 0
		temp_rgb["b"] = x
	else:
		raise("Value of H must be between 0 and 360")
	rgb["r"] = (temp_rgb["r"] + m) * 255
	rgb["g"] = (temp_rgb["g"] + m) * 255
	rgb["b"] = (temp_rgb["b"] + m) * 255
	return rgb

def get_ens_name_id(name):
	k = sha3.keccak_256()
	name_bytes = name.encode('ascii') 
	k.update(name_bytes)
	ens_name_id = int(k.hexdigest(), 16)
	return ens_name_id

def draw_background(name, main_color):
	return f'<rect fill="rgb({main_color["r"]},{main_color["g"]},{main_color["b"]})" height="{S}" width="{S}" x="0" y="0" />'

def draw_signature_background(name, main_color):
	ens_name_id = get_ens_name_id(name)
	bg_length = len(str(ens_name_id))*10 + 20
	bg_x = (S - bg_length) / 2
	bg_y = (S / len(name)) - 20
	return f'<rect fill="rgb({main_color["r"]},{main_color["g"]},{main_color["b"]})" height="50" width="{bg_length}" x="{bg_x}" y="{bg_y}" />'

def draw_shapes(name, accent_color):
	shapes = ''
	vowel_count = 0
	for letter in name:
		if letter in vowels:
			vowel_count += 1
	side_length = S / len(name)
	stroke_width = side_length / 40
	if vowel_count == 0:
		scrabblemeter_score = 0
		for letter in name:
			if letter.isalpha():
				scrabblemeter_score += scrabblemeter_dict[letter]
		scrabblemeter_score = round(scrabblemeter_score / len(name), 2)
		for i in range(len(name)):
			cx = (i*side_length + (i+1)*side_length)/2
			for j in range(len(name)):
				cy = (j*side_length + (j+1)*side_length)/2
				shapes += f'<circle cx="{cx}" cy="{cy}" fill="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" r="{stroke_width*scrabblemeter_score}" />'
	elif vowel_count == 1:
		for i in range(len(name)):
			cx = (i*side_length + (i+1)*side_length)/2
			for j in range(len(name)):
				cy = (j*side_length + (j+1)*side_length)/2
				shapes += f'<circle cx="{cx}" cy="{cy}" fill="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" r="{stroke_width}" />'
				shapes += f'<circle cx="{cx}" cy="{cy}" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" fill="transparent" r="{side_length/4}" stroke-width="{stroke_width}"/>'
	elif vowel_count == 2:
		for i in range(len(name)):
			cx = (i*side_length + (i+1)*side_length)/2
			for j in range(len(name)):
				cy = (j*side_length + (j+1)*side_length)/2
				shapes += f'<circle cx="{cx}" cy="{cy}" fill="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" r="{stroke_width}" />'
				shapes += f'<polyline points="{cx - side_length/4} {cy} {cx} {cy + side_length/4} {cx + side_length/4} {cy}" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" fill="transparent" stroke-width="5"/>'
	elif vowel_count == 3:
		# https://byjus.com/centroid-formula/
		a = side_length/4
		c = a/math.sqrt(3)
		b = (4*a)/math.sqrt(3)
		for i in range(len(name)):
			cx = (i*side_length + (i+1)*side_length)/2
			for j in range(len(name)):
				cy = (j*side_length + (j+1)*side_length)/2
				shapes += f'<circle cx="{cx}" cy="{cy}" fill="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" r="{stroke_width}" />'
				shapes += f'<polygon points="{cx} {cy-a} {cx-a} {cy+c} {cx+a} {cy+c}" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" fill="transparent" stroke-width="{stroke_width}"/>'
	elif vowel_count == 4:
		for i in range(len(name)):
			cx = (i*side_length + (i+1)*side_length)/2
			for j in range(len(name)):
				cy = (j*side_length + (j+1)*side_length)/2
				shapes += f'<circle cx="{cx}" cy="{cy}" fill="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" r="{stroke_width}" />'
				shapes += f'<rect x="{cx-side_length/4}" y="{cy-side_length/4}" width="{side_length/2}" height="{side_length/2}" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" fill="transparent" stroke-width="{stroke_width}"/>'
	elif vowel_count == 5:
		r = side_length / 4
		unit = r / 5
		for i in range(len(name)):
			cx = (i*side_length + (i+1)*side_length)/2
			for j in range(len(name)):
				cy = (j*side_length + (j+1)*side_length)/2
				shapes += f'<circle cx="{cx}" cy="{cy}" fill="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" r="{stroke_width}" />'
				shapes += f'<polygon points="{cx} {cy-r-unit} {cx+r+unit} {cy-unit} {cx+r-unit} {cy+r} {cx-r+unit} {cy+r} {cx-r-unit} {cy-unit}" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" fill="transparent" stroke-width="{stroke_width}"/>'
	else:
		r = side_length / 4
		unit = r / 2
		for i in range(len(name)):
			cx = (i*side_length + (i+1)*side_length)/2
			for j in range(len(name)):
				cy = (j*side_length + (j+1)*side_length)/2
				shapes += f'<circle cx="{cx}" cy="{cy}" fill="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" r="{stroke_width}" />'
				shapes += f'<polygon points="{cx-unit} {cy-r} {cx+unit} {cy-r} {cx+r} {cy} {cx+unit} {cy+r} {cx-unit} {cy+r} {cx-r} {cy}" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" fill="transparent" stroke-width="{stroke_width}"/>'
	return shapes

def draw_barcode(name, accent_color):
	barcode = ""
	ens_name_id = get_ens_name_id(name)
	count = (S - len(str(ens_name_id))*10) / 2
	barcode_y = (S / len(name)) - 10
	for digit in str(ens_name_id):
		barcode += f'<rect x="{count}" y="{barcode_y}" width="10" height="10" fill="{digit_colors[int(digit)]}" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" stroke-width="1"/>'
		count += 10
	return barcode

def draw_scrabblemeter(name, main_color, accent_color):
	scrabblemeter_score = 0
	ens_name_id = get_ens_name_id(name)
	for char in name:
		if char.isalpha():
			scrabblemeter_score += scrabblemeter_dict[char]
	scrabblemeter_score = round(scrabblemeter_score / len(name), 2)
	bar_length = len(str(ens_name_id))*10
	bar_x = (S - bar_length) / 2
	bar_y = (S / len(name)) + 10
	scrabblemeter_svg = f'<rect x="{bar_x}" y="{bar_y}" width="{bar_length}" height="10" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" fill="rgb({main_color["r"]},{main_color["g"]},{main_color["b"]})" stroke-width="1"/>'
	scrabblemeter_svg += f'<rect x="{bar_x}" y="{bar_y}" width="{scrabblemeter_score * len(str(ens_name_id))}" height="10" stroke="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" fill="rgb({accent_color["r"]},{accent_color["g"]},{accent_color["b"]})" stroke-width="1"/>'
	return scrabblemeter_svg

@app.route("/<name>")
def drawsvg(name):
	name = name.lower()
	main_color = {}
	accent_color = {}

	cap = 36
	min_sat = 0.5
	hue_cap = 360
	hue_count_max = 4

	vowel_count = 0
	for letter in name:
		if letter in vowels:
			vowel_count += 1

	saturation = min_sat + ((alphanumerics.index(name[1]) / cap) * min_sat)
	lightness = 0.3 + ((alphanumerics.index(name[2]) / cap) * 0.4)

	main_color["h"] = int((hue_cap/(len(alphanumerics)-1))*alphanumerics.index(name[0]))
	main_color["s"] = saturation
	main_color["l"] = lightness

	if len(name) <= hue_count_max:
		accent_color["h"] = get_h_accent(main_color["h"], hue_cap/len(name))
	else:
		accent_color["h"] = get_h_accent(main_color["h"], hue_cap/hue_count_max)
	accent_color["s"] = saturation
	accent_color["l"] = lightness

	backdrop = '<?xml version="1.0" encoding="utf-8" ?>\n'
	backdrop += '<svg baseProfile="full" height="100%" version="1.1" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs />'
	backdrop += draw_background(name, hsl_to_rgb(main_color))
	backdrop += draw_shapes(name, hsl_to_rgb(accent_color))
	backdrop += draw_signature_background(name, hsl_to_rgb(main_color))
	backdrop += draw_barcode(name, hsl_to_rgb(accent_color))
	backdrop += draw_scrabblemeter(name, hsl_to_rgb(main_color), hsl_to_rgb(accent_color))
	backdrop += '</svg>'
	return(backdrop)


# svg_file = open("test.svg", "w")
# svg_file.write(backdrop)
# svg_file.close()
