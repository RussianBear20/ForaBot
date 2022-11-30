import subprocess
import time

class LimitedServo():
    def __init__(self, motor_idx, position_dict):
        self.position_dict = position_dict
        self.motor_idx = motor_idx

    def turnTo(self, location_name):
        try:
            # Multiple of 4 because Maestro Control Center is us and UscCmd is 1/4 us
            self.usccmd('--servo', '{},{}'.format(self.motor_idx,4*self.position_dict[location_name]))
        except:
            raise Exception("Location Name: {} is not a known position for servo {}".format(location_name, self.motor_idx))
        self.waitComplete(location_name)

    @staticmethod
    def usccmd(*args):
        return subprocess.check_output(['UscCmd'] + list(args))

    def waitComplete(self, location_name):
      is_complete = False
      num_checks = 0
      us_position = self.position_dict[location_name] * 4
      while not is_complete:
          if num_checks > 100:
              raise Exception('Servo status check not complete: {} did not move to {}'.format(self.motor_idx, location_name))
          status_b = self.usccmd('--status')
          status = str(status_b)
          rows = status.split('\\n')
          target_speed_accel_pos = rows[self.motor_idx+1].split()
          is_complete = int(target_speed_accel_pos[4]) == us_position
          num_checks += 1
          time.sleep(0.01)
