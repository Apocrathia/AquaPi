#!/usr/bin/env python

#
#    build_arduino.py - build, link and upload sketches script for Arduino
#    Copyright (c) 2010 Ben Sasson.  All right reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import sys
import os
import optparse


EXITCODE_OK = 0
EXITCODE_NO_UPLOAD_DEVICE = 1
EXITCODE_NO_WPROGRAM = 2
EXITCODE_INVALID_AVR_PATH = 3


CPU_CLOCK = 16000000
ARCH = 'atmega328p'
ENV_VERSION = 18
BAUD = 57600
CORE = 'arduino'


COMPILERS = {
    '.c': 'avr-gcc',
    '.cpp': 'avr-g++',
}


def _exec(cmdline, debug=True, valid_exitcode=0, simulate=False):
    if debug or simulate:
        print(cmdline)
    if not simulate:
        exitcode = os.system(cmdline)
        if exitcode != valid_exitcode:
            print('-'*20 + ' exitcode %d ' % exitcode + '-'*20)
            sys.exit(exitcode)


def compile_source(source, avr_path='', target_dir=None, arch=ARCH, clock=CPU_CLOCK, include_dirs=[], verbose=False, simulate=False):
    """
    compile a single source file, using compiler selected based on file extension and translating arguments
    to valid compiler flags.
    """

    filename, ext = os.path.splitext(source)
    compiler = COMPILERS.get(ext, None)
    if compiler is None:
        print(source, 'has no known compiler')
        return

    if target_dir is None:
        target_dir = os.path.dirname(source)

    target = os.path.join(target_dir, os.path.basename(source) + '.o')
    env = dict(source=source, target=target, arch=arch, clock=clock, env_version=ENV_VERSION, compiler=compiler, avr_path=avr_path)

    # create include list, don't use set() because order matters
    dirs = [os.path.dirname(source)]
    for d in include_dirs:
        if d not in dirs:
            dirs.append(d)

    env['include_dirs'] = ' '.join('-I%s' % d for d in dirs)
    if verbose:
        env['verbose'] = '-v'
    else:
        env['verbose'] = ''
    cmdline = '%(avr_path)s%(compiler)s -c %(verbose)s -g -Os -w -ffunction-sections -fdata-sections -mmcu=%(arch)s -DF_CPU=%(clock)dL -DARDUINO=%(env_version)d %(include_dirs)s %(source)s -o%(target)s' % env
    _exec(cmdline, simulate=simulate)
    return target


def compile_directory(directory, target_dir=None, include_dirs=[], avr_path='', arch=ARCH, clock=CPU_CLOCK, verbose=False, simulate=False):
    """
    compile all source files in a given directory, return a list of all .obj files created
    """

    obj_files = []
    for fname in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, fname)):
            obj_files.append(compile_source(os.path.join(directory, fname), include_dirs=include_dirs, avr_path=avr_path, target_dir=target_dir, arch=arch, clock=clock, verbose=verbose, simulate=simulate))

    return filter(lambda o: o, obj_files)


def append_to_archive(obj_file, archive, avr_path='', verbose=False, simulate=False):
    """
    create an .a archive out of .obj files
    """

    env = dict(obj_file=obj_file, archive=archive, avr_path=avr_path)
    if verbose:
        env['verbose'] = 'v'
    else:
        env['verbose'] = ''
    cmdline = '%(avr_path)savr-ar rcs%(verbose)s %(archive)s %(obj_file)s' % env
    _exec(cmdline, simulate=simulate)


def link(target, files, arch=ARCH, avr_path='', verbose=False, simulate=False):
    """
    link .obj files to a single .elf file
    """

    env = dict(target=target, files=' '.join(files), link_dir=os.path.dirname(target), arch=arch, avr_path=avr_path)
    if verbose:
        env['verbose'] = '-v'
    else:
        env['verbose'] = ''
    cmdline = '%(avr_path)savr-gcc %(verbose)s -Os -Wl,--gc-sections -mmcu=%(arch)s -o %(target)s %(files)s -L%(link_dir)s -lm' % env
    _exec(cmdline, simulate=simulate)


def make_hex(elf, avr_path='', verbose=False, simulate=False):
    """
    slice elf to .hex (program) end .eep (EEProm) files
    """

    eeprom_section = os.path.splitext(elf)[0] + '.epp'
    hex_section = os.path.splitext(elf)[0] + '.hex'
    env = dict(elf=elf, eeprom_section=eeprom_section, hex_section=hex_section, avr_path=avr_path)
    if verbose:
        env['verbose'] = '-v'
    else:
        env['verbose'] = ''
    cmdline_make_eeprom = '%(avr_path)savr-objcopy %(verbose)s -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 %(elf)s %(eeprom_section)s' % env
    _exec(cmdline_make_eeprom, simulate=simulate)
    cmdline_make_hex = '%(avr_path)savr-objcopy %(verbose)s -O ihex -R .eeprom %(elf)s %(hex_section)s' % env
    _exec(cmdline_make_hex, simulate=simulate)
    return hex_section, eeprom_section


