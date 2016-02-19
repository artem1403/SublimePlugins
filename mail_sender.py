# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import smtplib
from email.mime.text import MIMEText



class MailSenderCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		toaddr = ['Мудряк Артем Геннадьевич <mudryak_ag@magnit.ru>'] #кому высылаем
		me = 'Мудряк Артем Геннадьевич <mudryak_ag@magnit.ru>' # кто по факту отправляет 
		subject = 'Auto mail sender.'

		if self.view.file_name() != None:
			subject += ' File: "' + self.view.file_name() + '"'

		server      = 'mail.tander.ru' # Сервер отправитель
		port        = 25
		user_name   = ''     # Адрес отправителя
		user_passwd = ''  # Пароль отправителя

		# Формируем заголовок письма
		mailText = self.view.substr(self.view.sel()[0])
		mailText = mailText.encode('utf-8')

		msg = MIMEText(mailText, "", "utf-8")
		msg['Subject'] = subject # Тема письма
		msg['From'] = me # Надпись, от кого будет отражаться письмо во входящих
		msg['To'] =  '; '.join([ toaddr[0] ]) # # Надпись, кто будет отражаться в получателях
		# msg['cc'] = ', '.join([ toaddr[0] ]) # отправка копии 1-му адресату



		# part2 = MIMEText('Содержимое приложенного файла', 'text/html;name="tasks.htm"', 'utf-8')
		# msg.attach(part2)

		try:
			# Подключение
			s = smtplib.SMTP(server, port)
			s.ehlo()
			s.starttls()
			s.ehlo()
			# Авторизация
			s.login(user_name, user_passwd)
			# Отправка пиьма
			s.sendmail(me, toaddr, msg.as_string())
			s.quit() 
		except:
			sublime.status_message('Problem! Mail was not sent.')
		else:
			sublime.status_message('Success send!')






