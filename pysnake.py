import pygame
import weakref
import random
from collections import deque
from engine.vector import Vector2
from engine.color import Color
from engine.screen import Screen
from engine.gameloop import GameLoop
from engine.entity import Entity
from engine.entity import EntitySpawner
from engine.components import RenderComponent
from engine.components import RectRenderComponent
from engine.components import TextRenderComponent
from engine.components import InputComponent
from engine.input import InputEvent
from engine.events import EventHook


DIRECTION_LEFT = Vector2(0, -1)
DIRECTION_RIGHT = Vector2(0, 1)
DIRECTION_UP = Vector2(-1, 0)
DIRECTION_DOWN = Vector2(1, 0)

CELL_SIZE = Vector2(20, 20)
CELL_BORDER_WIDTH = 2
CELL_TYPE_BLOCK = 1
CELL_TYPE_EMPTY = 0

CELL_MATRIX = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

CELL_MATRIX_2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class CellRenderComponent(RenderComponent):
    def __init__(self, surfaceSize, rectSize, borderWidth, fillColor, borderColor):
        RenderComponent.__init__(self, surfaceSize)
        self.rectSize = rectSize
        self.borderWidth = borderWidth
        self.fillColor = fillColor
        self.borderColor = borderColor

    def tick(self, deltaTime):
        pygame.draw.rect(self._surface, self.fillColor, (0, 0, self.rectSize.x, self.rectSize.y))
        pygame.draw.rect(self._surface, self.borderColor, (0, 0, self.rectSize.x, self.rectSize.y), self.borderWidth)
        Screen.getSurface().blit(
            self._surface,
            self.getEntity().getTransform().position + self.getEntity().getBoard().getTransform().position)


class CellEntity(Entity):
    def __init__(self, board, pos, type, priority=0, initialComponents=None):
        Entity.__init__(self, priority, initialComponents)
        self._board = weakref.ref(board)
        self._pos = pos
        self._type = type
        self.food = None

    def init(self):
        Entity.init(self)
        if (self._type == CELL_TYPE_EMPTY):
            self.addComponent(CellRenderComponent(CELL_SIZE, CELL_SIZE, CELL_BORDER_WIDTH, Color(25, 25, 25), Color.BLACK))
        if (self._type == CELL_TYPE_BLOCK):
            self.addComponent(CellRenderComponent(CELL_SIZE, CELL_SIZE, CELL_BORDER_WIDTH, Color.BLUE, Color.BLACK))

    def getBoard(self):
        return self._board()

    def getPos(self):
        return self._pos

    def getType(self):
        return self._type


class BoardEntity(Entity):
    def __init__(self, cellMatrix, priority=0, initialComponents=None):
        Entity.__init__(self, priority, initialComponents)
        self._cellMatrix = cellMatrix
        self._rows = len(self._cellMatrix)
        self._cols = len(self._cellMatrix[0])
        self._cells = list()

    def init(self):
        Entity.init(self)
        for row in range(self._rows):
            for col in range(self._cols):
                cellType = self._cellMatrix[row][col]
                cellEntity = EntitySpawner.spawnEntity(CellEntity, self, Vector2(row, col), cellType)
                cellEntity.getTransform().position = Vector2(col * CELL_SIZE.x, row * CELL_SIZE.y)
                self._cells.append(cellEntity)

    def getRows(self):
        return self._rows

    def getCols(self):
        return self._cols

    def getCell(self, row, col):
        return self._cells[self.getCellIndex_Internal(row, col)]

    def getCellIndex_Internal(self, row, col):
        return row * self._cols + col


class SnakeRenderComponent(RenderComponent):
    def __init__(self, surfaceSize, rectSize, borderWidth, bodyColor, borderColor):
        RenderComponent.__init__(self, surfaceSize)
        self.rectSize = rectSize
        self.borderWidth = borderWidth
        self.bodyColor = bodyColor
        self.borderColor = borderColor

    def tick(self, deltaTime):
        boardPos = self.getSnake().getBoard().getTransform().position
        self._surface.fill(Color.NONE)
        for pos in self.getSnake().getBodyPositions():
            rectPos = boardPos + Vector2(pos.y * self.rectSize.x, pos.x * self.rectSize.y)
            pygame.draw.rect(self._surface, self.bodyColor, (rectPos.x, rectPos.y, self.rectSize.x, self.rectSize.y))
            pygame.draw.rect(
                self._surface,
                self.borderColor,
                (rectPos.x, rectPos.y, self.rectSize.x, self.rectSize.y),
                self.borderWidth)

        Screen.getSurface().blit(self._surface, Vector2(0, 0))

    def getSnake(self):
        return self.getEntity()


