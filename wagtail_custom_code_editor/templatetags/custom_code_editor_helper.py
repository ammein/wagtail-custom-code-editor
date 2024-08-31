from typing import Dict, List

from django import template
from django.utils.safestring import mark_safe
import json
import re

register = template.Library()


@register.simple_tag()
def tojson(value):
    return json.dumps(value)


def regexCamelToTitle():
    return r"""
            (            # start the group
                # alternative 1
            (?<=[a-z])  # current position is preceded by a lower char
                        # (positive lookbehind: does not consume any char)
            [A-Z]       # an upper char
                        #
            |   # or
                # alternative 2
            (?<!\A)     # current position is not at the beginning of the string
                        # (negative lookbehind: does not consume any char)
            [A-Z]       # an upper char
            (?=[a-z])   # matches if next char is a lower char
                        # lookahead assertion: does not consume any char
            )           # end the group
            """


@register.simple_tag()
def generate_options_lists(options: List[Dict]):
    html: str = ""
    category_options = {}

    # Sort the category
    for value_options in options:
        if category_options.get(value_options.get('category')) is None:
            category_options[value_options.get('category')] = [value_options]
        else:
            category_options[value_options.get('category')].append(value_options)

    # Loop Options
    for category in category_options:
        # Build Category
        category_label = re.sub(regexCamelToTitle(), r' \1', category.replace('-', ' '), flags=re.VERBOSE)
        html += f"""
                <li data-category='{category}' id='{category}' style='cursor:pointer;' data-header='{category}'>
                    <h1 class='category' class='uncollapse' style='text-transform:capitalize;'> {category_label.capitalize()} Options</h1>
                </li>    
                <ul data-header='{category}'>
                """
        for option in category_options[category]:
            options_html: str = ""
            help_html: str = ""
            label = re.sub(regexCamelToTitle(), r' \1', option.get('name').replace('-', ' '), flags=re.VERBOSE)
            if option.get('value') is not None and isinstance(option.get('value'), list):
                # Dropdown
                if isinstance(option.get('value'), list):
                    # Loop Options
                    for options_value in option.get('value'):
                        if isinstance(options_value, str):
                            options_html += f"<option value='{options_value}'>{options_value}</option>"
                        elif isinstance(options_value, object):
                            title, value = options_value.values()
                            options_html += f"<option value='{json.dumps(value) if isinstance(value, str) is False else value}'>{title}</option>"

                    if option.get('help') is not None:
                        help_html = f"<span style='font-size: 12px;font-style: italic; display:block;'>{option.get('help')}</span>"

                    html += f"""
                            <li id='{option.get('name')}' class='lists-inputs' data-custom-code-editor-target='optionList' data-category='{option.get('category').replace('-', ' ')}'>
                                <label for='{option.get('name')}'>{label.capitalize()} :</label>
                                <select name='{option.get('name')}' data-custom-code-editor-target='options' data-action='change->custom-code-editor#{'dropdownOnChange' if isinstance(option.get('value'), object) else 'dropdownObjectOnChange'}'>
                                    {options_html}
                                </select>
                                {help_html}
                            </li>
                            """
            # Slider
            elif option.get('type') == 'number':
                if option.get('help') is not None:
                    help_html = f"<span style='font-size: 12px;font-style: italic; display:block;'>{option.get('help')}</span>"

                if option.get('value') is not None:
                    html += f"""
                            <li id='{option.get('name')}' class='lists-inputs' data-custom-code-editor-target='optionList' data-category='{option.get('category').replace('-', ' ')}'>
                                <label for='{option.get('name')}'>{label.capitalize()} :</label>
                                <input name='{option.get('name')}' data-custom-code-editor-target='options' max='{option.get('value').get('max')}' min='{option.get('value').get('min')}' step='{option.get('value').get('step')}' type='range' class='range-slider__range' data-action='input->custom-code-editor#sliderOnChange blur->custom-code-editor#sliderOnFocusOut'>
                                <output class='range-slider__value' style='display:none;'></output>
                                {help_html}
                            </li>
                            """
                else:
                    html += f"""
                            <li id='{option.get('name')}' class='lists-inputs' data-custom-code-editor-target='optionList' data-category='{option.get('category').replace('-', ' ')}'>
                                <label for='{option.get('name')}'>{label.capitalize()} :</label>
                                <input name='{option.get('name')}' data-custom-code-editor-target='options' type='number' data-action='input->custom-code-editor#sliderOnChange' value='0'>
                                {help_html}
                            </li>
                            """

            elif option.get('type') == 'boolean':
                # Checkbox
                if option.get('help') is not None:
                    help_html = f"<span style='font-size: 12px;font-style: italic; display:block;'>{option.get('help')}</span>"

                html += f"""
                        <li id='{option.get('name')}' class='lists-inputs' data-custom-code-editor-target='optionList' data-category='{option.get('category').replace('-', ' ')}'>
                            <label for='{option.get('name')}'>{label.capitalize()} :</label>
                            <input name='{option.get('name')}' data-custom-code-editor-target='options' type='checkbox' class='error' data-action='custom-code-editor#checkboxOnChange'>
                            {help_html}
                        </li>
                        """
        html += "</ul>"

    return mark_safe(html)
