import os

dups = []

toDel = []

def convert(istr):
    arr = istr.split('\t')
    return arr[1] + '\\' + arr[0]

with open('duplicate.txt', 'r', encoding='utf-16le') as f:
    f.readline()
    dup = []
    while True:
        row = f.readline()[:-1]
        if (row == ''):
            dups.append(dup)
            break;
        elif (row[0] == '-'):
            dups.append(dup)
            dup = []
        else:
            dup.append(convert(row))


for i in dups:
    guess = i.index(min(i, key=len))
    for f in range(0, len(i)):
        if (guess == f):
            print('>['+str(f)+']: ' + i[f])
        else:
            print('d['+str(f)+']: ' + i[f])
    
    index = input("Is the file to keep selected right? [Y/index] ")
    try:
        index = int(index)
    except:
        index = guess

    for f in range(0, len(i)):
        if (index != f):
            toDel.append(i[f])
    print()
    
print("Generating BAT file...")

bat = ['@echo off',
       'echo --== Вы действительно хотите удалить следующие файлы? ==--']

for i in toDel:
    bat.append('echo ' + i)

bat += ['set /p agreement="Вы действительно хотите удалить все перечисленные выше файлы? [д/Н] "',
'if "%agreement%" == "Y" (',
'\tgoto execute',
') else (',
'\tif "%agreement%" == "y" (',
'\t\tgoto execute',
'\t) else (',
'\t\tif "%agreement%" == "Д" (',
'\t\t\tgoto execute',
'\t\t) else (',
'\t\t\tif "%agreement%" == "д" (',
'\t\t\t\tgoto execute',
'\t\t\t) else (',
'\t\t\t\tgoto abort',
'\t\t\t)',
'\t\t)',
'\t)',
')',
':execute']

for i in toDel:
    bat.append("@powershell.exe -nologo -noprofile -Command \"& {Add-Type -AssemblyName 'Microsoft.VisualBasic'; Get-ChildItem -Path '" + i + "' | ForEach-Object { if ($_ -is [System.IO.DirectoryInfo]) { [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($_.FullName,'OnlyErrorDialogs','SendToRecycleBin') } else { [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($_.FullName,'OnlyErrorDialogs','SendToRecycleBin') } } }\"")

bat += ['goto end',
        ':abort',
        'echo Удаление отменено.',
        ':end']

with open('duplicate.bat', 'w',encoding='cp866') as f:
    f.writelines('\n'.join(bat) + '\n')

print('Done.')
