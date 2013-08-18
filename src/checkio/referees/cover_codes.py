unwrap_args = '''

def cover(func, in_data):
    return func(*in_data)

'''

unwrap_kwargs = '''

def cover(func, in_data):
    return func(**in_data)

'''

