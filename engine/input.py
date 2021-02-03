import pygame
import json
import os
import engine.math
from engine.events import EventHook


KEY_NAMES_BY_KEY_CODE = {
    pygame.K_BACKSPACE: "K_BACKSPACE",
    pygame.K_TAB: "K_TAB",
    pygame.K_CLEAR: "K_CLEAR",
    pygame.K_RETURN: "K_RETURN",
    pygame.K_PAUSE: "K_PAUSE",
    pygame.K_ESCAPE: "K_ESCAPE",
    pygame.K_SPACE: "K_SPACE",
    pygame.K_EXCLAIM: "K_EXCLAIM",
    pygame.K_QUOTEDBL: "K_QUOTEDBL",
    pygame.K_HASH: "K_HASH",
    pygame.K_DOLLAR: "K_DOLLAR",
    pygame.K_AMPERSAND: "K_AMPERSAND",
    pygame.K_QUOTE: "K_QUOTE",
    pygame.K_LEFTPAREN: "K_LEFTPAREN",
    pygame.K_RIGHTPAREN: "K_RIGHTPAREN",
    pygame.K_ASTERISK: "K_ASTERISK",
    pygame.K_PLUS: "K_PLUS",
    pygame.K_COMMA: "K_COMMA",
    pygame.K_MINUS: "K_MINUS",
    pygame.K_PERIOD: "K_PERIOD",
    pygame.K_SLASH: "K_SLASH",
    pygame.K_0: "K_0",
    pygame.K_1: "K_1",
    pygame.K_2: "K_2",
    pygame.K_3: "K_3",
    pygame.K_4: "K_4",
    pygame.K_5: "K_5",
    pygame.K_6: "K_6",
    pygame.K_7: "K_7",
    pygame.K_8: "K_8",
    pygame.K_9: "K_9",
    pygame.K_COLON: "K_COLON",
    pygame.K_SEMICOLON: "K_SEMICOLON",
    pygame.K_LESS: "K_LESS",
    pygame.K_EQUALS: "K_EQUALS",
    pygame.K_GREATER: "K_GREATER",
    pygame.K_QUESTION: "K_QUESTION",
    pygame.K_AT: "K_AT",
    pygame.K_LEFTBRACKET: "K_LEFTBRACKET",
    pygame.K_BACKSLASH: "K_BACKSLASH",
    pygame.K_RIGHTBRACKET: "K_RIGHTBRACKET",
    pygame.K_CARET: "K_CARET",
    pygame.K_UNDERSCORE: "K_UNDERSCORE",
    pygame.K_BACKQUOTE: "K_BACKQUOTE",
    pygame.K_a: "K_a",
    pygame.K_b: "K_b",
    pygame.K_c: "K_c",
    pygame.K_d: "K_d",
    pygame.K_e: "K_e",
    pygame.K_f: "K_f",
    pygame.K_g: "K_g",
    pygame.K_h: "K_h",
    pygame.K_i: "K_i",
    pygame.K_j: "K_j",
    pygame.K_k: "K_k",
    pygame.K_l: "K_l",
    pygame.K_m: "K_m",
    pygame.K_n: "K_n",
    pygame.K_o: "K_o",
    pygame.K_p: "K_p",
    pygame.K_q: "K_q",
    pygame.K_r: "K_r",
    pygame.K_s: "K_s",
    pygame.K_t: "K_t",
    pygame.K_u: "K_u",
    pygame.K_v: "K_v",
    pygame.K_w: "K_w",
    pygame.K_x: "K_x",
    pygame.K_y: "K_y",
    pygame.K_z: "K_z",
    pygame.K_DELETE: "K_DELETE",
    pygame.K_KP0: "K_KP0",
    pygame.K_KP1: "K_KP1",
    pygame.K_KP2: "K_KP2",
    pygame.K_KP3: "K_KP3",
    pygame.K_KP4: "K_KP4",
    pygame.K_KP5: "K_KP5",
    pygame.K_KP6: "K_KP6",
    pygame.K_KP7: "K_KP7",
    pygame.K_KP8: "K_KP8",
    pygame.K_KP9: "K_KP9",
    pygame.K_KP_PERIOD: "K_KP_PERIOD",
    pygame.K_KP_DIVIDE: "K_KP_DIVIDE",
    pygame.K_KP_MULTIPLY: "K_KP_MULTIPLY",
    pygame.K_KP_MINUS: "K_KP_MINUS",
    pygame.K_KP_PLUS: "K_KP_PLUS",
    pygame.K_KP_ENTER: "K_KP_ENTER",
    pygame.K_KP_EQUALS: "K_KP_EQUALS",
    pygame.K_UP: "K_UP",
    pygame.K_DOWN: "K_DOWN",
    pygame.K_RIGHT: "K_RIGHT",
    pygame.K_LEFT: "K_LEFT",
    pygame.K_INSERT: "K_INSERT",
    pygame.K_HOME: "K_HOME",
    pygame.K_END: "K_END",
    pygame.K_PAGEUP: "K_PAGEUP",
    pygame.K_PAGEDOWN: "K_PAGEDOWN",
    pygame.K_F1: "K_F1",
    pygame.K_F2: "K_F2",
    pygame.K_F3: "K_F3",
    pygame.K_F4: "K_F4",
    pygame.K_F5: "K_F5",
    pygame.K_F6: "K_F6",
    pygame.K_F7: "K_F7",
    pygame.K_F8: "K_F8",
    pygame.K_F9: "K_F9",
    pygame.K_F10: "K_F10",
    pygame.K_F11: "K_F11",
    pygame.K_F12: "K_F12",
    pygame.K_F13: "K_F13",
    pygame.K_F14: "K_F14",
    pygame.K_F15: "K_F15",
    pygame.K_NUMLOCK: "K_NUMLOCK",
    pygame.K_CAPSLOCK: "K_CAPSLOCK",
    pygame.K_SCROLLOCK: "K_SCROLLOCK",
    pygame.K_RSHIFT: "K_RSHIFT",
    pygame.K_LSHIFT: "K_LSHIFT",
    pygame.K_RCTRL: "K_RCTRL",
    pygame.K_LCTRL: "K_LCTRL",
    pygame.K_RALT: "K_RALT",
    pygame.K_LALT: "K_LALT",
    pygame.K_RMETA: "K_RMETA",
    pygame.K_LMETA: "K_LMETA",
    pygame.K_LSUPER: "K_LSUPER",
    pygame.K_RSUPER: "K_RSUPER",
    pygame.K_MODE: "K_MODE",
    pygame.K_HELP: "K_HELP",
    pygame.K_PRINT: "K_PRINT",
    pygame.K_SYSREQ: "K_SYSREQ",
    pygame.K_BREAK: "K_BREAK",
    pygame.K_MENU: "K_MENU",
    pygame.K_POWER: "K_POWER",
    pygame.K_EURO: "K_EURO"
}


