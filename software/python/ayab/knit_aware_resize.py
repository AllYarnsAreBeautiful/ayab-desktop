
from PIL import Image
from math import sqrt, log, floor


def resize_image(image, width_proportion, height_proportion):
    width, height = image.size
    resized_image = image.transform(
        (width_proportion * width, height_proportion * height),
        Image.AFFINE,
        (1./width_proportion, 0, 0, 0, 1./height_proportion, 0),
        Image.NEAREST)
    return resized_image


## Based on code from:
## https://groups.yahoo.com/neo/groups/tuning-math/conversations/topics/14958

def contfrac(a): ### continued fraction expansion
    terms=[]
    count=0
    b=1
    while ((b != 0) and (count < 7)): ### 5 times, emprical accuracy measurement
    ### limit
        terms.append(floor(a/(b+0.0)))
        a,b = b, a % b
        count = count + 1
    return terms


def ra(x): ### 'rational approximation', or convergent
    numerators=[0,1]
    denominators=[1,0]
    expansion=contfrac(x) ### call the contfrac function
    for num in expansion: ### [-1] and [-2] index 'previous'
        ### and 'previous-previous'
        numerators.append((num*numerators[-1])+numerators[-2])
        denominators.append((num*denominators[-1])+denominators[-2])

    for index in range(len(numerators)):
        yield (numerators[index], denominators[index])
        #print "%i/%i" % (numerators[index], denominators[index])

def get_rational_ratios(ratio):
    ratios_list = list(ra(ratio))
    return ratios_list[2::]
