import sys


snafu_symbol_chart = {
    "0": 0,
    "1": 1,
    "2": 2,
    "-": -1,
    "=": -2
}
# 0, 1, 2, -, =
def convert_from_snafu(snafu):
    reverse_snafu = snafu[::-1]
    sum = 0
    for place, ch in enumerate(reverse_snafu):
        ch_value = snafu_symbol_chart[ch]
        temp = (5 ** place) * ch_value
        sum += temp
    return sum


def get_max_negative(power):
    result = 0
    while power >= 0:
        result += -2 * 5 ** power
        power -= 1
    return result


decimal_symbol_chart = {
    0 : "0",
    1 : "1",
    2 : "2",
    -1 : "-",
    -2 : "="
}
def convert_from_decimal(decimal):    
    snafu = ""
    # 314159265
    # reverse_decimal = str(decimal)[::-1]
    power = 0
    while 5 ** power < decimal:
        power += 1
    # power -= 1

    while power >= 0:
        for digit in [2, 1, 0, -1, -2]:
            place_value = (5 ** power * digit)
            max_negative = get_max_negative(power - 1) 
            if place_value + max_negative > decimal:
                continue
            decimal -= place_value
            snafu += decimal_symbol_chart[digit]
            power -= 1
            break
    while True:
        if snafu[0] == "0":
            snafu = snafu[1:]
            continue
        break            
    # while power > 0:
    #     snafu += "0"
    #     power -= 1
    print(snafu)
    return snafu
    # snafu += "1"
    # sum = 0
    # for place, ch in enumerate(reverse_decimal):
    #     ch_value = snafu_symbol_chart[ch]
    #     temp = (5 ** place) * ch_value
    #     sum += temp
    # return sum


# MAIN
# try:
#     filename = str(sys.argv[1])
# except Exception as e:
#     print("Warning exception:", e)
#     filename = "sample"
# # assert filename == "input" or filename == "sample"
# filename += ".txt"


snafu_to_decimal = {}
decimal_to_snafu = {}
filename = "sample.txt"
with open(filename, "r") as handle:
    for line in handle:
        line = line.strip().split()
        if not line:
            continue
        if line[0] == "Decimal":
            decimal_first = True
            continue
        if line[0] == "SNAFU":
            decimal_first = False
            continue
        if decimal_first:
            decimal = int(line[0])
            snafu = line[1]
        else:
            decimal = int(line[1])
            snafu = line[0]
        decimal_to_snafu[decimal] = snafu
        snafu_to_decimal[snafu] = decimal

convert_from_decimal(5)
convert_from_snafu("1121-1110-1=0")
for decimal, snafu in decimal_to_snafu.items():    
    print(f"Converting between snafu:{snafu} and decimal:{decimal}")
    assert snafu_to_decimal[snafu] == convert_from_snafu(snafu)
    assert decimal_to_snafu[decimal] == convert_from_decimal(decimal)


filename = "input.txt"
sum = 0
with open(filename, "r") as handle:
    for line in handle:
        snafu = line.strip()
        sum += convert_from_snafu(snafu)
answer = convert_from_decimal(sum)
print(answer)