def getInputSettings_Internal():
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = "{0}/{1}".format(dirPath, "InputSettings.json")
    with open(filePath, "r") as fileStream:
        return json.load(fileStream)


def createAxisValues_Internal():
    axisValues = dict()
    axisMappings = getInputSettings_Internal()["axisMappings"]
    for axis in axisMappings:
        axisValues[axis] = 0.0
    return axisValues


class InputEvent:
    EVENT_TYPE_PRESSED = 0
    EVENT_TYPE_RELEASED = 1
    EVENT_TYPE_AXIS = 2

    def __init__(self, name: str, type: int, axisValue: float = 0):
        self.name = name
        self.type = type
        self.axisValue = axisValue

    def __str__(self):
        return "[InputEvent: name={0} | type={1} | axisValue={2:.2f}]".format(self.name, self.type, self.axisValue)


class Input:
    onInputEvent = EventHook()

    _inputSettings = getInputSettings_Internal()
    _axisValues = createAxisValues_Internal()
    _pressedKeysThisFrame = set()
    _pressedKeysLastFrame = set()

    @staticmethod
    def getInputSettings():
        return Input._inputSettings

    @staticmethod
    def getActionMappings():
        inputSettings = Input.getInputSettings()
        actionMappings = inputSettings["actionMappings"]
        return actionMappings

    @staticmethod
    def getAxisMappings():
        inputSettings = Input.getInputSettings()
        axisMappings = inputSettings["axisMappings"]
        return axisMappings

    @staticmethod
    def tick_Internal(deltaTime):
        Input.cachePressedKeysFromLastFrame_Internal()
        Input.updatePressedKeysThisFrame_Internal()

        # Dispatch action events
        actionMappings = Input.getActionMappings()
        for action, keys in actionMappings.items():
            for key in keys:
                if ((key in Input._pressedKeysThisFrame) and not (key in Input._pressedKeysLastFrame)):
                    Input.onInputEvent.invoke(InputEvent(action, InputEvent.EVENT_TYPE_PRESSED))
                elif ((key in Input._pressedKeysLastFrame) and not (key in Input._pressedKeysThisFrame)):
                    Input.onInputEvent.invoke(InputEvent(action, InputEvent.EVENT_TYPE_RELEASED))

        # Update axis values
        axisMappings = Input.getAxisMappings()
        for axis, axisSettings in axisMappings.items():
            axisAcceleration = axisSettings["acceleration"]
            axisDeceleration = axisSettings["deceleration"]
            axisPositiveKeys = axisSettings["positive"]
            axisNegativeKeys = axisSettings["negative"]

            anyPositiveKey = False
            for posKey in axisPositiveKeys:
                if (posKey in Input._pressedKeysThisFrame):
                    anyPositiveKey = True
                    break

            anyNegativeKey = False
            for negKey in axisNegativeKeys:
                if (negKey in Input._pressedKeysThisFrame):
                    anyNegativeKey = True
                    break

            axisValue = Input._axisValues[axis]
            if ((anyPositiveKey and anyNegativeKey) or (not (anyPositiveKey or anyNegativeKey))):
                if (axisValue < 0.0):
                    axisValue = engine.math.clamp(axisValue + axisDeceleration * deltaTime, -1.0, 0.0)
                elif(axisValue > 0.0):
                    axisValue = engine.math.clamp(axisValue - axisDeceleration * deltaTime, 0.0, 1.0)
            elif (anyPositiveKey and not anyNegativeKey):
                axisValue = engine.math.clamp(axisValue + axisAcceleration * deltaTime, -1.0, 1.0)
            elif(anyNegativeKey and not anyPositiveKey):
                axisValue = engine.math.clamp(axisValue - axisAcceleration * deltaTime, -1.0, 1.0)

            Input._axisValues[axis] = axisValue
            Input.onInputEvent.invoke(InputEvent(axis, InputEvent.EVENT_TYPE_AXIS, axisValue))

    @staticmethod
    def cachePressedKeysFromLastFrame_Internal():
        Input._pressedKeysLastFrame.clear()
        for key in Input._pressedKeysThisFrame:
            Input._pressedKeysLastFrame.add(key)

    @staticmethod
    def updatePressedKeysThisFrame_Internal():
        Input._pressedKeysThisFrame.clear()
        pressedKeyFlags = pygame.key.get_pressed()
        for keyCode, keyName in KEY_NAMES_BY_KEY_CODE.items():
            if (pressedKeyFlags[keyCode]):
                Input._pressedKeysThisFrame.add(keyName)