def upload(hex_section, dev, avr_path='', dude_conf=None, arch=ARCH, core=CORE, baud=BAUD, verbose=False, simulate=False):
    """
    Upload .hex file to arduino board
    """

    env = dict(hex_section=hex_section, dev=dev, arch=arch, core=core, baud=baud, avr_path=avr_path)
    if verbose:
        env['verbose'] = '-v'
    else:
        env['verbose'] = ''
    if dude_conf is not None:
        env['dude_conf'] = '-C' + dude_conf
    else:
        env['dude_conf'] = ''
    cmdline = '%(avr_path)savrdude %(verbose)s %(dude_conf)s -p%(arch)s -c%(core)s -P%(dev)s -b%(baud)d -D -Uflash:w:%(hex_section)s:i' % env
    _exec(cmdline, simulate=simulate)


def main(argv):
    parser = optparse.OptionParser()
    parser.add_option('-d', '--directory', dest='directory', default='.', help='project directory')
    parser.add_option('-v', '--verbose', dest='verbose', default=False, action='store_true', help='be verbose')
    parser.add_option('--only-build', dest='only_build', default=False, action='store_true', help="only build, don't upload")
    parser.add_option('-u', '--upload-device', dest='upload_device', metavar='DEVICE', help='use DEVICE to upload code')
    parser.add_option('-i', '--include', dest='include_dirs', default=[], action='append', metavar='DIRECTORY', help='append DIRECTORY to include list')
    parser.add_option('-l', '--libraries', dest='libraries', default=[], action='append', metavar='DIRECTORY', help='append DIRECTORY to libraries search & build path')
    parser.add_option('-W', '--WProgram-dir', dest='wprogram_directory', metavar='DIRECTORY', help='DIRECTORY of Arduino.h and the rest of core files')
    parser.add_option('--avr-path', dest='avr_path', metavar='DIRECTORY', help='DIRECTORY where avr* programs located, if not specified - will assume found in default search path')
    parser.add_option('--dude-conf', dest='dude_conf', default=None, metavar='FILE', help='avrdude conf file, if not specified - will assume found in default location')
    parser.add_option('--simulate', dest='simulate', default=False, action='store_true', help='only simulate commands')
    parser.add_option('--core', dest='core', default=CORE, help='device core name [%s]' % CORE)
    parser.add_option('--arch', dest='arch', default=ARCH, help='device architecture name [%s]' % ARCH)
    parser.add_option('--baud', dest='baud', default=BAUD, type='int', help='upload baud rate [%d]' % BAUD)
    parser.add_option('--cpu-clock', dest='cpu_clock', default=CPU_CLOCK, metavar='Hz', action='store', type='int', help='target device CPU clock [%d]' % CPU_CLOCK)

    options, args = parser.parse_args(argv)

    if options.wprogram_directory is None or not os.path.exists(options.wprogram_directory) or not os.path.isdir(options.wprogram_directory):
        if options.verbose:
            print('WProgram directory was not specified or does not exist [%s]' % options.wprogram_directory)
        sys.exit(EXITCODE_NO_WPROGRAM)

    core_files = options.wprogram_directory

    if options.avr_path is not None:
        if not os.path.exists(options.avr_path) or not os.path.isdir(options.avr_path):
            if options.verbose:
                print('avr-path was specified but does not exist or not a directory [%s]' % options.avr_path)
            sys.exit(EXITCODE_INVALID_AVR_PATH)
        avr_path = os.path.join(options.avr_path, '')
    else:
        avr_path = ''

    # create build directory to store the compilation output files
    build_directory = os.path.join(options.directory, '_build')
    if not os.path.exists(build_directory):
        os.makedirs(build_directory)

    # compile arduino core files
    core_obj_files = compile_directory(core_files, build_directory, include_dirs=[core_files], avr_path=avr_path, arch=options.arch, clock=options.cpu_clock, verbose=options.verbose, simulate=options.simulate)

    # compile directories passed to program
    libraries_obj_files = []
    for library in options.libraries:
        libraries_obj_files.extend(compile_directory(library, build_directory, include_dirs=options.libraries + [core_files], avr_path=avr_path, arch=options.arch, clock=options.cpu_clock, verbose=options.verbose, simulate=options.simulate))

    # compile project
    project_obj_files = compile_directory(options.directory, build_directory, include_dirs=(options.include_dirs + options.libraries + [core_files]), avr_path=avr_path, arch=options.arch, clock=options.cpu_clock, verbose=options.verbose, simulate=options.simulate)

    # link project, libraries and core .obj files to a single .elf
    link_output = os.path.join(build_directory, os.path.basename(options.directory) + '.elf')
    link(link_output, project_obj_files + libraries_obj_files + core_obj_files, avr_path=avr_path, verbose=options.verbose, simulate=options.simulate)

    hex_section, eeprom_section = make_hex(link_output, avr_path=avr_path, verbose=options.verbose, simulate=options.simulate)

    # upload .hex file to arduino if needed
    if not options.only_build:
        if options.upload_device is None:
            if options.verbose:
                print('no upload device selected')
            sys.exit(EXITCODE_NO_UPLOAD_DEVICE)
        upload(hex_section, dev=options.upload_device, dude_conf=options.dude_conf, avr_path=avr_path, arch=options.arch, core=options.core, baud=options.baud, verbose=options.verbose, simulate=options.simulate)


if __name__ == '__main__':
    main(sys.argv)
