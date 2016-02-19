# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re

class SqlBeautifier(sublime_plugin.TextCommand):
	IS_DEVELOPMENT = False #False #True

	def run(self, edit):
		s=self.view.sel()[0]
		result = self.view.substr(s)

		# каждое поле с новой строки, если оно не начинается с комментария
		result = re.sub('(?<!(--)),[ \t]*', '\n, ', result) 

		# левые переносы строк убираем
		result = re.sub('[ ]*\n{1,}[\t ]+', ' ', result) 
		result = re.sub('(?<=((SELECT)|(select)))[\n \t]+', '\n  ', result)
		result = re.sub('(\n){2,}', '\n', result)
		result = re.sub('(?<=((FROM)|(from)))[ \t]+', ' ', result)

		'''
		Заменить в исходном тексте
			, edit   - где заменить
			, s      - что заменить
			, result - на что заменить
		'''
		self.view.replace(edit, s, result)

		# Смена оформления внешнего вида на SQL
		self.view.set_syntax_file(u'Packages/SQL/SQL.tmLanguage') 

		if self.IS_DEVELOPMENT:
			parseSqlStr = result
			posSelect   = 0
			posFrom     = 0
			posWhere    = 0

			posSelect = parseSqlStr.upper().find('SELECT') # ищем слово select
			posFrom   = parseSqlStr.upper().find('FROM')   # ищем слово from
			posWhere  = parseSqlStr.upper().find('WHERE')  # ищем слово where

			if (posSelect!=-1 & posFrom!=-1):
				strBtwnSelectAndFrom = parseSqlStr[len('select'):posFrom]
				self.view.insert(edit, len(parseSqlStr), strBtwnSelectAndFrom)

			# self.view.insert(edit, 0, 'where - ' + str(posWhere) + '\n')
			# self.view.insert(edit, 0, 'from - ' + str(posFrom) + '\n')
			# self.view.insert(edit, 0, 'select - ' + str(posSelect) + '\n')





# S.upper()
# S.find(str, [start],[end])
# S[i:j:step]
# S.strip([chars]) #удаляет пробелы в строке слева и справа