class SnakeEntity(Entity):
    def __init__(self, board, speed, initialSize, initialHeadPos, initialDir, priority=0, initialComponents=None):
        Entity.__init__(self, priority, initialComponents)
        self._board = board
        self._headPos = initialHeadPos
        self._dir = initialDir
        self._deque = deque()
        for i in range(initialSize):
            self._deque.appendleft(initialHeadPos - initialDir * i)

        self._speed = speed
        self._passedDistance = 0.0
        self._dirQueue = deque()
        self._ateFood = False
        self.onFoodEaten = EventHook()

    def init(self):
        Entity.init(self)
        self._renderComponent = self.addComponent(
            SnakeRenderComponent(Screen.getSize(), CELL_SIZE, CELL_BORDER_WIDTH, Color.RED, Color.BLACK))

        self._inputComponent = self.addComponent(InputComponent())
        self._inputComponent.bindAction("left", InputEvent.EVENT_TYPE_PRESSED, lambda: self.changeDirection(DIRECTION_LEFT))
        self._inputComponent.bindAction("right", InputEvent.EVENT_TYPE_PRESSED, lambda: self.changeDirection(DIRECTION_RIGHT))
        self._inputComponent.bindAction("up", InputEvent.EVENT_TYPE_PRESSED, lambda: self.changeDirection(DIRECTION_UP))
        self._inputComponent.bindAction("down", InputEvent.EVENT_TYPE_PRESSED, lambda: self.changeDirection(DIRECTION_DOWN))

    def tick(self, deltaTime):
        Entity.tick(self, deltaTime)
        self._passedDistance += self._speed * deltaTime
        if (self._passedDistance > 1.0):
            self._passedDistance -= 1.0
            self.move_Internal()
            self.hangleCollisions_Internal()

    def getBoard(self):
        return self._board

    def getSpeed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def getHeadPos(self):
        return self._headPos

    def getNextHeadPos(self):
        return self._headPos + self._dir

    def getBodyPositions(self):
        return iter(self._deque)

    def changeDirection(self, newDir):
        length = len(self._dirQueue)
        if (length == 2):
            return

        lastQueueDir = self._dir
        if (length > 0):
            lastQueueDir = self._dirQueue[length - 1]
        if (newDir != lastQueueDir * -1.0):
            self._dirQueue.append(newDir)

    def move_Internal(self):
        if (self._ateFood):
            self._ateFood = False
        else:
            self._deque.popleft()

        if (len(self._dirQueue) > 0):
            self._dir = self._dirQueue.popleft()
        self._deque.append(self.getNextHeadPos())
        self._headPos = self.getNextHeadPos()

    def hangleCollisions_Internal(self):
        # Handle collision with block cells
        headCell = self._board.getCell(self._headPos.x, self._headPos.y)
        if (headCell.getType() == CELL_TYPE_BLOCK):
            EntitySpawner.destroyEntity(self)

        # Handle collision with itself
        bodyPositions = list(self.getBodyPositions())
        bodyPositions.remove(self._headPos)
        if (self._headPos in bodyPositions):
            EntitySpawner.destroyEntity(self)

        # Handle collision with food
        for cellPos in self.getBodyPositions():
            cell = self._board.getCell(cellPos.x, cellPos.y)
            if (cell.food is not None):
                self._ateFood = True
                food = cell.food
                cell.food = None
                EntitySpawner.destroyEntity(food)
                self.onFoodEaten.invoke()
                break

    def eatFood_Internal(self, cell, food):
        self._ateFood = True
        cell.food = None
        EntitySpawner.destroyEntity(food)
        self.onFoodEaten.invoke()


class FoodEntity(Entity):
    def __init__(self, board, pos, priority=0, initialComponents=None):
        Entity.__init__(self, priority, initialComponents)
        self._board = board
        self._pos = pos
        self.setPos(self._pos)
        self._board.getCell(self._pos.x, self._pos.y).food = self

    def init(self):
        Entity.init(self)
        self._renderComponent = self.addComponent(
            CellRenderComponent(CELL_SIZE, CELL_SIZE, CELL_BORDER_WIDTH, Color.GREEN, Color.BLACK))

    def getBoard(self):
        return self._board

    def getPos(self):
        return self._pos

    def setPos(self, pos):
        self._pos = pos
        self._transform.position = Vector2(pos.y * CELL_SIZE.x, pos.x * CELL_SIZE.y)


def spawnFood(board, snake):
    randRow = random.randrange(1, board.getRows() - 1)
    randCol = random.randrange(1, board.getCols() - 1)
    while (board.getCell(randRow, randCol).getType() == CELL_TYPE_BLOCK or
           Vector2(randRow, randCol) in snake.getBodyPositions()):
        randRow = random.randrange(1, board.getRows() - 1)
        randCol = random.randrange(1, board.getCols() - 1)

    EntitySpawner.spawnEntity(FoodEntity, board, Vector2(randRow, randCol))


def setSnakeSpeed(snake, speed):
    snake.speed = speed


def run():
    pygame.init()
    Screen.init(width=500, height=450, flags=0, depth=32)

    backgroundEntity = EntitySpawner.spawnEntity(Entity)
    backgroundEntity.addComponent(RectRenderComponent(Screen.getSize(), Screen.getSize(), Color.BLACK))

    boardEntity = EntitySpawner.spawnEntity(BoardEntity, CELL_MATRIX_2)

    snakeEntity = EntitySpawner.spawnEntity(SnakeEntity, boardEntity, 5, 3, Vector2(3, 3), DIRECTION_RIGHT)
    snakeEntity.onFoodEaten += lambda: spawnFood(boardEntity, snakeEntity)
    snakeEntity.onFoodEaten += lambda: snakeEntity.setSpeed(snakeEntity.getSpeed() + 0.1)
    spawnFood(boardEntity, snakeEntity)

    scoreEntity = EntitySpawner.spawnEntity(Entity)
    scoreEntity.getTransform().position = Vector2(0, boardEntity.getRows() * CELL_SIZE.y)
    scoreText = scoreEntity.addComponent(TextRenderComponent())
    scoreText.setFontName("mono")
    scoreText.setFontSize(20)
    scoreText.setBold(True)
    scoreText.setColor(Color.WHITE)
    scoreText.setText("SCORE:0")

    GameLoop(fps=60).run()
    pygame.quit()


if (__name__ == "__main__"):
    run()
