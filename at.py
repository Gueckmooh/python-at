import warnings
import subprocess
import os

executable = "/usr/bin/at"

def str_to_bytes (sb):
  if isinstance (sb, bytes):
    return sb
  return str.encode (sb)

class at (object):
  def __init__ (self, date="now", _executable=None):
    if not _executable is None:
      self.executable = _executable
    else:
      self.executable = executable
    self.date = date
    self.running = False

  def start (self):
    command = [self.executable, self.date]
    if self.running:
      warn.warnings ("At instance is already in use", Warning)
      return
    with open (os.devnull, "w") as devnull:
      self._process = subprocess.Popen (
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr = devnull
      )
    self.running = True

  def terminate (self):
    if not self.running:
      return
    self._process.communicate ()
    del self._process
    self.running = False

  def __enter__ (self):
    self.start ()
    return self

  def __exit__ (self, exc_type, exc_val, exc_tb):
    self.terminate ()

  def __del__ (self):
    self.terminate ()

  def add_command (self, *commands):
    if not self.running:
      raise ValueError ("At not running")
    for c in commands:
      command = str_to_bytes ("{}\n".format (c))
      self._process.stdin.write (command)
      self._process.stdin.flush ()
