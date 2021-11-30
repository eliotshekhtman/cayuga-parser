# e ogonek --> ~ t y
# o ogonek --> q
# o ogonek undersc --> 2
# a undersc --> 3 ;} a
# glottal --> '
# e undersc --> ~ ~
# e ogonek glot --> f
# might be space after glottal
# e ogonek undersc --> ~
# i undersc --> i

import random

words = [random.randint(1, 8633) for i in range(50)]
words.sort()
print(words)