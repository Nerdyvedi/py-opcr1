# py-opcR1

Python library for operating the Alphasense OPC-R1 Optical Particle Counter using a Raspberry Pi (or other linux device). 


## Dependencies

One of the following, depending on whether you use GPIO pins or a SPI-USB adapter:

  1. [`py-spidev`](https://github.com/doceme/py-spidev) - for those using GPIO pins
  1. [`pyusbiss`](https://github.com/dancingquanta/pyusbiss) - for those using a SPI-USB adapter (python3+ only)



## Working


If you are using the SPI-USB adapter only, you will also need to install `pyusbiss`. This can be done as follows:

    $ pip install pyusbiss

Depending on your python setup, you may need to use `pip3` instead of `pip` to install for python3+:

    $ pip3 install pyusbiss

If you are using the GPIO pins to communicate with the OPC-R2, you must download the requirement `py-spidev` as follows:

    $ pip install git+https://github.com/doceme/py-spidev.git
    
Run the file "opc_r1_example.py" . Assign the required value of the port in the code.

    $ python opc_r1_example.py


## License

  This library is licensed under the MIT license. The full text of the license can be found in this repository at LICENSE.txt.




