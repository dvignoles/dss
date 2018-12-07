#snc_template_tags
#template tags etc

from django import template

register = template.Library()


@register.filter
def imgsrc(user):
	return 'img/{}.png'.format(user.prof_pic_num)