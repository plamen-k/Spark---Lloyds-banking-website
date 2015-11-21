# taken from https://stackoverflow.com/questions/4386168/how-to-concatenate-strings-in-django-templates

from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
	"""concatenate arg1 & arg2"""
	return str(arg1) + str(arg2)