#
# Demo code to control multio board
# A 128bit I/O expander using up to eight MCP23017 devices
#
# This package uses ports number 0-15 to address each port
# It translates that to internal I2C addresses and registers
#
# No copyright G.J. van Loo
# Fen Logic Ltd.
#
#

import smbus
import sys
import time

bus = smbus.SMBus(1) # /dev/i2c-1

#
# MCP23017 definitions
#

M17_IODIRA   = 0x00 # 1=input   0=output  RST=0xFF
M17_IODIRB   = 0x01 #
M17_IPOLA    = 0x02 # 1=invert  0=true    RST=0x00
M17_IPOLB    = 0x03 #
M17_IRQENA   = 0x04 # IRQ on change 1=enabled RST=0x00
M17_IRQENB   = 0x05 #
M17_IRQPREVA = 0x06 # Prev 'IRQ' state
M17_IRQPREVB = 0x07 #
M17_INTCNTA  = 0x08 # IRQ compare 1=prev, 0=pin
M17_INTCNTB  = 0x09 #
M17_IOCON    = 0x0A #
#M17_IOCON   = 0x0B # repeat of previous
M17_GPPUA    = 0x0C # 1 = pull up enabled  RST=0x00
M17_GPPUB    = 0x0D #
M17_INTFA    = 0x0E # Interrupt flag (Read only) RST=0x00
M17_INTFB    = 0x0F #
M17_INTCAPA  = 0x10 # IRQ capture (Read only) RST=0x??
M17_INTCAPB  = 0x11 #
M17_GPIOA    = 0x12 # Read=port status, write=Output latch
M17_GPIOB    = 0x13 #
M17_OLATA    = 0x14 # Output latch
M17_OLATB    = 0x15 #

# M17_IOCON I/O control register bits
M17_IC_BANK    = 0x80 # 1=banked 0=seq addresses
M17_IC_MIRROR  = 0x40 # 1=IRQs connected
M17_IC_SEQOP   = 0x20 # 1=seq operation 0=normal addressing
M17_IC_SLEWDIS = 0x10 # 1=SDA slewrate disabled
M17_IC_HAEN    = 0x08 # <Not functional on I2C>
M17_IC_ODR     = 0x04 # IRQ opendrain
M17_IC_INTPOL  = 0x02 # 1=IRQ acive high 0=IRQ active low

# Set up a port as input/output
# port is number 0-15
# Bit mask: 1 = input, 0 = output
def set_port_input(port,input_bits):
   i2c_adrs = 0x20+(port>>1)
   reg_adrs = M17_IODIRA + (port & 0x01)
   bus.write_byte_data(i2c_adrs,reg_adrs,input_bits)

# Write byte to port
def write_port(port,data):
   i2c_adrs = 0x20+(port>>1)
   reg_adrs = M17_OLATA + (port & 0x01)
   bus.write_byte_data(i2c_adrs,reg_adrs,data)

# read byte from port
def read_port(port):
   i2c_adrs = 0x20+(port>>1)
   reg_adrs = M17_GPIOA + (port & 0x01)
   return bus.read_byte_data(i2c_adrs,reg_adrs)

#
# MAIN
#

# Set all ports to output mode
for port in range(0,16):
  set_port_input(port,0x00)

# have to step through ports 0,1,4,5,8,9...2,3,6,7,10,11
#                 
port1_cw = [ 0,1,4,5,8,9,12,13]
port2_cw = [ 2,3,6,7,10,11,14,15]

while True:
  for port in range (0,8):
    for bit in range (0,8):
      write_port(port1_cw[port],1<<bit)
      time.sleep(0.01)
    write_port(port1_cw[port],0)
  for port in range (7,-1,-1):
    for bit in range (0,8):
      write_port(port2_cw[port],1<<bit)
      time.sleep(0.01)
    write_port(port2_cw[port],0)



