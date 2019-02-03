import random, discord
from math import ceil
client = discord.Client()

typeIconConversionTable = {"1": "<:1:541411666085150730>", 
    "2": "<:2:541411762151358465>", 
    "3": "<:3:541411666093539338>", 
    "4": "<:4:541411666068504586>",
    "5": "5",
    "6": "6",
    "mine": "<:m:541411666110447616>", 
    "empty": "<:c:541411666647187467>"
    }

class Utility():
    def randomChance(chance):
        randomList = list(range(1, 101))
        randomChoice = random.choice(randomList)
        print(randomChoice)
        if chance >= randomChoice:
            return True
        return False

    def randomCell(dimensions):
        randomRow, randomColumn = range(1, len(dimensions)), range(1, len(dimensions))
        randomRowChoice, randomColumnChoice = random.choice(randomRow), random.choice(randomColumn)
        return "{0}row{1}columnCell".format(randomRowChoice, randomColumnChoice)

    def getNearbyCells(currentCell):
        rowNumber = int(currentCell.split("row")[0])
        columnNumber = int(currentCell.split("row")[1].replace("columnCell", ""))
        return [
            "{0}row{1}columnCell".format(rowNumber-1, columnNumber-1),
            "{0}row{1}columnCell".format(rowNumber-1, columnNumber),
            "{0}row{1}columnCell".format(rowNumber-1, columnNumber+1),
            "{0}row{1}columnCell".format(rowNumber, columnNumber-1),
            "{0}row{1}columnCell".format(rowNumber, columnNumber+1),
            "{0}row{1}columnCell".format(rowNumber+1, columnNumber-1),
            "{0}row{1}columnCell".format(rowNumber+1, columnNumber),
            "{0}row{1}columnCell".format(rowNumber+1, columnNumber+1)
        ]

    def checkNearbyCells(board, cell):
        nearbyCells = Utility.getNearbyCells(cell)
        for cellNumber in nearbyCells:
            if "0" not in cellNumber:
                if getattr(board, cellNumber).type == "mine":
                    return False
        return True

class Cell():
    def __init__(self, type="empty"):
        self.type = type
        self.icon = typeIconConversionTable[self.type]
    
    def setType(self, type):
        self.icon = typeIconConversionTable[type]
        self.type = type

    def increaseValue(self):
        if self.type != "mine":
            if self.type == "empty":
                self.setType("1")
                return True
            self.setType(str(int(self.type)+1))
            return True
        return False


class Board():
    def __init__(self, dim=5):
        self.dimensions = list(range(1, dim + 1))
        self.dimensionsInt = dim
        for cellRow in self.dimensions:
            for cellColumn in self.dimensions:
                setattr(self, "{0}row{1}columnCell".format(cellRow, cellColumn), Cell())
        self.setCells()
    
    def setCells(self):
        limit, count = self.dimensionsInt, 0#ceil(self.dimensionsInt + self.dimensionsInt/2), 0
        while True:
            cellNumber = Utility.randomCell(self.dimensions); cellObject = getattr(self, cellNumber)
            if cellObject.type != "mine":
                if Utility.checkNearbyCells(self, cellNumber):
                    cellObject.setType("mine")
                    for cell in Utility.getNearbyCells(cellNumber):
                        if "0" not in cell:
                            cellUpdateObj = getattr(self, cell)
                            cellUpdateObj.increaseValue()
                    count += 1
            if count >= limit:
                break

    def draw(self):
        drawString = ""
        for cellRow in self.dimensions:
            for cellColumn in self.dimensions:
                drawString += " ||{0.icon}||".format(getattr(self, "{0}row{1}columnCell".format(cellRow, cellColumn)))
            drawString += "\n"
        return drawString

@client.event
async def on_message(message):
    if message.content.lower().startswith("!minesweeper"):
        dimensions = int(message.content[13:])
        board = Board(dimensions)
        string = board.draw()
        await client.send_message(message.channel, string)
