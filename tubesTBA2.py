import re

subjek = ["aku", "kamu", "dia", "kita", "mereka"]
predikat = ["makan", "minum", "pergi", "baca", "nonton"]
obyek = ["nasi", "mineral", "kuliah", "koran", "film"]
ket = ["di rumah", "di kampus", "pada pagi hari", "pada siang hari", "pada malam hari"]

def recognize(buffer, kata):
    return buffer in kata

def tokenation(kalimat):
    return list(kalimat)

def parse_FA(chars):
    state = 'q0'
    buffer = ""
    tipeToken = []

    subjek_chars = ['a', 'd', 'e', 'i', 'k', 'm', 'r', 't', 'u']
    predikat_chars = ['a', 'b', 'c', 'g', 'i', 'k', 'm', 'n', 'o', 'p', 'r', 't']
    obyek_chars = ['a', 'f', 'i', 'k', 'l', 'm', 'n', 'o', 'r', 's', 'u']
    ket_chars = ['a', 'd', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 'u']

    for char in chars:
        buffer += char
        if state == 'q0' and buffer.strip() and buffer.strip()[-1] in subjek_chars and recognize(buffer.strip(), subjek):
            state = 'q1'
            tipeToken.append('S')
            buffer = ""
        elif state == 'q1' and buffer.strip() and buffer.strip()[-1] in predikat_chars and recognize(buffer.strip(), predikat):
            state = 'q2'
            tipeToken.append('P')
            buffer = ""
        elif state == 'q2' and buffer.strip() and buffer.strip()[-1] in obyek_chars and recognize(buffer.strip(), obyek):
            state = 'q3'
            tipeToken.append('O')
            buffer = ""
        elif state == 'q2' and buffer.strip() and buffer.strip()[-1] in ket_chars and recognize(buffer.strip(), ket):
            state = 'q3'
            tipeToken.append('K')
            buffer = ""
        elif state == 'q3' and buffer.strip() and buffer.strip()[-1] in ket_chars and recognize(buffer.strip(), ket):
            state = 'q4'
            tipeToken.append('K')
            buffer = ""
        else:
            continue
    return (state == 'q2' or state == 'q3' or state == 'q4'), tipeToken

class PDA:
    def __init__(self):
        self.stack = []

    def parse(self, chars):
        self.stack = ['#']  # Initial stack with bottom marker
        state = 'q0'
        buffer = ""
        tipeToken = []

        subjek_chars = ['a', 'd', 'e', 'i', 'k', 'm', 'r', 't', 'u']
        predikat_chars = ['a', 'b', 'c', 'g', 'i', 'k', 'm', 'n', 'o', 'p', 'r', 't']
        obyek_chars = ['a', 'f', 'i', 'k', 'l', 'm', 'n', 'o', 'r', 's', 'u']
        ket_chars = ['a', 'd', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 'u']

        print(f"Initial Stack: {self.stack}")  # Print initial stack

        for char in chars:
            buffer += char

            if state == 'q0' and buffer.strip() and buffer.strip()[-1] in subjek_chars and recognize(buffer.strip(), subjek):
                # Read λ, pop λ, push S
                state = 'q1'
                self.stack.append('A')  # Push A
                tipeToken.append('S')
                buffer = ""
                print(f"State: q0 -> q1, Read: λ, Pop: λ, Push: A, Stack: {self.stack}")
                
            elif state == 'q1' and buffer.strip() and buffer.strip()[-1] in predikat_chars and recognize(buffer.strip(), predikat):
                state = 'q2'
                tipeToken.append('P')
                buffer = ""
                print(f"State: q1 -> q2, Read: λ, Pop: λ, Push: A, Stack: {self.stack}")

            elif state == 'q2' and buffer.strip() and buffer.strip()[-1] in obyek_chars and recognize(buffer.strip(), obyek):
                tipeToken.append('O')
                buffer = ""
                print(f"State: q2 -> q2, Read: λ, Pop: λ, Push: A, Stack: {self.stack}")

            elif state == 'q2' and buffer.strip() and buffer.strip()[-1] in ket_chars and recognize(buffer.strip(), ket):
                tipeToken.append('K')
                buffer = ""
                print(f"State: q2 -> q2, Read: λ, Pop: λ, Push: A, Stack: {self.stack}")

        # Final transition when stack is empty
        while self.stack and self.stack[-1] != '#':
            self.stack.pop()
            print(f"State: q2 -> q2, Read: λ, Pop: λ, Push: λ, Stack: {self.stack}")

        if self.stack and self.stack[-1] == '#':
            self.stack.pop()  # Pop the bottom marker
            print(f"State: q2 -> q3, Read: λ, Pop: #, Push: λ, Stack is empty")

        return (state == 'q2' or state == 'q3'), tipeToken

def main():
    print("Pilih metode:")
    print("1. Token Recognizer FA per Character")
    print("2. Push Down Automata Parser per Character")
    metode = input("Pilihan (1/2): ").strip()

    if metode not in ['1', '2']:
        print("Metode tidak valid. Silakan pilih 1 atau 2.")
        return

    kalimat = input("Masukkan kalimat: ")

    kalimat = re.sub(r'[^a-zA-Z\s]', '', kalimat.lower())

    chars = tokenation(kalimat)
    print("Tokenisasi per Karakter:", chars)

    if metode == '1':
        valid, tipeToken = parse_FA(chars)
        if valid:
            print("Kalimat valid dengan FA per Karakter")
        else:
            print("Kalimat tidak valid dengan FA per Karakter")
        print("Tipe tata bahasa:", tipeToken)
    elif metode == '2':
        pda = PDA()
        valid, tipeToken = pda.parse(chars)
        if valid:
            print("Kalimat valid dengan PDA per Karakter")
        else:
            print("Kalimat tidak valid dengan PDA per Karakter")
        print("Tipe tata bahasa:", tipeToken)

if __name__ == "__main__":
    main()
