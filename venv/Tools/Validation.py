# CreatedBy: Emilia Crow
# CreateDate: 20210330
# Updated: 20210811
# CreateFor: Franklin Young International
# -*- coding: utf-8 -*-

import re

class Validator:
    def __init__(self):
        self.name = 'Vlad the Validator'

    def validate_spelling(self, in_phrase):

        return True

    def validate_measure(self, in_phrase):
        pattern = '(\d{1,8}\.?\d{0,3}\s?\w{1,4})'
        match = re.search(pattern, string)
        if match:
            process(match)

        return True

    def review_product_number(self, product_number):
        test_number = product_number[:4]+product_number[5:]
        test_number = test_number.replace(' ','')
        pattern = '(\W)'
        match = re.search(pattern, test_number)
        if match:
            return False

        return True

    def run_cleaning(self, in_phrase):
        out_phrase = in_phrase

        out_phrase = self.validate_spelling(out_phrase)
        out_phrase = self.validate_measure(out_phrase)

        return out_phrase

    def validate_lead_time(self,lead_time):
        return_val = False
        if 365 > lead_time > 0:
            return_val =  True

        return return_val

    def clean_part_number(self,str_to_clean, leave_gap = False):
        pattern = '(\W)'
        if leave_gap:
            str_to_clean = re.sub(pattern, ' ', str_to_clean)
        else:
            str_to_clean = re.sub(pattern, '', str_to_clean)
        str_to_clean = str_to_clean.strip()
        return str_to_clean

    def clean_country_name(self,str_to_clean, leave_gap = False):
        pattern = '(\-|\.|`|,|/|\+|\&|\_|\s|\"|\'|#|=|\$|\\\\|\(|\))'
        if leave_gap:
            str_to_clean = re.sub(pattern, ' ', str_to_clean)
        else:
            str_to_clean = re.sub(pattern, '', str_to_clean)
        str_to_clean = str_to_clean.strip()
        return str_to_clean

    def bc_image_name(self,image_name):
        pattern = '(\.500\.500\_\_\d*)'
        image_name = re.sub(pattern, '', image_name)
        return image_name

    def clean_description(self,description):
        pattern = ''
        description = re.sub(pattern, '', description)
        return description

    def prep_for_category_match(self,look_up_val):
        look_up_val = ' '+look_up_val+' '
        pattern_punctuation = '([{}()-\.,;:\'\"/^_#<>!%&?=~`°+])'
        look_up_val = re.sub(pattern_punctuation, ' ', look_up_val)

        pattern_number = '(\d{1,4})'
        look_up_val = re.sub(pattern_number, ' ', look_up_val)

        pattern_short_word = '(?<=\W)(\w{0,2})(?=\W)'
        look_up_val = re.sub(pattern_short_word, '', look_up_val)

        look_up_val = look_up_val.replace('[','')
        look_up_val = look_up_val.replace(']', '')

        look_up_val = look_up_val.replace('  ', ' ')
        look_up_val = look_up_val.strip()
        look_up_val = look_up_val.lower()

        look_up_val = look_up_val.replace(' for ', ' ')
        look_up_val = look_up_val.replace(' and ', ' ')

        return look_up_val

    def imperial_validation(self,in_term):
        out_term = in_term.replace('\'','ft.')
        out_term = out_term.replace('\"','in.')
        return out_term

    def regular_standards(self, in_phrase):
        # this will house all the standardization of characters and terms and such
        out_phrase = in_phrase.replace('–','-')
        return out_phrase

    def remove_unicode(self,in_phrase):
        out_phrase = in_phrase.replace('Î»','[lambda]')

        out_phrase = out_phrase.replace('Î±','[alpha]')
        out_phrase = out_phrase.replace('Â±', '[alpha]')
        out_phrase = out_phrase.replace('Î©','[omega]')
        out_phrase = out_phrase.replace('Ï‰','[omega]')
        out_phrase = out_phrase.replace('Î³','[gamma]')
        out_phrase = out_phrase.replace('Î¼','u')
        out_phrase = out_phrase.replace('•¡','u')
        out_phrase = out_phrase.replace('Âµ','u')
        out_phrase = out_phrase.replace('Îº','[kappa]')
        out_phrase = out_phrase.replace('Â²','[beta]')
        out_phrase = out_phrase.replace('Î²','[beta]')
        out_phrase = out_phrase.replace('ÃŸ','[beta]')
        out_phrase = out_phrase.replace('Îµ','[epsilon]')
        out_phrase = out_phrase.replace('Î¸','[theta]')
        out_phrase = out_phrase.replace('Ïƒ','[sigma]')

        out_phrase = out_phrase.replace('‚„','')
        out_phrase = out_phrase.replace('â a','')

        out_phrase = out_phrase.replace('”¬',' ')
        out_phrase = out_phrase.replace('ÃŽ',' ')

        out_phrase = out_phrase.replace('–‘','°')
        out_phrase = out_phrase.replace('Ëš','°')
        out_phrase = out_phrase.replace('Â°', '°')
        out_phrase = out_phrase.replace('â€', '\"')
        out_phrase = out_phrase.replace('â€™', '\'')
        out_phrase = out_phrase.replace('"™','\'')


        out_phrase = out_phrase.replace('ˆ’','-')
        out_phrase = out_phrase.replace('"“','-')
        out_phrase = out_phrase.replace('€“','-')
        out_phrase = out_phrase.replace('‰¤','<=')
        out_phrase = out_phrase.replace('‰¥','>=')
        out_phrase = out_phrase.replace('„¢','(r)')
        out_phrase = out_phrase.replace('Â®','(r)')

        out_phrase = out_phrase.replace('â€','-')
        out_phrase = out_phrase.replace('â€','-')

        out_phrase = out_phrase.replace('Ã¤','a')
        out_phrase = out_phrase.replace('Ã¡','a')
        out_phrase = out_phrase.replace('Ã…','a')
        out_phrase = out_phrase.replace('Ã±','n')
        out_phrase = out_phrase.replace('Å„','n')
        out_phrase = out_phrase.replace('Ã©','e')
        out_phrase = out_phrase.replace('Ã¨','e')
        out_phrase = out_phrase.replace('Ã³','o')
        out_phrase = out_phrase.replace('Ã¶','o')
        out_phrase = out_phrase.replace('Ã­','i')
        out_phrase = out_phrase.replace('Ã®','i')
        out_phrase = out_phrase.replace('Ã¯','i')
        out_phrase = out_phrase.replace('Ã½','y')
        out_phrase = out_phrase.replace('Ã¼','u')
        out_phrase = out_phrase.replace('Ãº','u')
        out_phrase = out_phrase.replace('Ã—','x')
        out_phrase = out_phrase.replace('Å¡','s')
        out_phrase = out_phrase.replace('Å‚','l')
        out_phrase = out_phrase.replace('Ã‚Â', '')

        out_phrase = out_phrase.replace('â','-')

        # and many more

        return out_phrase

    def isEnglish(self,in_phrase):
        try:
            in_phrase.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def clean_temp(self, in_phrase):
        out_phrase = in_phrase.replace('–','-')
        return out_phrase



def test_frame():
    char = ','
    test_word = char+'123'+char+'456'+char
    print(test_word)
    print(clean_part_number(test_word))


def clean_part_number(str_to_clean):
    pattern = '(\-|\.|,|/|\+|\&|\_|\s|\"|\'|#|=|\$|\\\\|\(|\))'
    str_to_clean = re.sub(pattern, '', str_to_clean)
    str_to_clean = str_to_clean.strip()
    return str_to_clean

if __name__ == '__main__':
    test_frame()



## end ##