# TODO: delete lines after read, \r


import requests
def define(a, b='usd'):
	p = str(requests.get(f'https://www.google.com/search?client=opera-gx&q={a}+to+{b}').content)
	i = p.find('United States Dollar')  # only works when convert TO usd
	s = p[i - 10: i]
	return float(s[[i for i, a in enumerate(s[:-1]) if not (a.isdigit() or a == '.')][-1] + 1:])
def convert(n): return round(func(n, amt), 2)
unit = input('> which unit would you like to translate to?\n').strip()
amt = define(unit)
func = lambda a, b: a * b
while 1:
	n = input()
	if n in ('', 'exit', 'exit()'): exit()
	if n == 'switch':
		print(f'>a) {unit} -> USD\n>b) USD -> {unit}')
		choice = input()[0]
		msg = f'switching to choice {choice}'
		if choice == 'a': func = lambda a, b: a * b
		elif choice == 'b': func = lambda a, b: a / b
		else: msg = f'{choice} is not a valid option'
	else:
		try: msg = convert(float(n))
		except Exception: msg = f'"{n}" is not a valid input'
	print(f'> {msg}')