import syntax_check

def is_code_complete(code):
    try:
        syntax_check.check(code)
        return True
    except syntax_check.SyntaxError:
        return False

# Example code snippets
incomplete_code = '''
def incomplete_function():
    if x:
        print("Hello")
'''

complete_code = '''
def complete_function():
    if x:
        print("Hello")
'''

print("Incomplete code:", is_code_complete(incomplete_code))
print("Complete code:", is_code_complete(complete_code))
