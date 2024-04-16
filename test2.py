xpath_list = []

for i in range(3, 8):
    xpath = '//*[@id="botstuff"]/div/div[3]/table/tbody/tr/td[{}]/a'.format(i)
    xpath_list.append(xpath)

print(xpath_list)
