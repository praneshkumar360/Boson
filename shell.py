import boson

while True:
    text = input("Boson > ")
    if text.strip() == "": continue
    result, error = boson.run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(result.elements[0])
        else:
            print(repr(result))

