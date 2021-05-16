import zero

while True:
    text = input('zero > ')
    result, error = zero.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)
