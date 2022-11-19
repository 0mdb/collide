from unidecode import unidecode
import string


def create_match_name(name_in):
    # remove any accented characters
    new = unidecode(name_in)
    # remove punctuation, since it may or may not always be present (e.g. Inc. vs Inc)
    new = new.translate(str.maketrans('', '', string.punctuation))
    # strip out all the whitespace, since there may be one space or two, etc
    new = new.translate(str.maketrans('', '', string.whitespace))
    # convert to lower case
    new = new.lower()
    return new


# if __name__ == "__main__":
#
#     test_list = ['Canadian Turkey Marketing Agency C.O.B. as Turkey Farmers of Canada',
#                  'Petro-Canada',
#                  'Fédération des communautés Francophones et Acadienne du Canada',
#                  ]
#
#     for s in test_list:
#         print(create_match_name(s))
