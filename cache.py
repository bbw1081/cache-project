
def get_values():
    while(True):
        nominal_size = input("Give nominal size in bytes ")
        try:
            nominal_num = int(nominal_size)
            break
        except ValueError:
            print("Invalid input, try again!")

    while(True):
        words_per_block = input("Give the number of words per block (1,2,4,8)")
        try:
            words_per_block_num = int(words_per_block)
            if(not words_per_block_num in (1, 2, 4, 8)):
                print("invalid input, try again!")
            else:
                break
        except ValueError:
            print("invalid input, try again!")

    # maping policy : 0 for DM, 1 for set-associative
    while(True):
        mapping_policy = input("Enter mapping policy, 0 for Direct-Mapped and 1 for set-associative ")
        if(mapping_policy == "1"):
            while(True):
                n_sets = input("enter the N number of sets ")
                try:
                    n_sets_num = int(n_sets)
                    break
                except ValueError:
                    print("invalid input, try again!")
            break
        elif(mapping_policy == "0"):
            n_sets_num = None
            break
        else:
            print("Invalid input! Try again")

    while(True):
        blocks_per_set = input("Give the number of blocks per set ")
        try:
            blocks_per_set_num = int(blocks_per_set)
            break
        except ValueError:
            print("Invalid input, try again!")

    return nominal_num, words_per_block_num, int(mapping_policy), n_sets_num, blocks_per_set_num

def main():
    nominal_size, words_per_block, mapping_policy_int, num_sets, blocks_per_set = get_values()    

if __name__ == "__main__":
    main()