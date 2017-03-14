#!/usr/bin/env python3

import os
import re
import sys
import sqlite3
from collections import Counterd

from tqdm import tqdm

def file_lines(file_path):
    with open(file_path, 'rb') as fp:
        b = fp.read()
    content = b.decode('utf8', 'ignore')
    lines = []
    for line in tqdm(content.split('\n')):
        try:
            line = line.replace('\n', '').strip()
            if line.startswith('E'):
                lines.append('')
            elif line.startswith('M '):
                chars = line[2:].split('/')
                while len(chars) and chars[len(chars) - 1] == '.':
                    chars.pop()
                if chars:
                    sentence = ''.join(chars)
                    sentence = re.sub('\s+', '，', sentence)
                    lines.append(sentence)
        except:
            print(line)
            return lines
            lines.append('')
    return lines

def contain_chinese(s):
    if re.findall('[\u4e00-\u9fa5]+', s):
        return True
    return False

def valid(a, max_len=0):
    if len(a) > 0 and contain_chinese(a):
        if max_len <= 0:
            return True
        elif len(a) <= max_len:
            return True
    return False

def insert(a, b, cur):
    cur.execute("""
    INSERT INTO conversation (ask, answer) VALUES
    ('{}', '{}')
    """.format(a.replace("'", "''"), b.replace("'", "''")))

def insert_if(question, answer, cur, input_len=500, output_len=500):
    if valid(question, input_len) and valid(answer, output_len):
        insert(question, answer, cur)
        return 1
    return 0

def main(file_path):
    lines = file_lines(file_path)

    print('一共读取 %d 行数据' % len(lines))

    db = 'db'
    if os.path.exists(db):
        os.remove(db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversation
        (ask text, answer text);
        """)
    conn.commit()

    words = Counter()
    a = ''
    b = ''
    inserted = 0

    for index, line in tqdm(enumerate(lines), total=len(lines)):
        words.update(Counter(line))
        a = b
        b = line
        ask = a
        answer = b
        inserted += insert_if(ask, answer, cur)
        # 批量提交
        if inserted != 0 and inserted % 50000 == 0:
            conn.commit()
    conn.commit()

if __name__ == '__main__':
    file_path = 'dgk_shooter_min.conv'
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print('文件 {} 不存在'.format(file_path))
    else:
        main(file_path)


#C:\Program Files (x86)\Common Files\NetSarang;C:\tools\OpenBLAS-v0.2.19-Win64-int32;D:\Anaconda\MinGW\bin;C:\cygwin64\bin;C:\ProgramData\Oracle\Java\javapath;;C:\Program Files (x86)\AMD APP\bin\x86_64;C:\Program Files (x86)\AMD APP\bin\x86;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Program Files (x86)\ATI Technologies\ATI.ACE\Core-Static;D:\Program Files\Java\jdk1.7.0_79\bin;D:\Program Files\Java\jdk1.7.0_79\jre\bin;C:\Program Files\Microsoft\Web Platform Installer\;C:\Program Files (x86)\Microsoft ASP.NET\ASP.NET Web Pages\v1.0\;C:\Program Files (x86)\Windows Kits\8.0\Windows Performance Toolkit\;C:\Program Files\Microsoft SQL Server\110\Tools\Binn\;D:\Indri\Indri5.9\bin;C:\CTEX\UserData\miktex\bin;C:\CTEX\MiKTeX\miktex\bin;C:\CTEX\CTeX\ctex\bin;C:\CTEX\CTeX\cct\bin;C:\CTEX\CTeX\ty\bin;C:\CTEX\Ghostscript\gs9.05\bin;C:\CTEX\GSview\gsview;C:\CTEX\WinEdt;D:\opencv\build\x64\vc12;C:\Program Files (x86)\Microsoft Visual Studio 11.0\Common7\IDE;C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\bin;C:\tools;C:\Program Files\Git\bin;;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v7.5\lib\x64;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v7.5\bin;C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\bin;C:\tools\pypy2-v5.4.1-win32;C:\tools\pypy2-v5.4.1-win32\bin;C:\Strawberry\c\bin;C:\Strawberry\perl\site\bin;C:\Strawberry\perl\bin;C:\Program Files\CMake\bin;D:\Anaconda3;D:\Anaconda3\Scripts;D:\Anaconda3\Library\bin