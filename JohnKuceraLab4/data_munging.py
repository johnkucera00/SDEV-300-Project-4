"""
__filename__ = "data_munging.py"
__coursename__ = "SDEV 300 6380 - Building Secure Web Applications (2198)"
__author__ = "John Kucera"
__copyright__ = "None"
__credits__ = ["John Kucera"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "John Kucera"
__email__ = "johnkucera00@gmail.com"
__status__ = "Test"
"""
import re
import pandas as pd


def get_contacts():
    """
    Return contact data
    """
    # First name, Last name, Zip code, Phone number
    contacts = [
        ['Yui', 'Hirasawa', '92375', '253-434-1298'],       # Perfect
        ['SATOSHI', 'Tainaka', '23452', '678-333-2222 '],   # CAPS Firstname
        ['', 'Father', '28877', '111-666-3333'],            # Empty Firstname string
        ['Keiko', 'iida', '21111', '000-333-7776'],         # lowercase Lastname
        ['Mother', '', '34333', '324-234-7898'],            # Empty Lastname string
        ['Mio', 'Akiyama', ' 25321-3452 ', '834-643-2347'], # 9-digit Zip
        ['Ui', 'Hirasawa', '174252345', '999-999-9999'],    # Zip with no hyphen
        ['Azusa', 'Nakano ', '', '2345345660'],             # Empty Zip string
        [' Ritsu', 'Tainaka', '555', '100-423-7989'],       # Invalid Zip, 3 digits
        ['Noboru', ' Taki', '123456', '111-222-3333'],      # Invalid Zip, 6 digits
        ['HazUki', 'KaTOU ', '0192933847', '000-999-2222'], # Invalid Zip, 9 digits
        ['Nozomi ', 'Kasaki', '12340.1222', '828-949-2929'],# Invalid Zip, period
        ['Tsumugi', 'Kotobuki', 'xd0bb', '856-132-7895'],   # Invalid Zip, Letters
        ['Sawako', 'YAMAnaka', '02029', '029485-7392'],     # Phone with no first hyphen
        ['NoDoka', 'Manabe', '77555', '154-1230098'],       # Phone with no second hyphen
        ['Jun', 'Suzuki', '111 45', ' 0192837465'],         # Phone with no hyphens, invalidzip
        ['Kumiko       ', 'Oumae', '21511 ', ''],           # Empty Phone string
        ['Reina', 'Kousaka ', ' 33322', '156'],             # Invalid phone, 3 digits
        ['SAPphire', 'Kawashima', '02354', '10101010101'],  # Invalid phone, 11 digits
        ['Asuka', 'Tanaka', '11100', 'dnqwid9222'],         # Invalid phone, some letters
        ['NAtSuki', 'Nakagawa', '62342', 'johnkucera'],     # Invalid phone, all letters
        ['Shuuichi', 'Tsukamoto', '11245', '(111)5551029'], # Phone with parentheses
        ['End ', 'Owari', ' 23040', '(919)122-1234 '],      # Phone with parentheses, hyphen
        ['Mizore123', 'YorOIZuka', '', '666-202-1234'],     # Invalid first name, number
        ['Yuuko', '44', '44444-1123 ', '1119998888']        # Invalid last name, number
    ]

    return contacts

def get_formatted_name(value):
    """
    Formatting Names
    """
    result = value.strip().title()
    # Valid name has only uppercase or lowercase letters
    if re.fullmatch('[a-zA-Z]*', result):
        return result
    # Invalid name
    else:
        return ''

def get_formatted_zip(value):
    """
    Formatting Zip Codes
    """
    result = value.strip()
    # 5 Digit zip code
    if re.fullmatch(r'\d{5}', result):
        return result

    # 9 Digit zip code
    elif re.fullmatch(r'\d{9}', result):
        return '-'.join(result[i:i+5]
                        for i in range(0, len(result), 5))

    # 9 Digit zip code with hyphen
    elif re.fullmatch(r'\d{5}-\d{4}', result):
        return result

    # Invalid zip code
    else:
        return ''

def get_formatted_phone(value):
    """
    Formatting Phone Numbers
    """
    value = value.strip()

    # 10 digit number with no hyphens
    if re.fullmatch(r'(\d{3})(\d{3})(\d{4})', value):
        result = re.fullmatch(r'(\d{3})(\d{3})(\d{4})', value)
        return '-'.join(result.groups())

    # 10 digit number with hyphens
    elif re.fullmatch(r'\d{3}-\d{3}-\d{4}', value):
        return value

    # 10 digit number with first hyphen
    elif re.fullmatch(r'(\d{3}-\d{3})(\d{4})', value):
        result = re.fullmatch(r'(\d{3}-\d{3})(\d{4})', value)
        return '-'.join(result.groups())

    # 10 digit number with second hyphen
    elif re.fullmatch(r'(\d{3})(\d{3}-\d{4})', value):
        result = re.fullmatch(r'(\d{3})(\d{3}-\d{4})', value)
        return '-'.join(result.groups())

    # 10 digit number with parentheses and hyphen
    elif re.fullmatch(r'([(]\d{3}[)])(\d{3}-\d{4})', value):
        result = re.fullmatch(r'([(]\d{3}[)])(\d{3}-\d{4})', value)
        result = '-'.join(result.groups())
        result = result.replace('(', '')
        result = result.replace(')', '')
        return result

    # 10 digit number with parentheses and no hyphen
    elif re.fullmatch(r'([(]\d{3}[)])(\d{7})', value):
        result = re.fullmatch(r'([(]\d{3}[)])(\d{3})(\d{4})', value)
        result = '-'.join(result.groups())
        result = result.replace('(', '')
        result = result.replace(')', '')
        return result

    # Invalid phone number
    else:
        return ''

def main():
    """
    Data Munging Application main
    """
    # Creating DataFrame
    contactsdf = pd.DataFrame(get_contacts(),
                              columns=['Firstname', 'Lastname', 'Zipcode', 'Phone'])

    # Applying all formatting to the DataFrame and printing
    formatted_first_name = contactsdf['Firstname'].map(get_formatted_name)
    contactsdf['Firstname'] = formatted_first_name

    formatted_last_name = contactsdf['Lastname'].map(get_formatted_name)
    contactsdf['Lastname'] = formatted_last_name

    formatted_zip = contactsdf['Zipcode'].map(get_formatted_zip)
    contactsdf['Zipcode'] = formatted_zip

    formatted_phone = contactsdf['Phone'].map(get_formatted_phone)
    contactsdf['Phone'] = formatted_phone

    print(contactsdf)
    return

if __name__ == "__main__":
    main()
