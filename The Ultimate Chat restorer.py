import json
import os
import zipfile
import sys

def convert_telegram_to_whatsapp(telegram_export_path, whatsapp_output_path):
    with open(telegram_export_path, 'r', encoding='utf-8') as file:
        telegram_data = json.load(file)

    with open(whatsapp_output_path, 'w', encoding='utf-8') as output_file:
        if 'messages' in telegram_data:
            messages = telegram_data['messages']
        elif 'chats' in telegram_data:
            messages = []
            for chat in telegram_data['chats'].get('list', []):
                messages.extend(chat.get('messages', []))
        else:
            messages = []

        for message in messages:
            date = message.get('date', '')
            from_user = message.get('from', '')
            text = message.get('text', '')
            media_type = message.get('media_type', '')
            mine_type = message.get('mime_type', '')
            file_url = message.get('file', '')

            date_parts = date.split('T')
            if len(date_parts) == 2:
                date_formatted = date_parts[0].replace('-', '/')
                time_formatted = date_parts[1]
                date = f"[{date_formatted}, {time_formatted}]"

            if isinstance(text, str):
                whatsapp_message = f"{date} - {from_user}: {text}\n"
            else:
                for text_object in text:
                    if isinstance(text_object, dict):
                        text_from_text_dict_object = text_object.get('text', '')
                        whatsapp_message = f"{date} - {from_user}: {text_from_text_dict_object}\n"
                    elif isinstance(text_object, str):
                        whatsapp_message = f"{date} - {from_user}: {text_object}\n"

            output_file.write(whatsapp_message)

            if file_url:
                # output_file.write(f"{date} - {from_user}: <attached: {file_url}>\n")
                filename = os.path.basename(file_url)
                output_file.write(f"{date} - {from_user}: <attached: {filename}>\n")


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

def create_zip_file():
    zipf = zipfile.ZipFile('Whatsapp Chat - xxx.zip', 'w', zipfile.ZIP_DEFLATED)
    zipf.write('_chat.txt')
    media_folders = ['photos', 'stickers', 'video_files', 'voice_messages', 'round_video_messages', 'files', 'contacts']

    for folder in media_folders:
        if os.path.exists(folder):
            # zipdir(folder, zipf)
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=os.path.basename(file_path))

    zipf.close()

def main():
    if len(sys.argv) > 1:
        telegram_export_path = sys.argv[1]
        whatsapp_output_path = sys.argv[2]
    else:
        telegram_export_path = 'result.json'
        whatsapp_output_path = '_chat.txt'

    convert_telegram_to_whatsapp(telegram_export_path, whatsapp_output_path)
    create_zip_file()

if __name__ == "__main__":
    main()


