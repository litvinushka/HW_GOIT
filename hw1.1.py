import os
import shutil
import re
extensions = {
    'images': {'JPEG', 'PNG', 'JPG', 'SVG'},
    'videos': {'AVI', 'MP4', 'MOV', 'MKV'},
    'documents': {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'},
    'audio': {'MP3', 'OGG', 'WAV', 'AMR'},
    'archives': {'ZIP', 'GZ', 'TAR'}
}
translit_dict = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
    'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
    'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y',
    'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
    'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
}


def main():
    folder_name = input("Введите название папки для сортировки: ")
    folder_path = os.path.abspath(folder_name)

    if not os.path.exists(folder_path):
        print("Папка не найдена.")
        return

    process_folder(folder_path)


def normalize(filename):
    return re.sub(r'[^\w\s.-]', '_', ''.join(translit_dict.get(c, c) for c in filename))


def sort_folder(folder_path):
    unknown_folder = 'unknown'

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in extensions.keys()]

        for file in files:
            file_path = os.path.join(root, file)
            filename, extension = os.path.splitext(file)
            extension = extension[1:].upper()

            destination_folder = next(
                (category for category, ext_list in extensions.items()
                 if extension in ext_list),
                unknown_folder
            )
            destination_folder_path = os.path.join(
                folder_path, destination_folder)

            os.makedirs(destination_folder_path, exist_ok=True)

            try:
                normalized_filename = normalize(filename)

                destination_path = os.path.join(
                    destination_folder_path, normalized_filename)

                if destination_folder == 'archives':
                    shutil.unpack_archive(file_path, destination_path)
                else:
                    destination_filename = f"{normalized_filename}.{extension}"
                    destination_path = os.path.join(
                        destination_folder_path, destination_filename)
                    shutil.move(file_path, destination_path)
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass

    print('Сортировка завершена!')


def list_files_in_folder(folder_path):
    for category in os.listdir(folder_path):
        category_path = os.path.join(folder_path.encode(
            'utf-8').decode('cp1251'), category.encode('utf-8').decode('cp1251'))
        if os.path.isdir(category_path):
            print(f'{category}:')
            for file in os.listdir(category_path):
                print(file)
            print()


def list_known_extensions():

    known_extensions = {ext for ext_list in extensions.values()
                        for ext in ext_list}
    for extension in known_extensions:
        print(extension)


def list_unknown_extensions(folder_path):

    known_extensions = {ext for ext_list in extensions.values()
                        for ext in ext_list}
    unknown_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            _, extension = os.path.splitext(file)
            extension = extension[1:].upper()
            if extension not in known_extensions:
                unknown_extensions.add(extension)

    for extension in unknown_extensions:
        print(extension)


def process_folder(folder_path):
    sort_folder(folder_path)
    print("Сортировка завершена.")
    print("Список файлов в каждой категории:")
    list_files_in_folder(folder_path)
    print("Список известных расширений файлов:")
    list_known_extensions()
    print("Список неизвестных расширений файлов:")
    list_unknown_extensions(folder_path)


if __name__ == "__main__":
    main()