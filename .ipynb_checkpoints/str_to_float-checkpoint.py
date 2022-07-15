import re

def str_to_float(x, decimal_char=None):
    '''auxiliary function tries to convert <x> string into float, fixing thousands and decimal separators
    removes all non-numeric characters from string, except ['.',',','-', '%']
    
    > defining <decimal_char> force formatting number, removing the opposite thousands-separator-character
    (i.e.: decimal_char='.' will remove commas ',' from string number before converting into float)
    
    <return> float
        > ambiguous string numbers are returned as original strings
    '''
    pattern_US_decimal_point = re.compile(r"^\-?\$?(([0-9]{1,3},)*[0-9]{3}|([0-9]{1,3})|([0-9]+))(\.\d{1,2})$")
    pattern_EU_decimal_comma = re.compile(r"^\-?\$?(([0-9]{1,3}.)*[0-9]{3}|([0-9]{1,3})|([0-9]+))(\,\d{1,2})$")
    pattern_only_numeric = re.compile(r"^\-?(\d)*$")
    
    def _remove_currency(currency):
        if type(currency) is not str: # this check might be redundant
            return currency
        
        str_number = str(currency)
        list_char = ['.',',','-','%']

        for char in str_number:
            if not char.isnumeric(): 
                if char not in list_char:
                    str_number = str_number.replace(char, '')
                    
        return str_number

    if type(x) is int or type(x) is float:
        return float(x)
    
    result = _remove_currency(x)
    
    if len(result) ==0:
        return x
    elif pattern_only_numeric.search(result) is not None:
        result = float(result)
    elif pattern_US_decimal_point.search(result) is not None:
        # remove thousands_comma separators from all results that END with 1 or 2 decimal numbers
        result = float(result.replace(',',''))
    elif pattern_EU_decimal_comma.search(result) is not None:
        # remove thousands_point separators from all results that END with 1 or 2 decimal numbers
        result = float(result.replace('.','').replace(',','.'))
    else: # check for ambiguous formatting "100.000" or "100,000" of numbers without (1 or 2) decimal numbers, or more than 3 decimal numbers
        if decimal_char is not None:
            if decimal_char == '.':
                result = result.replace(',','') # remove thousands char
            elif decimal_char == ',':
                result = result.replace('.','').replace(',','.') # remove thousands char and change decimal comma to decimal point
        try:
            if '%' in result:
                result = float(result.replace('%','')) / 100
            else:
                result = float(result)
        except:
            result = str(result) + ' (ambiguous)'
    return result

def test_str_to_float(func=str_to_float, dec_char=None):
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
        '1.11': 1.11,
        '100.000': 100000,
        '100,000': 100000,
        '100000' : 100000,
        '0,5%': 0.005,
        '0.5%': 0.005
        
    }
    
    def _number_generator():
        result_list = []
        result_dict = {}
        #generating floating numbers
        '''
        for n in range(0,10):
            print(10**n)
        for n in range(0,6):
            print((1/(10)**n))
        '''

        for n in range(0,6):
            for y in range(0,6):
                for s in [1,-1]:
                    snum = f'{s*((1/(10)**n) + 10**y)}'
                    snum_us = f'{s*((1/(10)**n) + 10**y) :,}'
                    snum_br = snum.replace('.',',')
                    snum_br_tsep = snum_us.replace(',','X').replace('.',',').replace('X','.')
                    result_list.append(snum)
                    result_list.append(snum_us)
                    result_list.append(snum_br)
                    result_list.append(snum_br_tsep)
                    result_dict[snum] = float(snum)
                    result_dict[snum_us] = float(snum)
                    result_dict[snum_br] = float(snum)
                    result_dict[snum_br_tsep] = float(snum)

        return result_list, result_dict
    
    x, y = _number_generator()
    ttd = {**ttd, **y}
    
    # result header:
    print(f"{'<test>':5}{'| i: <input>':>13}{'<type> |' :>32}{' r: <result>':>20}{'<type> ':>32}{' | Pass? <True/False>':>20}")
    n = 1
    test_errors = 0
    test_report = []
    for k in ttd.keys():
        # result for each test
        i = k                          # function input (ttd.key)
        itype = str(type(i))           # function input type
        r = func(i,dec_char)           # function result (ttd.value)
        rtype = str(type(r))           # function result type
        testpass = (r == ttd[k]) # function result should be equal to tdd.value expected result
        
        row = f"{n:<5}  |{i:>15} {itype:>25} | {r:>20} {rtype:>30} | {str(testpass):>10}"
        print(row)
        
        if not testpass:
            test_errors +=1
            test_report.append(row + f' | Expected result: {ttd[k]}  -  {type(ttd[k])}')
        n+=1
        
    if test_errors >0:
        print(f"\n\nTest finished and found {test_errors} errors. These tests did not have the expected result from TTD dictionary\n {dec_char=}")
        for row in test_report:
            print(row)
    else:
        print("UNEXPECTED: Test finished and all tests passed. \n\n This shouldn't happen because pof the ambiguous results.")

if __name__ == '__main__':
    test_str_to_float(str_to_float, dec_char='.')