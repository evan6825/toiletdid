mystring = "Alice"
mybytes = mystring.encode('utf-32')
myint = int.from_bytes(mybytes, 'little')
print(myint)
recoveredbytes = myint.to_bytes((myint.bit_length() + 7) // 8, 'little')
recoveredstring = recoveredbytes.decode('utf-32')
print(recoveredstring)