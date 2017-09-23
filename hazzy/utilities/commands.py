#!/usr/bin/env python

import linuxcnc

# Setup logging
from utilities import logger
log = logger.get(__name__)

stat = linuxcnc.stat()
command = linuxcnc.command()

def estop():
    set_state(linuxcnc.STATE_ESTOP)

def estop_reset():
    set_state(linuxcnc.STATE_ESTOP_RESET)

def machine_off():
    set_state(linuxcnc.STATE_OFF)

def machine_on():
    set_state(linuxcnc.STATE_ON)

def mist_on():
    command.mist(1)

def mist_off():
    command.mist(0)

def flood_on():
    command.flood(1)

def flood_off():
    command.flood(0)

def set_mode(mode):
    stat.poll()
    if stat.task_mode == mode:
        return
    command.mode(mode)
    command.wait_complete()

def set_state(state):
    stat.poll()
    if stat.state == state:
        return
    command.state(state)
    command.wait_complete()

def set_motion_mode(mode):
    stat.poll()
    if stat.motion_mode == mode:
        return
    command.teleop_enable(0)
    command.traj_mode(mode)
    command.wait_complete()

def issue_mdi(mdi_command):
    log.info("Issuing MDI command: {}".format(mdi_command))
    command.mdi(mdi_command)

def set_work_offset(axis, value):
    offset_command = 'G10 L20 P%d %s%.12f' % (stat.g5x_index, axis, value)
    issue_mdi(offset_command)
    set_mode(linuxcnc.MODE_MANUAL)

def home_joint(joint):
    set_mode(linuxcnc.MODE_MANUAL)
    if stat.joint[joint]['homed'] == 0 and not stat.estop and stat.joint[joint]['homing'] == 0:
        log.info("Homing joint {0}".format(joint))
        command.home(joint)
    elif stat.homed[joint]:
        log.info("joint {0} is already homed, unhoming".format(joint))
        set_motion_mode(linuxcnc.TRAJ_MODE_FREE)
        command.unhome(joint)
    elif stat.joint[joint]['homing'] != 0:
        log.error("Homing sequence already in progress")
    else:
        log.error("Can't home joint {0}, check E-stop and machine power".format(joint))

def is_moving():
    '''Check if machine is moving due to MDI, program execution, etc.'''
    if stat.state == linuxcnc.RCS_EXEC:
        return True
    else:
        return stat.task_mode == linuxcnc.MODE_AUTO \
            and stat.interp_state != linuxcnc.INTERP_IDLE
