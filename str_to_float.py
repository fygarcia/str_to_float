import re
def str_to_float(x):
    '''auxiliary function try to convert string into float,
    fixing thousands and decimal separators
    '''
    pattern_US_decimal_point = re.compile(r"^\-?\$?(([0-9]{1,3},)*[0-9]{3}|([0-9]{1,3})|([0-9]+))(\.\d{1,2})?$")

    def _remove_currency(currency):
        if type(currency) is not str:
            return currency
        str_number = currency
        for char in currency:
            if not char.isnumeric():
                if char not in ['.',',','-']:
                    str_number = str_number.replace(char, '')
                    #print('Char removed: ', char)
        return str_number

    if type(x) is int or type(x) is float:
        return float(x)

    result = _remove_currency(x)

    if pattern_US_decimal_point.search(result) is not None:
        # remove thousands_comma separators
        result = result.replace(',','')

    try:
        result = float(result) # try to convert to float first to prevent unintended decimal dot removal
    except:
        result = x


    # fix decimal first (first sep character from right to left) # ERROR: REPLACE THIS BLOCK
    '''
    if type(result) is str:
        result = result.replace('.', '').replace(',','.') # remove dots first, then, replace comma with dot
        # remove currency letters
        for letter in result:
            if letter.isalpha():
                result.replace(letter, '')
    '''

    return result

def test_str_to_float(func=str_to_float):
    '''testing function: this test will use ttd dicitonary keys as input for the function
    and compare its result with each expected result from the ttd dictionary values
    '''
    ttd = {
        '1,10': 1.1,         # string converted into float (decimal separator is comma)
        '1.10': 1.1,         # string converted into float (decimal separator is dot)
        '1.000,00': 1000.0,  # string converted into float (dot as thousands sep, and comma as decimal sep)
        '1,000.00': 1000.0,  # string converted into float (comma as thousands sep, and dot as decimal sep)
        1: 1.0,              # int converted into float
        0: 0.0,              # zero converted into float
        1.1: 1.1,            # float return float
        10000.0: 10000.0,    # float return float
        'a': 'a',            # string characters return self
        '   1.00  ': 1.00,
        ' US$ 1.01 ': 1.01,
        ' R$1,01': 1.01,
        ' R$ 1.100,55': 1100.55,
        'R$ 1.000,01':1000.01,
        'R$1.123,01':1123.01,
        'R$ 11.000,01':11000.01,
        'R$ 1.000':1000,
        'R$ 10,01':10.01,
        ' US$1,123.99':1123.99,
        'US $ 1,999':1999,
        'US$ 1,223.00':1223.00,
        ' 1.20,10 ': ' 1.20,10 ',
        ' 1,20.10 ': ' 1,20.10 ',
        '1.11': 1.11
    }
    # result header:
    print(f"{'<test>':5}{' | i: <input>':>10}{' <type>' :^20}{' | r: <result>':>5}{' <type>':>20}{' | Pass? <True/False>':>20}")
    n = 1
    test_errors = 0
    test_report = []
    for k in ttd.keys():
        # result for each test
        i = k                          # function input (ttd.key)
        itype = str(type(i))           # function input type
        r = func(i)                    # function result (ttd.value)
        rtype = str(type(r))           # function result type
        testpass = (func(i) == ttd[k]) # function result should be equal to tdd.value expected result

        row = f"{n:<5}  |{i:>10} {itype:>20} | {r:>10} {rtype:>20} | {str(testpass):>10}"
        print(row)

        if not testpass:
            test_errors +=1
            test_report.append(row)
        n+=1

    if test_errors >0:
        print(f"\n\nTest finished and found {test_errors} errors. These tests did not have the expected result from TTD dictionary")
        for row in test_report:
            print(row)
    else:
        print("Test finished and all tests passed.")

if __name__ == '__main__':
    test_str_to_float(str_to_float)
