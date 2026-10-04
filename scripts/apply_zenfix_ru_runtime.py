#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: apply_zenfix_ru_runtime.py /path/to/vlc")

root = Path(sys.argv[1]).resolve()
qt_cpp = root / "modules/gui/qt/qt.cpp"
text = qt_cpp.read_text(encoding="utf-8")

old = '''        assert(text);\n        return QString::fromUtf8(text);\n'''

new = r'''        assert(text);

        const QString translated = QString::fromUtf8(text);
        const QString source = QString::fromUtf8(sourceText);

        // VLC 4 snapshots currently ship an incomplete Russian catalog for
        // a number of new Qt/QML strings. Keep normal gettext translations as
        // the primary source and only apply Zenfix fallbacks when Russian is
        // actually selected and gettext returned the original English string.
        if (translated == source
            && QString::fromUtf8(vlc_gettext("Video")) == QString::fromUtf8("Видео"))
        {
            if (source == QStringLiteral("Open Disc")) return QString::fromUtf8("Открыть диск");
            if (source == QStringLiteral("Videos")) return QString::fromUtf8("Видео");
            if (source == QStringLiteral("Playlists")) return QString::fromUtf8("Плейлисты");
            if (source == QStringLiteral("Artists")) return QString::fromUtf8("Исполнители");
            if (source == QStringLiteral("Albums")) return QString::fromUtf8("Альбомы");
            if (source == QStringLiteral("Tracks")) return QString::fromUtf8("Треки");
            if (source == QStringLiteral("Genres")) return QString::fromUtf8("Жанры");
            if (source == QStringLiteral("Folders")) return QString::fromUtf8("Папки");
            if (source == QStringLiteral("Computer")) return QString::fromUtf8("Компьютер");
            if (source == QStringLiteral("Discover")) return QString::fromUtf8("Обнаружение");
            if (source == QStringLiteral("Services")) return QString::fromUtf8("Сервисы");
            if (source == QStringLiteral("Add a service")) return QString::fromUtf8("Добавить сервис");
            if (source == QStringLiteral("Radio Browser")) return QString::fromUtf8("Радио");
            if (source == QStringLiteral("Podcasts")) return QString::fromUtf8("Подкасты");
            if (source == QStringLiteral("Jamendo Selections")) return QString::fromUtf8("Подборки Jamendo");
            if (source == QStringLiteral("Paste or write the URL here")) return QString::fromUtf8("Вставьте или введите URL");

            if (source == QStringLiteral("No video found")) return QString::fromUtf8("Видео не найдено");
            if (source == QStringLiteral("Please try adding sources")) return QString::fromUtf8("Попробуйте добавить источники");
            if (source == QStringLiteral("No video found\nPlease try adding sources")) return QString::fromUtf8("Видео не найдено\nПопробуйте добавить источники");
            if (source == QStringLiteral("No artists found\nPlease try adding sources")) return QString::fromUtf8("Исполнители не найдены\nПопробуйте добавить источники");
            if (source == QStringLiteral("No albums found\nPlease try adding sources")) return QString::fromUtf8("Альбомы не найдены\nПопробуйте добавить источники");
            if (source == QStringLiteral("No tracks found\nPlease try adding sources")) return QString::fromUtf8("Треки не найдены\nПопробуйте добавить источники");
            if (source == QStringLiteral("No genres found\nPlease try adding sources")) return QString::fromUtf8("Жанры не найдены\nПопробуйте добавить источники");
            if (source == QStringLiteral("No media found\nPlease try adding sources")) return QString::fromUtf8("Медиа не найдено\nПопробуйте добавить источники");
            if (source == QStringLiteral("No playlists found")) return QString::fromUtf8("Плейлисты не найдены");
            if (source == QStringLiteral("Right click on a media\nto add it to a playlist")) return QString::fromUtf8("Щёлкните правой кнопкой по медиа,\nчтобы добавить его в плейлист");
            if (source == QStringLiteral("No media found")) return QString::fromUtf8("Медиа не найдено");
            if (source == QStringLiteral("No network shares found")) return QString::fromUtf8("Сетевые ресурсы не найдены");
            if (source == QStringLiteral("No information available")) return QString::fromUtf8("Информация недоступна");
            if (source == QStringLiteral("No results")) return QString::fromUtf8("Нет результатов");

            if (source == QStringLiteral("&Tools") || source == QStringLiteral("Tools")) return QString::fromUtf8("Инструменты");
            if (source == QStringLiteral("Trim Video...")) return QString::fromUtf8("Обрезать видео...");
            if (source == QStringLiteral("Trim Video")) return QString::fromUtf8("Обрезать видео");
            if (source == QStringLiteral("Source file")) return QString::fromUtf8("Исходный файл");
            if (source == QStringLiteral("Output file")) return QString::fromUtf8("Выходной файл");
            if (source == QStringLiteral("Start time")) return QString::fromUtf8("Начало");
            if (source == QStringLiteral("End time")) return QString::fromUtf8("Конец");
            if (source == QStringLiteral("Browse...")) return QString::fromUtf8("Обзор...");
            if (source == QStringLiteral("Trim")) return QString::fromUtf8("Обрезать");
            if (source == QStringLiteral("Select source video")) return QString::fromUtf8("Выберите исходное видео");
            if (source == QStringLiteral("Save trimmed video")) return QString::fromUtf8("Сохранить обрезанное видео");
            if (source == QStringLiteral("Trimming video...")) return QString::fromUtf8("Обрезка видео...");
            if (source == QStringLiteral("Video trim completed")) return QString::fromUtf8("Обрезка видео завершена");
            if (source == QStringLiteral("Video trim failed")) return QString::fromUtf8("Не удалось обрезать видео");

            if (source == QStringLiteral("Audio Device")) return QString::fromUtf8("Аудиоустройство");
            if (source == QStringLiteral("&Decrease Volume") || source == QStringLiteral("Decrease Volume")) return QString::fromUtf8("Уменьшить громкость");
            if (source == QStringLiteral("&Increase Volume") || source == QStringLiteral("Increase Volume")) return QString::fromUtf8("Увеличить громкость");

            if (source == QStringLiteral("Save Play Queue to &File...") || source == QStringLiteral("Save Play Queue to File...")) return QString::fromUtf8("Сохранить очередь воспроизведения в файл...");
            if (source == QStringLiteral("Quit at the end of play queue")) return QString::fromUtf8("Выйти после окончания очереди воспроизведения");
            if (source == QStringLiteral("Play &Queue") || source == QStringLiteral("Play Queue")) return QString::fromUtf8("Очередь воспроизведения");
            if (source == QStringLiteral("Docked Play Queue")) return QString::fromUtf8("Закреплённая очередь воспроизведения");
            if (source == QStringLiteral("Always on &top") || source == QStringLiteral("Always on top")) return QString::fromUtf8("Поверх всех окон");
            if (source == QStringLiteral("&Big Player View") || source == QStringLiteral("Big Player View")) return QString::fromUtf8("Большой режим плеера");
            if (source == QStringLiteral("&Minimal View") || source == QStringLiteral("Minimal View")) return QString::fromUtf8("Минимальный вид");
            if (source == QStringLiteral("&View Items as Grid") || source == QStringLiteral("View Items as Grid")) return QString::fromUtf8("Показывать элементы сеткой");
            if (source == QStringLiteral("&Color Scheme") || source == QStringLiteral("Color Scheme")) return QString::fromUtf8("Цветовая схема");

            if (source == QStringLiteral("Open File")) return QString::fromUtf8("Открыть файл");
            if (source == QStringLiteral("Configure...")) return QString::fromUtf8("Настроить...");
        }

        return translated;
'''

if old not in text:
    raise RuntimeError("Translator return anchor not found in qt.cpp")

text = text.replace(old, new, 1)
qt_cpp.write_text(text, encoding="utf-8")

# Service discovery names arrive from plugin metadata as dynamic strings and
# therefore bypass qsTr(). Route the known built-in names through qsTr() so
# the Russian runtime fallback above can translate them too.
services_qml = root / "modules/gui/qt/network/qml/ServicesSources.qml"
services_text = services_qml.read_text(encoding="utf-8")
services_old = '            title: is_dummy ? qsTr("Add a service") : model.long_name\n'
services_new = '''            title: {\n                if (is_dummy) return qsTr("Add a service")\n                if (model.long_name === "Radio Browser") return qsTr("Radio Browser")\n                if (model.long_name === "Podcasts") return qsTr("Podcasts")\n                if (model.long_name === "Jamendo Selections") return qsTr("Jamendo Selections")\n                return model.long_name\n            }\n'''
if services_old not in services_text:
    raise RuntimeError("ServicesSources title anchor not found")
services_text = services_text.replace(services_old, services_new, 1)
services_qml.write_text(services_text, encoding="utf-8")

print("Zenfix Russian runtime fallback applied")
