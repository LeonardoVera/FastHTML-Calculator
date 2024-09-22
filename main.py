from fasthtml.common import *
import re

app = FastHTML()

#Import htmx
htmxlink = Script(src="https://unpkg.com/htmx.org@1.6.1/dist/htmx.min.js")

result = ''
first = ''
second = ''

tailwind_css = Link(href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css', rel='stylesheet')

def head():
    return Head(
        Title("FastHTML-tailwind calculator"),
        tailwind_css,
    )

def numberButtons():
    buttons = [Button(9 - i, cls="p-4 bg-gray-500 text-white rounded-xl", hx_post=f"/clicked-{9-i}", hx_target='#result', hx_swap='innerHTML') for i in range(9)]
    return Div(*buttons, Button(0, id='number-0', hx_post='/clicked-0', hx_target='#result',hx_swap='innerHTML' ,cls='p-4 bg-gray-500 text-white rounded-xl col-span-3'),
               cls='numbers-container grid grid-cols-3 gap-4 col-span-3'
    )

def resultDisplay():
    return Div(result, cls='bg-gray-300 p-4 rounded-xl text-4xl text-right col-span-4', id='result')

def clearNEraseButtons():
    return Div(
        Button('C', cls='p-4 bg-red-500 text-white col-span-2 rounded-xl', hx_post='/clear', hx_target='#result', hx_swap='innerHTML'),
        Button('←', cls='p-4 bg-red-500 text-white col-span-1 rounded-xl', hx_post='/erase', hx_target='#result', hx_swap='innerHTML'),
        cls='grid grid-cols-3 gap-4 col-span-3'
    )
    
def operationButtons():
    return Div(
        Button('+', cls='p-4 bg-blue-500 text-white rounded-xl', hx_post='/click-+', hx_target='#result', hx_swap='innerHTML'),
        Button('-', cls='p-4 bg-blue-500 text-white rounded-xl' ,hx_post='/click--', hx_target='#result', hx_swap='innerHTML'),
        Button('x', cls='p-4 bg-blue-500 text-white rounded-xl' ,hx_post='/click-x', hx_target='#result', hx_swap='innerHTML'),
        Button('/', cls='p-4 bg-blue-500 text-white rounded-xl' ,hx_post='/click-/', hx_target='#result', hx_swap='innerHTML'),
        Button('=', cls='p-4 bg-blue-500 text-white rounded-xl' ,hx_post='/click-=', hx_target='#result', hx_swap='innerHTML'),
        cls='grid gap-4'
    )

def numbersNEraseLayout():
    return Div(
        clearNEraseButtons(),
        numberButtons(),
        cls='grid col-span-3 gap-4'
    )

def calculatorLayout():
    return Div(
        resultDisplay(),
        numbersNEraseLayout(),
        operationButtons(),
        cls='container bg-gray-400 grid grid-cols-4 gap-4 p-4 max-w-2xl mx-auto border-4 border-gray-500 rounded-xl'
    )

@app.get('/')
def home():
    return Html(
        head(),
        Body(
            Main(
                calculatorLayout()
            ),
            htmxlink,
            cls='bg-gray-900 h-screen flex justify-center items-center'
        )
    )

@app.post('/clicked-{number}')
def clicked(number: str):
    global result
    result += number
    return result

@app.post('/clear')
def clickedC():
    global result
    result = ''
    return result

@app.post('/erase')
def clickedErase():
    global result
    result = result[:-1]
    return result

@app.post('/click-+')
def clickedPlus():
    global result
    result += '+'
    return result

@app.post('/click--')
def clickedMinus():
    global result
    result += '-'
    return result

@app.post('/click-x')
def clickedMultiply():
    global result
    result += '*'
    return result

@app.post('/click-/')
def clickedDivide():
    global result
    result += '/'
    return result

@app.post('/click-=')
def clickedEqual():
    global result
    global first
    global second
    match = re.match(r'(\d+)([\+\-\*/])(\d+)', result)

    if match:
        first = int(match.group(1))
        operator = match.group(2)
        second = int(match.group(3))

        if operator == '+':
            result = first + second
        elif operator == '-':
            result = first - second
        elif operator == '*':
            result = first * second
        elif operator == '/':
            try:
                result = first / second
            except ZeroDivisionError:
                result = 'Invalid division by zero'
    else:
        result = 'Invalid operator'
            

    result = str(result)
    return result

serve()
