import pytest
import ayab_communication


class DummySerial(object):
  pass


class TestCommunication():

  @pytest.fixture
  def ayab_communication():
    dummy_serial = DummySerial()
    ayab_communication_dummy = ayab_communication.AyabCommunication(dummy_serial)
    return ayab_communication_dummy

  def test_read_line(ayab_comm):
    print "LOLCAT"
    print type(ayab_comm)
    assert 0
