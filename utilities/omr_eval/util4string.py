def convert_hex2rgb(hexcode):
    """
    converts hexcode to rgb array
    returns rgb array

    parameters:
        hexcode(string|required): hexcode to convert
    """
    hexcolor = hexcode
    value = None
    foreground = hexcolor.replace('#', '').lower()
    if len(foreground) == 6 and '#' in hexcolor:
        value= list(int(foreground[i : i + 2], base=16) for i in (0, 2, 4))
    

def rgb2ascii(string, rgb):
    """converts rgb array into ascii text
    returns text in ascii format.

    paramters:
        string(string|required): string to apply ascii
        rgb(array|required): rgb value to convert into ascii
    """
    rc = rgb[0]
    gc = rgb[1]
    bc = rgb[2]
    resetter = "\x1b[0m"
    text= f"\033[38;2;{rc};{gc};{bc}m{string}{resetter}"
    
    return text

def get_asciiface(string, rgb=[255,255,255], bold=False, italic=False, underline=False,strike=False,dim=False, ):
    """
    parameters:
        string(string|required): string
        rgb(array|[255,255,255]): color of string
        bold, italic, underline, strike(bool|False): use face
        dim(bool|False): make font color 25% dimmert
    """
    
    resetter = "\x1b[0m"
    
    if dim:
        new_rgb = []
        for color in rgb:
            color = int(int(color)*0.75)
            new_rgb.append(color)
        rgb = new_rgb
    tempstr = ''
    tempstr = rgb2ascii(string, rgb)
    if bold:
        tempstr = "\x1b[1m" + tempstr + resetter
    if italic:
        tempstr =  "\x1b[3m" + tempstr + resetter
    if underline:
        tempstr = "\x1b[4m" + tempstr + resetter
    if strike:
        tempstr = "\x1b[9m" + tempstr +resetter
    
        
    return tempstr

from re import escape,finditer,findall,split,search,sub

def get_regmatch_str(string, pattern, first_match=False, ):
    """
    gets regex pattern matches as string
    returns string/array of strings

    parameters:
        string(string|rquired): string to base
        pattern(string|required): regex pattern
        first_match(bool|True): returns first match only else list
        chain(bool|False): will return chain object with value stored in .value
            chain object: grants access to additional methods
    """
    import re
    result = re.findall(pattern = pattern, string = string)
    result = result[0] if first_match else result
    
        
    return result

def get_regmatch_index(string, pattern, first_match=False, ):
    """
    gets regex pattern matches as indices
    returns string/array of indices

    parameters:
        string(string|rquired): string to base
        pattern(string|required): regex pattern
        first_match(bool|True): returns first match only else list
        chain(bool|False): will return chain object with value stored in .value
            chain object: grants access to additional methods
    """
    import re
    pattern = re.compile(pattern)
    result = []
    for matcher in pattern.finditer(string):
        result.append(list([matcher.start(),matcher.end()]))
        if first_match:
            result = result[0]
            break
    
        
    return result


def do_regtester(string, pattern, first_match=False):
    """
    gets regex pattern matches as indices
    returns string/array of indices

    parameters:
        string(string|rquired): string to base
        pattern(string|required): regex pattern
        first_match(bool|True): returns first match only else list
        chain(bool|False): will return chain object with value stored in .value
            chain object: grants access to additional methods
    """

    result = None
    index_match = get_regmatch_index(string, pattern, first_match=first_match)
    #index_match = self.clone().update(first_match=self._first_match).get()
    indices = []
    matches = []
    if first_match:
        index_match = [index_match]
    str_to_list = list(string)
    for pair in index_match:
        matches.append(''.join(list(string)[pair[0]:pair[1]]))
        for ind in range(pair[0], pair[1]):
            if ind not in indices:
                indices.append(ind)
    for ind in range(len(str_to_list)):
        if ind in indices:
            str_to_list[ind] = get_asciiface(str_to_list[ind], rgb=[255,255,255],underline=True)
    result = ''.join(str_to_list)
    result = result + '\n' + get_asciiface(', '.join(matches),rgb=[100,100,100])
    
        
    return result

def get_regmatch_groups(string, pattern, first_match=True, ):
    """
    gets regex pattern matches as indices
    returns string/array of indices

    parameters:
        string(string|rquired): string to base
        pattern(string|required): regex pattern
        first_match(bool|True): returns first match only else list
    """
    import re
    result = []
    pattern = re.compile(pattern)
    for matcher in pattern.finditer(string):
        result.append(list(matcher.groups()))
        if first_match: 
            result = result[0]
            break
    
        
    return result


def convert_str2list(string, sep=''):
    if sep=='':
        return list(string)
    else:
        return string.split(sep)
    

def get_alphanums(lowercase=False, uppercase=False, digits=False):
    import string
    result = []
    result += list(string.ascii_lowercase) if lowercase else  []
    result += (list(string.ascii_uppercase)) if uppercase else []
    result += list('01234567890') if digits else []
    return result

