from django.shortcuts import render,redirect
import serial
from escpos.printer import Usb
# Create your views here.

def index(request):
    return render(request,'index.html')
def sucess(request):
    return render(request,'sucess.html')

def test1(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    bill_content = [
        "Your Store Name",
        "Address Line 1",
        "Address Line 2",
        "Phone: 1234567890",
        "--------------------------------",
        "Item             Price",
        "--------------------------------",
        "Item 1           $10.00",
        "Item 2           $20.00",
        "Item 3           $30.00",
        "--------------------------------",
        "Total            $60.00",
        "--------------------------------",
        "Thank you for shopping with us!",
    ]
    
    bill_string = "\n".join(bill_content)
    ser.write(bill_string.encode())
    ser.close()
    return redirect(sucess)


def test2(request):
    # Get the necessary data for the bill
    # Replace these with your actual data or retrieve it from the database
    customer_name = "John Doe"
    items = [
        {"name": "Item 1", "price": 10.99},
        {"name": "Item 2", "price": 5.99},
        {"name": "Item 3", "price": 7.99},
    ]
    total = sum(item['price'] for item in items)

    # Prepare the bill content
    bill_content = f"Customer Name: {customer_name}\n\n"
    bill_content += "Item\t\tPrice\n"
    for item in items:
        bill_content += f"{item['name']}\t\t${item['price']}\n"
    bill_content += f"\nTotal: ${total}\n"

    # Send the bill content to the thermal printer
    try:
        print('1')
        # Connect to the printer
        printer = Usb(0x04b8, 0x0e15)  # Replace with your printer's vendor and product IDs
        print('2')
        # Set the printer style
        printer.set(align='center', font='a', bold=True)

        # Print the bill content
        printer.text(bill_content)

        # Cut the paper
        printer.cut()

        # Close the printer connection
        printer.close()

        return render(request, 'sucess.html')
    except Exception as e:
        return render(request, 'index.html')


def test3(request):

    # Connect to the printer
    p = Usb(0x04b8, 0x0e03, 0, 0x81, 0x03)

    # Set font style (optional)
    p.set(font='a')

    # Print your name
    name = "John Doe"
    p.text("Name: {}\n".format(name))

    # Cut the paper (optional)
    p.cut()

    # Close the connection
    p.close()

    return redirect(sucess)