import sciter
import clipboard
from tkinter import Tk
from tkinter import filedialog
import ctypes
import translator
import sys
import traceback


class Frame(sciter.Window):
    def __init__(self, options):
        super().__init__(ismain=True, uni_theme=True)
        self.translator = translator.Translator()
        self.options = options

    @sciter.script
    def getHtmlFile(self):
        return 'mainpage.html'

    @sciter.script
    def print(self, p1):
        print(p1)

    @sciter.script
    def keyPaste(self):
        return clipboard.paste()

    @sciter.script
    def keyImport(self):
        try:
            root = Tk()
            root.withdraw()
            with open(filedialog.askopenfilename(), 'r') as f:
                return f.read()
        except Exception:
            msgbox(f'Failed to read key\n\n{traceback.format_exc()}', 'Error', 16)
            return ''

    @sciter.script
    def hide(self, public, private, keyIV, encryptionMethod, pgpKey):
        def checkErrors():
            errors = []
            if len(public.split()) < 2:
                errors.append('Public message must be 2 or more words')
            if len(private) == 0:
                errors.append('Must have a private message')
            if len(keyIV) != 32 and encryptionMethod == '1key':
                errors.append('Key must be 32 characters for this encryption method')
            if not self.translator.verifyPGP(pgpKey) and encryptionMethod == '2key' and 'ignorePGP' not in self.options:
                errors.append('Your PGP public/private key is invalid.')
            if len(errors) > 0:
                errors = "\n".join(errors)
                msgbox(f'You have the following errors: \n{errors}', 'Errors', 16)
                return ['error', '1']
            del errors

        checkErrors()

        try:
            if encryptionMethod == '1key':
                key = keyIV[:16]
                IV = keyIV[16:]
                private = self.translator.SymmetricalEncryption.encrypt(private, key, IV)
            elif encryptionMethod == '2key':
                msgbox('This encryption method may not work. A recommended fix is to encrypt/decrypt it yourself and select the "No encryption" method', 'Warning',
                       48)
                private = self.translator.AsymmetricEncryption.encrypt(private,  self.translator.AsymmetricEncryption.loadPublic(pgpKey))

            # public, private = self.translator.slice(public, private, 220, self.options)
            # mapping = self.translator.getMapping(public, private)
            # Convert Private -> Binary -> Zero-width
            private = self.translator.Conversion.convertTextBinary(private)
            private = self.translator.Conversion.convertBinaryZero(private)
            finalMessage = self.translator.insertMessage(public, private)
            msgbox('Message successfully generated', 'Success :)', 64)
            return [finalMessage]
        except Exception:
            msgbox(traceback.format_exc(), 'Fatal error', 16)
            return ['error']

    @sciter.script
    def extract(self, public, keyIV, encryptionMethod, pgpKey):
        def checkErrors():
            errors = []
            if len(public.split()) < 2:
                errors.append('Public key must be 2 or more words')
            if len(keyIV) != 32 and encryptionMethod == '1key':
                errors.append('Key must be 32 characters for this encryption method')
            if len(errors) > 0:
                errors = "\n".join(errors)
                msgbox(f'You have the following errors: \n{errors}', 'Errors', 16)
                return ['error', '2']
            del errors

        checkErrors()

        try:
            # Find text between startEnd chars
            public, private = self.translator.findContent(public)  # ZeroWidth encoded
            private = self.translator.Conversion.convertZeroBinary(private)  # Binary encoded (Zero -> Binary)
            private = self.translator.Conversion.convertBinaryText(private)  # Deciphered private message

            if encryptionMethod == '1key':
                key = keyIV[:16]
                IV = keyIV[16:]
                private = self.translator.SymmetricalEncryption.decrypt(private, key, IV)
            elif encryptionMethod == '2key':
                msgbox('This encryption method may not work. A recommended fix is to encrypt/decrypt it yourself and select the "No encryption" method', 'Warning',
                       48)
                private = self.translator.AsymmetricEncryption.decrypt(private, self.translator.AsymmetricEncryption.loadPrivate(pgpKey))

            msgbox('Message successfully extracted', 'Success :)', 64)

            return [private]
        except Exception:
            msgbox(traceback.format_exc(), 'Fatal error', 16)
            return ['error']


def msgbox(text, title, code):
    return ctypes.windll.user32.MessageBoxW(0, text, title, code)


if __name__ == '__main__':
    options = sys.argv[1:]
    frame = Frame(options)
    frame.load_file('index.html')
    frame.run_app()
