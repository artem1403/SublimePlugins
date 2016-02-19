# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re

class CodeAlignerCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		alignKey = self.view.substr(self.view.sel()[0])

		if (alignKey == ''):
			self.aligner(edit, ' as ')
		else:
			self.aligner(edit, alignKey)


	def aligner(self, edit, alignKey):
		result = self.view.substr(sublime.Region(0, self.view.size()))
		result = re.sub('\t', ' '*4, result) 
		result = result.split('\n')
		positions = [] 

		for element in result:
			positions.append(element.find(alignKey))

		maxPos = self.max_in_list(positions)

		i = 0
		for element in result:
			pos = element.find(alignKey)

			if (pos != -1):


				result[i] = result[i][:pos] + \
					''.ljust(maxPos - pos) + \
					result[i][pos:] 

			result[i] = result[i] + '\n'
			i += 1

		res = ''.join(result)
		self.view.erase(edit, sublime.Region(0, self.view.size()))
		self.view.insert(edit, 0, res)


	def max_in_list(self, lst):
		assert lst
		m = lst[0]
		for i in lst:
			if i > m:
				m = i
		return m
