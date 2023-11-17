import jionlp as jio

def imagine_address(address):
    """ 
    根据地址信息，生成一个解析地址层级

    Args:
        address: 字符串，地址信息

    Returns:
        字符串，地址
    """

    if not isinstance(address, str):
        raise TypeError('the input address must be string')

    result = jio.parse_location(address)
    return result

    
# if __name__ == '__main__':
#     imagine_address("南海区南海万科广场")