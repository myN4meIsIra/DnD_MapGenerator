# generate a map and populate it into a bmp... basically

import random

from element import Element
from building_rules import rules
from loggingAndOutput import Logging
Logging = Logging(False)
from statics import weights


class GenerateAndPopulate():

    def procedural_generation(self, Creation, img, pixels, generationIterations, material):

        # matrix of types of elements
        blockMatrix = []
        for i in range(Creation.blocksWidth+1):
            blockColumn = []
            #Logging.log("","\n")
            for j in range(Creation.blocksHeight+1):
                blockColumn.append(0)
                #Logging.log(f"[{i},{j}]", "")
            blockMatrix.append(blockColumn)

        Logging.say('generating map')
        for iteration in range(generationIterations):
            Logging.say(f'running map population through iteration {iteration + 1} of {generationIterations}')


            # generate borders
            """
            Logging.say('generating borders')

            for borderX in range(0, Creation.blocksWidth):
                element.new('wall', material, 'h')
                blockMatrix[borderX][0] = element
                blockMatrix[borderX][Creation.blocksHeight] = element

            for borderY in range(0, Creation.blocksHeight):
                element.new('wall', material, 'v')
                blockMatrix[0][borderY] = element
                blockMatrix[Creation.blocksWidth][borderY] = element
            """


            # generate structure,
            for blockX in range(Creation.blocksWidth):
                Logging.log("", "\n")
                for blockY in range(Creation.blocksHeight):
                    ceiling, floor, left, right = "none", 'none', 'none', 'none'
                    # orientation = 'h'
                    # logic for generating the next element
                    Logging.log(f"[{blockX},{blockY}]", '')
                    if blockY > 0:                       ceiling = blockMatrix[blockX][blockY - 1]
                    if blockY < Creation.blocksHeight:   floor = blockMatrix[blockX][blockY + 1]
                    if blockX > 0:                       left = blockMatrix[blockX - 1][blockY]
                    if blockX < Creation.blocksWidth:    right = blockMatrix[blockX + 1][blockY]

                    Logging.log(f"ceiling:{ceiling}, floor:{floor}, left:{left}, right:{right}", '\n')

                    possibleNextElements = []

                    # ceilings
                    if ceiling != 'none' and ceiling != 0:
                        for type in rules['ceiling'][
                            str(ceiling.getElementType()) + "-" + str(ceiling.getOrientation())]:
                            # print(f'type is {type}')
                            possibleNextElements.append(type)
                    if floor != 'none' and floor != 0:
                        '''for type in rules['floor'][floor.getElementType()]:
                            print(f'type is {type}')
                            possibleNextElements.append(type)
                        '''
                        # copy ceiling and floor rules
                        for type in rules['ceiling'][str(floor.getElementType()) + "-" + str(floor.getOrientation())]:
                            # print(f'type is {type}')
                            possibleNextElements.append(type)
                    if right != 'none' and right != 0:
                        for type in rules['right'][str(right.getElementType()) + "-" + str(right.getOrientation())]:
                            # print(f'type is {type}')
                            possibleNextElements.append(type)
                    if left != 'none' and left != 0:
                        # copy the left and right rules
                        for type in rules['right'][str(left.getElementType()) + "-" + str(left.getOrientation())]:
                            # print(f'type is {type}')
                            possibleNextElements.append(type)

                        '''
                        for type in rules['left'][left.getElementType()]:
                            print(f'type is {type}')
                            possibleNextElements.append(type)
                        '''
                    else:
                        possibleNextElements = [{'wall': 'h'}, {'floor': ""}, {'tree': ""}, {'door': 'h'}]

                    # if there is a vertical wall above or below and a horizontal wall left or right, force a corner wall
                    verticalPresent = False
                    horizontalPresent = False
                    for l in possibleNextElements:
                        # print(f'l is {l}')
                        if list(l.keys())[0] == 'h':
                            horizontalPresent = True
                        if list(l.keys())[0] == 'v':
                            verticalPresent = True
                        if (horizontalPresent and verticalPresent):
                            Logging.log('there be walls here', '\n')

                            possibleNextElements.remove({'wall': 'h'})
                            possibleNextElements.remove({'wall': 'v'})
                            break

                    #Logging.log(f"the list of possible next elements: {possibleNextElements}", '\n')

                    # select element to built based on probability distribution
                    weightList = []
                    for thingy in possibleNextElements:
                        Logging.log(f'thingy = {thingy} \t key = {list(thingy.keys())[0]} \t weight[thingy] {weights[list(thingy.keys())[0]]}','\n')
                        weight = weights[list(thingy.keys())[0]]
                        weightList.append(weight)

                    # select at random next element
                    Logging.log(f"weights list: {weightList}", '\n')
                    type = random.choices(possibleNextElements, weights=weightList, k=1)[0]
                    elementType = list(type.keys())[0]
                    material = material
                    orientation = type[elementType]
                    Logging.log(f"type chosen to build {elementType}, {material}, {orientation}","\n")


                    element = Element()
                    element.new(elementType, material, orientation)
                    if blockX in list([Creation.blocksWidth-1, 0]):
                        element.new('wall', material, 'v')
                    if blockY in list([Creation.blocksHeight-1, 0]):
                        element.new('wall', material, 'h')

                    Logging.log(f"[{blockX},{blockY}, {elementType}]", '')
                    blockMatrix[blockX][blockY] = element


        return self.populateMap(Creation, img, pixels, blockMatrix)


    def populateMap(self, Creation, img, pixels, blockMatrix):
        Logging.say('\n\npopulating map')

        # translate blockMatrix into image
        for blockX in range(Creation.blocksWidth):
            if Creation.blocksHeight > 90 or Creation.blocksWidth > 90:
                Logging.say(f"row {blockX} of {Creation.blocksWidth}")

            Logging.log("", '\n')
            for blockY in range(Creation.blocksHeight):

                # pull data from element at [blockX, blockY]
                element = blockMatrix[blockX][blockY]
                elementType = element.getElementType()
                material = element.getMaterial()
                orientation = element.getOrientation()

                Logging.log(f"[{blockX},{blockY}, {elementType}]", '')

                # operation to perform
                if elementType == 'wall':
                    filledArea = Creation.wall(material, orientation)

                elif elementType == 'floor':
                    filledArea = Creation.floor(material)

                elif elementType == 'door':
                    filledArea = Creation.door(material, orientation)

                elif elementType == 'road':
                    filledArea = Creation.road(material, orientation)

                elif elementType == 'tree':
                    filledArea = Creation.tree(orientation, material)

                # print(f'last element type {elementType}')

                # transfer operated area into main image
                for i in range(Creation.blockSize):
                    for j in range(Creation.blockSize):
                        pixels[i + (blockX * Creation.blockSize), j + (blockY * Creation.blockSize)] = filledArea[i, j]
                        # print(f'image[{i+(blockX*self.blockSize)},{j+(blockY*self.blockSize)}] <-- [{i},{j}]')
                filledArea = None

        return img
