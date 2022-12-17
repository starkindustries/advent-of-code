def transform_subject_num(subj, loop):
    # To transform a subject number, start with the value 1
    value = 1
    # Then, for a number of times (loop size), perform the following steps
    for _ in range(loop):
        value = loop_helper(subj, value)
    return value


def loop_helper(subj, value):
    # Set the value to itself multiplied by the subject number.
    # Set the value to the remainder after dividing the value by 20201227.
    return (value * subj) % 20201227


# Calculate public key
assert transform_subject_num(7, 8) == 5764801
assert transform_subject_num(7, 11) == 17807724

# Calculate the encryption key
assert transform_subject_num(17807724, 8) == 14897079
assert transform_subject_num(5764801, 11) == 14897079


# Part 1
def solve(pubkey1, pubkey2):
    # Figure out loop size for each public key
    loop_sizes = []
    for key in [pubkey1, pubkey2]:
        value = 1
        loops = 0
        while value != key:
            value = loop_helper(7, value)
            loops += 1
        print(f"Found loop size {loops} for {key}")
        loop_sizes.append(loops)
    # Calculate encryption key
    enc1 = transform_subject_num(pubkey1, loop_sizes[1])
    enc2 = transform_subject_num(pubkey2, loop_sizes[0])
    assert enc1 == enc2
    print(f"Found encryption key: {enc1}")
    return enc1


assert solve(5764801, 17807724) == 14897079
assert solve(8252394, 6269621) == 181800
