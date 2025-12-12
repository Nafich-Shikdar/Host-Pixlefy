import os
from telethon import TelegramClient

# --- আপনার তথ্য এখানে দিন ---
api_id = '59500429405'       # এখানে আপনার API ID বসান (সংখ্যা)
api_hash = '61113729d59500429405d8308b0e6372'   # এখানে আপনার API HASH বসান (কোটেশনের ভেতরে)
phone_number = '+8801405914178'   # আপনার টেলিগ্রাম নম্বর

# সেশন এবং ক্লায়েন্ট সেটআপ
client = TelegramClient('my_downloader_session', api_id, api_hash)

async def main():
    # লগইন নিশ্চিত করা
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    print("\n--- Telegram File Downloader ---\n")
    
    # ইনপুট: চ্যানেলের ইউজারনেম বা লিঙ্ক
    channel_username = input("Enter Channel Username (e.g., @mychannel or link): ")
    
    # ইনপুট: কী ধরণের ফাইল ডাউনলোড করতে চান? (খালি রাখলে সব নামবে)
    extension = input("Specific file type? (e.g., pdf, jpg, mp4) [Press Enter for ALL]: ").strip()
    
    print(f"\nDownloading from {channel_username}...")
    
    # ফোল্ডার তৈরি করা
    folder_name = "Telegram_Downloads"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # ডাউনলোড প্রসেস
    count = 0
    async for message in client.iter_messages(channel_username):
        if message.media: # যদি মেসেজে কোনো মিডিয়া বা ফাইল থাকে
            file_name = message.file.name or f"file_{message.id}"
            
            # এক্সটেনশন ফিল্টার চেক
            if extension and not str(file_name).lower().endswith(extension.lower()):
                continue

            print(f"Downloading: {file_name} ...")
            try:
                path = await client.download_media(message, file=f"{folder_name}/")
                print(f"Saved to: {path}")
                count += 1
            except Exception as e:
                print(f"Error downloading {file_name}: {e}")

    print(f"\n--- Complete! Total {count} files downloaded. ---")

with client:
    client.loop.run_until_complete(main())
