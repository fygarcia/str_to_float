def str_to_float(x):
    '''auxiliary function try to convert string into float, fixing thousands and decimal separators
    '''
    result = x
    try:
        result = float(result) # try to convert to float first to prevent unintended decimal dot removal
    except:
        pass
    if type(result) is str:
        result = result.replace('.', '').replace(',','.') # remove dots first, then, replace comma with dot
    try:
        result = float(result) # try to convert into float after dot/comma replacement
    except:
        result = x             # the exception means it cannot be converted
        
    return result

def test_str_to_float(func):
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
        'a': 'a'             # string characters return self
    }
    # result header:
    print(f"{'<test>':5}{' | i: <input>':>10}{' <type>' :^20}{' | r: <result>':>5}{' <type>':>20}{' | Pass? <True/False>':>20}")
    n = 1
    test_errors = 0
    for k in ttd.keys():
        # result for each test
        i = k                          # function input (ttd.key)
        itype = str(type(i))           # function input type
        r = func(i)                    # function result (ttd.value)
        rtype = str(type(r))           # function result type
        testpass = (func(i) == ttd[k]) # function result should be equal to tdd.value expected result
        print(f"{n:<5}  |{i:>10} {itype:>20} | {r:>10} {rtype:>20} | {str(testpass):>10}")
        
        if not testpass:
            test_errors +=1
        
        n+=1
        
    if test_errors >0:
        print(f"Test finished and found {test_errors} errors. These tests did not have the expected result from TTD dictionary")
    else:
        print("Test finished and all tests passed.")

if __name__ == '__main__":
    test_str_to_float(str_to_float)