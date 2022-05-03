import secrets
import time
from threading import Thread
import requests, ctypes
#from eth_account import Account
#from secrets import token_bytes
#from coincurve import PublicKey
#from sha3 import keccak_256
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional

threadc = int(input("Введи количество потоков: "))
secondCount = int(input("Введите кол-во часов: "))
#data = (input("Введи количество выполнений: "))
def divide(stuff):
    return [stuff[i::threadc] for i in range(threadc)]
class telegram:
    token = '5237275928:AAE_v3LMCBoNJSO-zeQPYBrqjOWxPGpaMvk'
    channel_id = '@maxgood11'
def send_telegram(text: str):
    try:
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(telegram.token), params=dict(
        chat_id=telegram.channel_id,
        text=text))
        print ("Send to telegram")
    except:
        print(f'Error send telegram.')
send_telegram("Начал Домашний комп")
def isCheckWork(secondCount):
    lastSecondTime = time.time()+secondCount*60*60
    while True:
        try:
            if time.time() >= lastSecondTime:
                lastSecondTime = time.time()+secondCount*60*60
                send_telegram("Я нигер, я работаю!")              
        except Exception as e:
            print(e)
            pass
def checker():
    total = 0.0
    
    while True:
        try:
        
            MNEMONIC: str = generate_mnemonic(language="english", strength=256)
            PASSPHRASE: Optional[str] = None
            bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
            bip44_hdwallet.from_mnemonic(
            mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE)
            bip44_hdwallet.clean_derivation()
            address_index = 0
            bip44_derivation: BIP44Derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index)
            bip44_hdwallet.from_path(path=bip44_derivation)
            #private_key = secrets.token_hex(32)
            #private_key = ('2c1a2839a9db3dcda1a177882dc954b0c99568ef1b419a0450f06a8a686d74ca')
            #acct = Account.from_key(private_key)
            #private_key = keccak_256(token_bytes(32)).digest()
            #public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
            #acct = keccak_256(public_key).digest()[-20:]
            #addr = ("0x"+acct.hex())
            addr = bip44_hdwallet.address()
            bal = 0.0
            try:  
                json_bal = requests.get(f"https://openapi.debank.com/v1/user/total_balance?id={addr}").json()
                total = float(total) + float(json_bal['total_usd_value'])
                #ctypes.windll.kernel32.SetConsoleTitleW(f"Private key Checker v1.0 | Total - {total}$")
                print(f"ETH:\n Key: {bip44_hdwallet.private_key()}\nAddress: {addr}\n Mnemonic : {bip44_hdwallet.mnemonic()}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                #print(f"ETH:\n Key: {private_key.hex()}\nAddress: {addr}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                
                if float(json_bal['total_usd_value'])  > 0.0:
                    save = open("Results.txt", "a").write(
                    f"ETH:\n Key: {bip44_hdwallet.private_key()}\nAddress: {addr} \nMnemonic : {bip44_hdwallet.mnemonic()}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                    text = (f"ETH:\n Key: {bip44_hdwallet.private_key()}\nAddress: {addr}\nMnemonic : {bip44_hdwallet.mnemonic()}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                    #f"ETH:\n Key: {private_key.hex()}\nAddress: {addr}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                    #text = (f"ETH:\n Key: {private_key.hex()}\nAddress: {addr}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                    send_telegram(text)    
            except Exception as e:
                print(e)
                print("API Error , sleep 5s...")
                time.sleep(5)
                try:
                    json_bal = requests.get(
                        f"https://openapi.debank.com/v1/user/total_balance?id={addr}").json()
                    
                    print(f"ETH:\n Key: {bip44_hdwallet.private_key()}\nAddress: {addr}\nMnemonic : {bip44_hdwallet.mnemonic()} \nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                    if float(json_bal['total_usd_value']) or acctb.get_balance('usd') > 0.0:
                        save = open("Results.txt", "a").write(f"ETH:\n Key: {bip44_hdwallet.private_key()}\nAddress: {addr}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                        text = (f"ETH:\n Key: {bip44_hdwallet.private_key()}\nAddress: {addr} \nMnemonic : {bip44_hdwallet.mnemonic()} \nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                        #save = open("Results.txt", "a").write(f"ETH:\n Key: {private_key.hex()}\nAddress: {addr}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                        #text = (f"ETH:\n Key: {private_key.hex()}\nAddress: {addr}\nFull Balance: {json_bal['total_usd_value']}\n--------------------------------\n")
                        send_telegram(text) 
                except Exception:
                    error = open("Errors.txt", "a").write(f'{private_key.hex}\n')
                    pass
                pass
        except Exception:
            pass

threads = []
tr1 = Thread(target=isCheckWork, args=(secondCount,))
tr1.start()

for i in range(threadc):
    threads.append(Thread(target=checker))
    threads[i].start()
for thread in threads:
    thread.join()


#print (f"Hex:{hex} Adress: {acct.address} Private key: {private_key}")