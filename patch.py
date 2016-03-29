#!/usr/bin/env python

import argparse
import subprocess
import sys
import os

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Patch ShareLatex Community Edition to enable Japanese document (latex to platex).')
    parser.add_argument('--dir', default='/var/www/sharelatex', help='ShareLatex installed directory.')
    parser.add_argument('--tex', default='/usr/bin', help='LaTeX commands installed directory.')
    parser.add_argument('--pdfjsver', default='1.0.1040', help='PDF.js version. See ./web/public/js/libs')
    parser.add_argument('--unpatch', action='store_true', help='Restore to the original files.')
    parser.add_argument('--compile', action='store_true', help='Compile after patch (un)installed.')
    parser.add_argument('--verbose', action='store_true', help='Print all status.')
    parser.add_argument('--simulation', action='store_true', help='Simulation mode. (Does not copy files)')
    
    args = parser.parse_args()
    
    # Check if sudo
    if (not args.simulation) and os.geteuid() != 0:
        print "You need to have root privileges. Run for example, 'sudo python patch.py'."
        sys.exit()
        
    # Verbose func
    def status(msg):
        '''
        Print a message for standard output if verbose option is enabled.
        
        Parameters
        ----------
        msg : str
            Message to be displayed.
        '''
        if args.verbose:
            print msg
            
    def patch(src, dst, backup, ifbackup=True, dirs=False):
        '''
        Apply a patch.
        
        Parameters
        ----------
        src : str
            Path of a patched source file.
        dst : str
            Path of the original file.
        backup : str
            Destination of the backuped original file.
        '''
        if ifbackup:
            if os.path.exists(backup):
                status('  Backup skipped. Backup file already exists.')
            elif not os.path.exists(dst):
                status('  Backup skipped. There is no destination file.')
            else:
                status('  Copying the original file...')
                status('    From: ' + dst)
                status('    To:   ' + backup)
                if not args.simulation:
                    subprocess.check_call(['cp', dst, backup])
                else:
                    if not os.path.exists(dst):
                        raise Exception()
        else:
            status('  Backup skipped. Backup is not enabled for this patch.')
        status('  Copying the patched version...')
        status('    From: ' + src)
        status('    To:   ' + dst)
        if not args.simulation:
            if dirs:
                subprocess.check_call(['cp', '-r', src, dst])
            else:
                subprocess.check_call(['cp', src, dst])
        else:
            if not os.path.exists(src):
                raise Exception()
        
    def unpatch(src, dst, backup, ifbackup=True, dirs=False):
        '''
        Restore to the original file.
        
        Parameters
        ----------
        src : str
            Path of a patched source file.
        dst : str
            Path of the original file.
        backup : str
            Destination of the backuped original file.
        '''
        if ifbackup:
            if os.path.exists(backup):
                status('  Copying the original file...')
                status('    From: ' + dst)
                status('    To:   ' + backup)
                if not args.simulation:
                    subprocess.check_call(['cp', backup, dst])
            else:
                status('  ERROR: Could not restore. The original file does not exist.')
        else:
            status('  WARNING: Not implelemted.')
    
    # patch clsi module
    for f in ['LatexRunner.coffee', 'RequestParser.coffee']:
        src = os.path.join('files', f)
        dst = os.path.join(args.dir, 'clsi/app/coffee/', f)
        backup = os.path.join(args.dir, 'clsi/app/coffee/', f+'.org')
        if args.unpatch:
            status('Restoreing to the original file: ' + f)
            unpatch(src, dst, backup)
        else:
            status('Applying a patch for ' + f)
            patch(src, dst, backup)
            
    # patch for web
    f = 'ClsiManager.coffee'
    src = os.path.join('files', f)
    dst = os.path.join(args.dir, 'web/app/coffee/Features/Compile/', f)
    backup = os.path.join(args.dir, 'web/app/coffee/Features/Compile/', f+'.org')
    if args.unpatch:
        status('Restoreing to the original file: ' + f)
        unpatch(src, dst, backup)
    else:
        status('Applying a patch for ' + f)
        patch(src, dst, backup)
        
    f = 'ProjectOptionsHandler.coffee'
    src = os.path.join('files', f)
    dst = os.path.join(args.dir, 'web/app/coffee/Features/Project/', f)
    backup = os.path.join(args.dir, 'web/app/coffee/Features/Project/', f+'.org')
    if args.unpatch:
        status('Restoreing to the original file: ' + f)
        unpatch(src, dst, backup)
    else:
        status('Applying a patch for ' + f)
        patch(src, dst, backup)

    f = 'left-menu.jade'
    src = os.path.join('files', f)
    dst = os.path.join(args.dir, 'web/app/views/project/editor/', f)
    backup = os.path.join(args.dir, 'web/app/views/project/editor/', f+'.org')
    if args.unpatch:
        status('Restoreing to the original file: ' + f)
        unpatch(src, dst, backup)
    else:
        status('Applying a patch for ' + f)
        patch(src, dst, backup)
        
    for f in ['pdf.js', 'pdf.worker.js']:
        src = os.path.join('files', f)
        dst = os.path.join(args.dir, 'web/public/js/libs/pdfjs-'+args.pdfjsver, f)
        backup = os.path.join(args.dir, 'web/public/js/libs/pdfjs-'+args.pdfjsver, f+'.org')
        if args.unpatch:
            status('Restoreing to the original file: ' + f)
            unpatch(src, dst, backup)
        else:
            status('Applying a patch for ' + f)
            patch(src, dst, backup)
            
    f = 'bcmaps'
    src = os.path.join('files', f)
    dst = os.path.join(args.dir, 'web/public/js/libs/', f)
    backup = os.path.join(args.dir, 'web/public/js/libs/', f+'.org')
    if args.unpatch:
        status('Restoreing to the original file: ' + f)
        unpatch(src, dst, backup, ifbackup=False, dirs=True)
    else:
        status('Applying a patch for ' + f)
        patch(src, dst, backup, ifbackup=False, dirs=True)
            
    # Latex system
    for f in ['dvipdf']: #['latexmk', 'dvipdf']:
        src = os.path.join('files', f)
        dst = os.path.join(args.tex, f)
        backup = os.path.join(args.tex, f+'.org')
        if args.unpatch:
            status('Restoreing to the original file: ' + f)
            unpatch(src, dst, backup)
        else:
            status('Applying a patch for ' + f)
            patch(src, dst, backup)
            
    f = 'texfonts.map'
    src = os.path.join('files', f)
    dst = os.path.join(args.dir, f)
    backup = os.path.join(args.dir, f+'.org')
    if not args.unpatch:
        status('Applying a patch for ' + f)
        patch(src, dst, backup)
            
    # compilation option
    if args.compile:
        status('Compile')
        if not args.simulation:
            subprocess.check_call(['grunt', 'install'])
            
    # change file owner
    subprocess.check_call(['chown','-R', 'sharelatex:sharelatex', args.dir])
