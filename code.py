def get_words():
    # Load the file.
    with open('sgb-words.txt','r') as f:
        ## This includes \n at the end of each line:
        #words = f.readlines()
    
        # This drops the \n at the end of each line:
        words = f.read().splitlines()

    return words

all_words = get_words()

from random import randrange

def get_rand_word(available_words):
    rand_num = randrange(len(available_words))
    
    word = available_words[rand_num]
    return word

# convert btwn charaters and numbers
def char_position(letter):
    return ord(letter) - 96

def pos_to_char(pos):
    return chr(pos + 96)

def confirm_word_choice(choosen_word,available_words,choice):
    if choice:
        print('word choosen is '+choosen_word)
        return choosen_word
    else:
        word_confirmation = False

        while not word_confirmation:
            conformation = input("Do you want to use "+choosen_word+" as your word? answer with True or False ")

            if conformation == 'True':
                return choosen_word
            else:
                want_new_word = input("Want a new random word? answer with True or False ")
                if want_new_word == 'True':
                    choosen_word = get_rand_word(available_words)
                else:
                    inputted_new_word = input("Input desired word, must be five letters lowercase ")
                    return inputted_new_word
                

# get input from wordle
def get_results():
    result = int(input("Enter Result from Wordle: "))
    while len(str(result)) != 5:
        print('incorrect length')
        result = int(input("Enter Result from Wordle: "))
    return str(result)

def relay_results(inputted_word):
    results = get_results()

    for n in range(0,len(results)):
        letter = results[n]
        index_of_letter = char_position(inputted_word[n])-1

        if letter == '1':
            all_letters[index_of_letter]+=1
        if letter == '3':
            right_letters[n] = char_position(inputted_word[n])
        if letter == '2':

            if misplaced_letters[index_of_letter] == None:
                new_value = n
            else:
                new_value = [misplaced_letters[index_of_letter]] + [n]

            misplaced_letters[index_of_letter] = new_value
            
    return results

def get_viable_words(available_words):
    viable_words = []
    available_words = available_words

    for word in available_words:
        
        tfvalues = [None] * 5
        
        
        # write word as list of letter index positions
        as_num = [0] * 5
        for j in range(0,len(word)):
            as_num[j] = char_position(word[j])
            
        # eliminate words with letters that don't match right_letters
        # get matching data

        for n in range(0,len(as_num)):
            if right_letters[n] != 0:
                if (as_num[n] == right_letters[n]):
                    tfvalues[n] = (True)
                else:
                    tfvalues[n] = (False)


        # word must contain misplaced letters not in wrong spot
        for letter_index in range(0,len(misplaced_letters)):
            if misplaced_letters[letter_index] != None:

                # does word contain letter?
                if (letter_index+1) in as_num:
                    # yes word contains letter
                    
                    # is letter in wrong position?
                    #letter should not be in positions misplaced_letters[letter_index]

                    # get letter position(s)
                    letter_positions = []
                    for given in range(0, len(as_num)):
                        if as_num[given] == letter_index+1:                        
                            letter_positions = letter_positions + [given]

                    if misplaced_letters[letter_index] in letter_positions:
                        #letter in position, not viable, set positions to false
                        for n in letter_positions:
                            if n == misplaced_letters[letter_index]:
                                tfvalues[n] = False
                else:
                    # word does not contain letter!
                    for value in range(0,len(tfvalues)):
                        tfvalues[value] = False
                        
        # find if the word contains wrong letters <- still needs to be checked for all cases
        for letter_index in range(0,len(all_letters)):
            if all_letters[letter_index] > 0:
                for given in range(0, len(as_num)):
                    if (tfvalues[given] != True) & (as_num[given] == (letter_index+1)):
                        tfvalues[given] = False

        if False not in tfvalues:
            viable_words.append(word)
            
    return viable_words


# set general databases
all_letters = [0] * 26
misplaced_letters = [None] * 26
right_letters = [0] * 5

viable_words = []

word_found = False



#get_most_probable_word()

while not word_found:
    next_word = get_rand_word(all_words)

    choosen_word = confirm_word_choice(next_word,viable_words,False)

    results = relay_results(choosen_word)

    viable_words = get_viable_words(viable_words)
    
    if (results == '33333') or (len(viable_words) == 1):
        word_found = True
    
print('word found! word was '+choosen_word)
