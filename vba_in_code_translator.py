import sublime, sublime_plugin


class VbaInCodeTranslatorCommand(sublime_plugin.TextCommand):
	VALUE_NAME         = 'Zapros'
	MAX_ROW_IN_BLOCK   = 12
	MAX_RIGHT_INDENT   = 80
	LEFT_INSIDE_INDENT = 4

	def run(self, edit):

		s = self.view.sel()[0]
		result = self.view.substr(s)
		result = result.replace('"', '""')
		result = result.split('\n')

		i = 0

		max_indent   = len(self.VALUE_NAME)*2 + 3 + 3
		first_indent = len(self.VALUE_NAME) + 3

		for element in result:
			element = element.ljust(self.MAX_RIGHT_INDENT-self.LEFT_INSIDE_INDENT)
			if i == 0:
				result[i] = ' '*first_indent + \
				self.VALUE_NAME + \
				' = "' + ' '*self.LEFT_INSIDE_INDENT + \
				element + \
				'" & vbnewline & _ \n'

			elif (i != 0) & (i % self.MAX_ROW_IN_BLOCK == 0):
				result[i] = self.VALUE_NAME + \
				' = ' + \
				self.VALUE_NAME + \
				' & "' + ' '*self.LEFT_INSIDE_INDENT +\
				element + \
				'" & vbnewline & _ \n'
				result[i-1] = result[i-1][:-5] + '\n'

			else:
				result[i] = ' '*max_indent + \
				'"' + ' '*self.LEFT_INSIDE_INDENT +\
				element + \
				'" & vbnewline & _ \n'

			i = i + 1

		res = ''.join(result)
		res = res[:-18]
		self.view.replace(edit, s, res)


class VbaOutCodeTranslatorCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		s = self.view.sel()[0]
		result = self.view.substr(s)
		result = result.split('\n')

		i = 0
		for element in result:
			result[i] = element[element.find('"') + 1:element.rfind('"')] \
			.rstrip() + '\n'

			if (result[i][:4] == ' '*4):
				result[i]=result[i][4:]

			i = i + 1

		res = ''.join(result)
		res = res.replace('""', '"')
		self.view.replace(edit, s, res)


