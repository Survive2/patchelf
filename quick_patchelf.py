from re import *
import os
import argparse
import sys
from sgtpyutils.logger import logger
from sgtpyutils.xls_txt.list import list2sheet


libc_all_in_one=f'xxx' # the path of the glibc-all-in-one
start_path=f'xxx' #the path of the elf file

def process_cmd(cmd):
    logger.info(f'exec command: {cmd}')
    os.system(cmd)

def process_patchelf(libc_file,ld_file,elf_file):
    libc_file_path=f'{libc_all_in_one}/{libc_file}'
    elf_file_path=f'{start_path}/{elf_file}'
    ld_file_path=f'{libc_all_in_one}/{ld_file}'
    cmd=f'patchelf --set-interpreter {ld_file_path} {elf_file_path}'
    process_cmd(cmd)
    cmd=f'patchelf --set-rpath {libc_file_path} {elf_file_path}'
    process_cmd(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="Patchelf Quickly!"
            )
    parser.add_argument(
            '-libc',
            default='none',
            help="the libc file you want"
            )
    parser.add_argument(
            '-ld',
            default='None',
            help="the ld file you want"
            )

    parser.add_argument(
            '-elf',
            default='None',
            help="the target elf file"
            )

    parser.add_argument(
            '-l',
            default=False,
            nargs=argparse.OPTIONAL,
            dest='show_all_libc',
            help="show the avaliable libc"
            )


    args = parser.parse_args()

    libc_list=os.listdir(libc_all_in_one)
    libc_list=sorted(libc_list)
    
    if(args.show_all_libc or args.show_all_libc is None):
        libc_list= list2sheet(libc_list, max_show_count=20)
        description = ['\navaliable libc list:']
        description.append('\n'.join(libc_list))
        logger.info('\n'.join(description))
        sys.exit(0)

    process_patchelf(
            args.libc,
            args.ld,
            args.elf,
            )

    logger.info(f'sucessfully patch {args.elf} libc to {args.libc}')
