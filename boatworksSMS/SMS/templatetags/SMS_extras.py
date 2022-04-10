from django import template
from SMS.models import Parent
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.simple_tag
def get_name_from_number(number):
    #need to handle what happens when a number not in the database texts.
    #that could break everything
    if number != settings.TWILIO_NUMBER:
        minus_1 = number[2:]
        area_code = minus_1[0:3]
        part_one = minus_1[3:6]
        part_two = minus_1[6:]
        number_list = [area_code, part_one, part_two]
        formatted_number = "-".join(number_list)
        try:
            parent = Parent.objects.get(cell_phone=formatted_number)
            if parent.last_name and parent.first_name:
                return parent.last_name + ", " + parent.first_name
            else:
                return "Parent of " + parent.student.last_name + ", " + parent.student.first_name
        except ObjectDoesNotExist:
            return "Unknown Number"
    else:
        return "BoatworksSMS"