
ORG_DELIMITER = ':- '
GREP_CMD_ORG = ['grep', '-r', '-n', '--include=*.org', r'"\-*::"']

def grep_org_pairs(directory, out):
    '''
    Extracts facts in the form "- ... :: ..." from my .org-files.
    Searches recursively in the path given by directory
    and stores the result in the file given by out.
    '''
    subprocess.call(GREP_CMD_ORG + [directory], stdout=out)

    
