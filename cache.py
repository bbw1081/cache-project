def get_values():
    while(True):
        nominal_size = input("Give nominal size in bytes ")
        try:
            nominal_num = int(nominal_size)
            break
        except ValueError:
            print("Invalid input, try again!")

    words_per_block = input("Give the number of words per block (1,2,4,8)")
    while(True):
        if(not words_per_block in (1, 2, 4, 8)):
            words_per_block = input("Try again! must be 1, 2, 4, or 8")
        else:
            break

    # maping policy : 0 for DM, 1 for set-associative
    while(True):
        mapping_policy = input("Enter mapping policy, 0 for Direct-Mapped and 1 for set-associative ")
        if(mapping_policy == "1"):
            n_sets = input("enter the N number of sets ")
            break
        elif(mapping_policy == "0"):
            break
        else:
            print("Invalid input! Try again")

    while(True):
        blocks_per_set = input("Give the numer of blocks per set ")
        try:
            blocks_per_set_num = int(blocks_per_set)
            break
        except ValueError:
            print("Invalid input, try again!")

def main():
    get_values()

if __name__ == "__main__":
    main()