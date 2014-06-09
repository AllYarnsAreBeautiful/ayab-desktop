import pytest
import serial
import unittest
from ayab.ayab_communication import AyabCommunication


class TestCommunication(unittest.TestCase):

  def setUp(self):
    self.dummy_serial = serial.serial_for_url("loop://logging=debug")
    self.comm_dummy = AyabCommunication(self.dummy_serial)

  def test_read_line(self):
    self.comm_dummy.read_line()

  def test_req_start(self):
    start_val, end_val = 0, 10
    self.comm_dummy.req_start(start_val, end_val)
    byte_array = bytearray([0x01, start_val, end_val, 0x0a, 0x0d])
    bytes_read = self.dummy_serial.read(len(byte_array))
    self.assertEqual(bytes_read, byte_array)
