"""Utility class to parse generic fields
"""
import re
class GenericFieldParser:
    """Utility class to parse generic fields

    Methods
    -------
    has_special_characters:
        returns True if the input string has special characters
    convert_json_to_dot_formatted_fields:
        converts the given data into json dot formated fields
    find_generic_fields:
        returns the list of fields which are generic
    """
    @staticmethod
    def has_special_characters(input_string): 
        regex= re.compile('[@_!#$%^&*()<>?/\\\|}{~:[\]]') 
        return not regex.search(str(input_string)) == None

    @staticmethod
    def convert_json_to_dot_formated_fields(data, prefix="request",values={}):
        if isinstance(data, dict):
            for key in data.keys():
                GenericFieldParser.convert_json_to_dot_formated_fields(data[key], prefix + "." + str(key),values=values)
        elif isinstance(data, list):
            for index,key in enumerate(data):
                GenericFieldParser.convert_json_to_dot_formated_fields(key, prefix + "." + str(index),values=values)
        else:
            values[prefix]=data

    @staticmethod
    def find_generic_fields(data, prefix=""):
        generic_fields={}
        dot_formated_fields={}
        GenericFieldParser.convert_json_to_dot_formated_fields(data, prefix=prefix, values=dot_formated_fields)
        for key in dot_formated_fields.keys():
            if GenericFieldParser.has_special_characters(dot_formated_fields[key]):
                generic_fields[key]=dot_formated_fields[key]
        return generic_fields
    
    
    
