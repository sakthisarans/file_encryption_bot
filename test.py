import telebot,time
import enc,os

api='6554856541:AAF9Q_Bp9vhKBuudBdomEKhv7N1CGGKPsoo'
bot=telebot.TeleBot(api)



@bot.message_handler(commands='start')
def bot_status(msg):
    bot.reply_to(msg, "welcome "+msg.from_user.first_name+"\n"
                    "bot is up and running")
    
@bot.message_handler(commands='decrypt')
def decrypt(msg):
    bot.send_message(chat_id=msg.from_user.id,text="send .enc file")
    bot.register_next_step_handler(msg,key)

def key(msg):
    file_name = msg.document.file_name
    file_info = bot.get_file(msg.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    path=f'{os.getcwd()}/encfil/{file_name}'
    open(path,'wb+').write(downloaded_file)
    bot.send_message(msg.from_user.id,text='enter key')
    bot.register_next_step_handler(msg,dec,path)

def dec(msg,encfilpath):
    try:
        key=msg.text
        out=f'{os.getcwd()}/out'
        outpath=(os.path.basename(os.path.splitext(encfilpath)[0]).split('/')[-1])
        enc.decrypt_file(encfilpath,out,enc.hex_to_bytes(key))
        bot.send_document(msg.from_user.id,document=open(f'{os.getcwd()}/out/{outpath}','rb'))
    except Exception as ex:
        print(ex)

@bot.message_handler(commands='encrypt')
def encrypt(msg):
    bot.send_message(chat_id=msg.from_user.id,text="send file")
    bot.register_next_step_handler(msg,fil)

def fil(msg):
    try:
        bot.send_message(chat_id=msg.from_user.id,text='processing..........')
        
        file_name = msg.document.file_name
        print(file_name)
        file_info = bot.get_file(msg.document.file_id)
        print(msg.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        print(downloaded_file)
        path=f'{os.getcwd()}/file/{file_name}'
        open(path,'wb+').write(downloaded_file)
        out=f'{os.getcwd()}/out'
        print(enc.encrypt_file(path,out))
        bot.send_document(chat_id=msg.from_user.id,document=open(f'{os.getcwd()}/out/{file_name}.enc','rb'))
        bot.send_document(chat_id=msg.from_user.id,document=open(f'{os.getcwd()}/out/{file_name}.txt','rb'))
    except:
        bot.send_message(chat_id=msg.from_user.id,text='error try again')



try:
    bot.polling(non_stop=True)
except Exception as e:
    print(e)
    time.sleep(1)