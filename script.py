import requests
import json

def remove_bismillah(text, surah_number, ayah_number):
    if surah_number != '001' or ayah_number != 1:
        bismillah = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِیمِ"
        return text.replace(bismillah, "").strip()
    return text

def fetch_all_surahs():
    base_url = "https://api.alquran.cloud/v1/surah"
    all_surah_data = {}

    for surah_number in range(1, 115):  # For all 114 surahs
        formatted_number = f"{surah_number:03}"  # Format surah number with leading zeros
        url = f"{base_url}/{surah_number}"
        response = requests.get(url)
        surah_details = response.json()

        if surah_details['status'] == 'OK':
            data = surah_details['data']
            surah_name = data['englishName']
            ayahs = data['ayahs']
            ayah_texts = []
            for index, ayah in enumerate(ayahs):
                if 'text' in ayah:
                    cleaned_text = remove_bismillah(ayah['text'], formatted_number, index + 1)
                    ayah_texts.append(cleaned_text)
            surah_text = ' . '.join(ayah_texts)
            all_surah_data[formatted_number] = {
                "name": surah_name,
                "text": surah_text
            }

    # Save the gathered data to a JSON file
    with open('surahs_data.json', 'w', encoding='utf-8') as file:
        json.dump(all_surah_data, file, ensure_ascii=False, indent=4)

    print("JSON file with all surahs has been created.")

# Call this function in your local Python environment
fetch_all_surahs()