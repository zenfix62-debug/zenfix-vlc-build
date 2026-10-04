#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: apply_zenfix_extras.py /path/to/vlc")

root = Path(sys.argv[1]).resolve()


def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"patch anchor not found in {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def po_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def set_po_translation(path: Path, msgid: str, msgstr: str):
    text = path.read_text(encoding="utf-8")
    blocks = text.split("\n\n")
    needle = f'msgid "{po_escape(msgid)}"'
    found = False

    for i, block in enumerate(blocks):
        lines = block.splitlines()
        if needle not in lines:
            continue

        found = True

        # A fuzzy translation is ignored by gettext. Remove only the fuzzy flag,
        # preserving any other flags on the same entry.
        cleaned = []
        for line in lines:
            if line.startswith("#,"):
                flags = [f.strip() for f in line[2:].split(",") if f.strip() and f.strip() != "fuzzy"]
                if flags:
                    cleaned.append("#, " + ", ".join(flags))
            else:
                cleaned.append(line)
        lines = cleaned

        msgstr_index = next((j for j, line in enumerate(lines) if line.startswith("msgstr ")), None)
        if msgstr_index is None:
            raise RuntimeError(f"msgstr missing for {msgid!r} in {path}")

        end = msgstr_index + 1
        while end < len(lines) and lines[end].startswith('"'):
            end += 1

        lines[msgstr_index:end] = [f'msgstr "{po_escape(msgstr)}"']
        blocks[i] = "\n".join(lines)
        break

    if not found:
        blocks.append(f'# Zenfix translation override\nmsgid "{po_escape(msgid)}"\nmsgstr "{po_escape(msgstr)}"')

    path.write_text("\n\n".join(blocks).rstrip() + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Russian localization fixes
# VLC 4 development snapshots contain several new Qt/QML strings for which
# ru.po is still incomplete. The QML translator delegates qsTr() to gettext,
# so filling these entries fixes both C++ and QML labels.
# ---------------------------------------------------------------------------
ru_po = root / "po/ru.po"
ru_overrides = {
    "Home": "Главная",
    "Video": "Видео",
    "Videos": "Видео",
    "All": "Все",
    "Playlists": "Плейлисты",
    "Music": "Музыка",
    "Artists": "Исполнители",
    "Albums": "Альбомы",
    "Tracks": "Треки",
    "Genres": "Жанры",
    "Browse": "Обзор",
    "Discover": "Обнаружение",
    "Services": "Сервисы",
    "Settings": "Настройки",
    "No video found": "Видео не найдено",
    "Please try adding sources": "Добавьте источники видео",
    "Audio Track": "Аудиодорожка",
    "Select": "Выбрать",
    "Subtitles": "Субтитры",
    "Playback Speed": "Скорость воспроизведения",
    "Chapters": "Главы",
    "Playback menu": "Меню воспроизведения",
    "Trim Video...": "Обрезать видео...",
    "Trim Video": "Обрезать видео",
    "Source file": "Исходный файл",
    "Output file": "Выходной файл",
    "Start time": "Начало",
    "End time": "Конец",
    "Browse...": "Обзор...",
    "Trim": "Обрезать",
    "Select source video": "Выберите исходное видео",
    "Save trimmed video": "Сохранить обрезанное видео",
    "Video files (*.mp4 *.mkv *.webm *.avi *.ts *.m2ts *.mpg *.mpeg *.flv *.ogg *.ogv)": "Видеофайлы (*.mp4 *.mkv *.webm *.avi *.ts *.m2ts *.mpg *.mpeg *.flv *.ogg *.ogv)",
    "Choose a source video file.": "Выберите исходный видеофайл.",
    "Choose an output file.": "Выберите выходной файл.",
    "Start time must be before end time.": "Время начала должно быть раньше времени окончания.",
    "Unsupported output format. Use MP4, MKV, WebM, AVI, TS, MPEG, FLV or OGG.": "Неподдерживаемый формат. Используйте MP4, MKV, WebM, AVI, TS, MPEG, FLV или OGG.",
    "Trimming video...": "Обрезка видео...",
    "Video trim completed": "Обрезка видео завершена",
    "Video saved to:\n%1": "Видео сохранено в:\n%1",
    "Video trim failed": "Не удалось обрезать видео",
    "Could not start the VLC trim process.": "Не удалось запустить процесс обрезки VLC.",
    "The trim process failed.\n\n%1": "Процесс обрезки завершился с ошибкой.\n\n%1",
}

for source, translated in ru_overrides.items():
    set_po_translation(ru_po, source, translated)


# ---------------------------------------------------------------------------
# Native Tools -> Trim Video...
# This deliberately uses the bundled VLC executable as the remux engine, so
# Zenfix does not depend on PowerShell, Python, FFmpeg.exe or an external app.
# The cut is stream-copy/remux based: fast and lossless, with keyframe-level
# precision for codecs that cannot start on arbitrary frames without re-encode.
# ---------------------------------------------------------------------------
provider_hpp = root / "modules/gui/qt/dialogs/dialogs_provider.hpp"
replace_once(
    provider_hpp,
    "    void synchroDialog();\n",
    "    void synchroDialog();\n    void trimVideoDialog();\n",
)

provider_cpp = root / "modules/gui/qt/dialogs/dialogs_provider.cpp"
replace_once(
    provider_cpp,
    "#include <QMessageBox>\n",
    "#include <QMessageBox>\n"
    "#include <QDialog>\n"
    "#include <QDialogButtonBox>\n"
    "#include <QFormLayout>\n"
    "#include <QHBoxLayout>\n"
    "#include <QVBoxLayout>\n"
    "#include <QLineEdit>\n"
    "#include <QPushButton>\n"
    "#include <QTimeEdit>\n"
    "#include <QProcess>\n"
    "#include <QProgressDialog>\n"
    "#include <QFileInfo>\n"
    "#include <QDir>\n"
    "#include <QCoreApplication>\n",
)

trim_method = r'''void DialogsProvider::trimVideoDialog()
{
    QWidget *parent = QApplication::activeWindow();

    QDialog dialog(parent);
    dialog.setWindowTitle(qtr("Trim Video"));
    dialog.setModal(true);
    dialog.setMinimumWidth(620);

    auto *mainLayout = new QVBoxLayout(&dialog);
    auto *formLayout = new QFormLayout();
    mainLayout->addLayout(formLayout);

    auto makeFileRow = [&dialog](QLineEdit **editOut, QPushButton **buttonOut) {
        auto *row = new QWidget(&dialog);
        auto *layout = new QHBoxLayout(row);
        layout->setContentsMargins(0, 0, 0, 0);
        layout->setSpacing(8);

        auto *edit = new QLineEdit(row);
        auto *button = new QPushButton(qtr("Browse..."), row);
        layout->addWidget(edit, 1);
        layout->addWidget(button);

        *editOut = edit;
        *buttonOut = button;
        return row;
    };

    QLineEdit *sourceEdit = nullptr;
    QPushButton *sourceBrowse = nullptr;
    QWidget *sourceRow = makeFileRow(&sourceEdit, &sourceBrowse);
    formLayout->addRow(qtr("Source file"), sourceRow);

    QLineEdit *outputEdit = nullptr;
    QPushButton *outputBrowse = nullptr;
    QWidget *outputRow = makeFileRow(&outputEdit, &outputBrowse);
    formLayout->addRow(qtr("Output file"), outputRow);

    auto *startEdit = new QTimeEdit(QTime(0, 0, 0, 0), &dialog);
    auto *endEdit = new QTimeEdit(QTime(0, 0, 10, 0), &dialog);
    startEdit->setDisplayFormat(QStringLiteral("HH:mm:ss.zzz"));
    endEdit->setDisplayFormat(QStringLiteral("HH:mm:ss.zzz"));
    formLayout->addRow(qtr("Start time"), startEdit);
    formLayout->addRow(qtr("End time"), endEdit);

    const QString videoFilter = qtr("Video files (*.mp4 *.mkv *.webm *.avi *.ts *.m2ts *.mpg *.mpeg *.flv *.ogg *.ogv)");

    QObject::connect(sourceBrowse, &QPushButton::clicked, &dialog, [&dialog, sourceEdit, outputEdit, videoFilter]() {
        const QString source = QFileDialog::getOpenFileName(&dialog, qtr("Select source video"), QString(), videoFilter);
        if (source.isEmpty())
            return;

        sourceEdit->setText(source);

        if (outputEdit->text().isEmpty())
        {
            const QFileInfo info(source);
            QString suffix = info.suffix();
            if (suffix.isEmpty())
                suffix = QStringLiteral("mkv");

            outputEdit->setText(info.dir().filePath(info.completeBaseName()
                                                    + QStringLiteral("_trimmed.")
                                                    + suffix));
        }
    });

    QObject::connect(outputBrowse, &QPushButton::clicked, &dialog, [&dialog, sourceEdit, outputEdit, videoFilter]() {
        QString initial = outputEdit->text();
        if (initial.isEmpty() && !sourceEdit->text().isEmpty())
        {
            const QFileInfo info(sourceEdit->text());
            QString suffix = info.suffix();
            if (suffix.isEmpty())
                suffix = QStringLiteral("mkv");
            initial = info.dir().filePath(info.completeBaseName() + QStringLiteral("_trimmed.") + suffix);
        }

        const QString output = QFileDialog::getSaveFileName(&dialog, qtr("Save trimmed video"), initial, videoFilter);
        if (!output.isEmpty())
            outputEdit->setText(output);
    });

    auto *buttons = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel, &dialog);
    if (QPushButton *ok = buttons->button(QDialogButtonBox::Ok))
        ok->setText(qtr("Trim"));
    mainLayout->addWidget(buttons);

    QObject::connect(buttons, &QDialogButtonBox::accepted, &dialog, &QDialog::accept);
    QObject::connect(buttons, &QDialogButtonBox::rejected, &dialog, &QDialog::reject);

    if (dialog.exec() != QDialog::Accepted)
        return;

    const QString source = sourceEdit->text().trimmed();
    const QString output = outputEdit->text().trimmed();

    if (source.isEmpty() || !QFileInfo::exists(source))
    {
        QMessageBox::warning(parent, qtr("Trim Video"), qtr("Choose a source video file."));
        return;
    }
    if (output.isEmpty())
    {
        QMessageBox::warning(parent, qtr("Trim Video"), qtr("Choose an output file."));
        return;
    }

    auto toSeconds = [](const QTime &time) {
        return time.hour() * 3600.0
             + time.minute() * 60.0
             + time.second()
             + time.msec() / 1000.0;
    };

    const double startSeconds = toSeconds(startEdit->time());
    const double endSeconds = toSeconds(endEdit->time());
    if (endSeconds <= startSeconds)
    {
        QMessageBox::warning(parent, qtr("Trim Video"), qtr("Start time must be before end time."));
        return;
    }

    const QString extension = QFileInfo(output).suffix().toLower();
    QString mux;
    if (extension == QStringLiteral("mp4") || extension == QStringLiteral("m4v") || extension == QStringLiteral("mov"))
        mux = QStringLiteral("mp4");
    else if (extension == QStringLiteral("mkv"))
        mux = QStringLiteral("avformat{mux=matroska}");
    else if (extension == QStringLiteral("webm"))
        mux = QStringLiteral("avformat{mux=webm}");
    else if (extension == QStringLiteral("avi"))
        mux = QStringLiteral("avi");
    else if (extension == QStringLiteral("ts") || extension == QStringLiteral("m2ts"))
        mux = QStringLiteral("ts");
    else if (extension == QStringLiteral("mpg") || extension == QStringLiteral("mpeg"))
        mux = QStringLiteral("ps");
    else if (extension == QStringLiteral("flv"))
        mux = QStringLiteral("avformat{mux=flv}");
    else if (extension == QStringLiteral("ogg") || extension == QStringLiteral("ogv"))
        mux = QStringLiteral("ogg");
    else
    {
        QMessageBox::warning(parent, qtr("Trim Video"),
                             qtr("Unsupported output format. Use MP4, MKV, WebM, AVI, TS, MPEG, FLV or OGG."));
        return;
    }

    QString safeOutput = QDir::fromNativeSeparators(output);
    safeOutput.replace(QLatin1Char('\''), QStringLiteral("\\'"));

    const QString sout = QStringLiteral("#std{access=file{no-append,no-format,no-overwrite},mux=%1,dst='%2'}")
                             .arg(mux, safeOutput);

    const QString executable = QCoreApplication::applicationFilePath();
    QStringList arguments;
    arguments << QStringLiteral("--no-one-instance")
              << QStringLiteral("--intf=dummy")
              << QStringLiteral("--dummy-quiet")
              << QStringLiteral("--no-video-title-show")
              << QStringLiteral("--start-time=%1").arg(startSeconds, 0, 'f', 3)
              << QStringLiteral("--stop-time=%1").arg(endSeconds, 0, 'f', 3)
              << source
              << (QStringLiteral("--sout=") + sout)
              << QStringLiteral("vlc://quit");

    auto *process = new QProcess(qApp);
    auto *progress = new QProgressDialog(qtr("Trimming video..."), qtr("Cancel"), 0, 0, parent);
    progress->setWindowTitle(qtr("Trim Video"));
    progress->setWindowModality(Qt::WindowModal);
    progress->setMinimumDuration(0);
    progress->setAutoClose(false);
    progress->setAutoReset(false);

    QObject::connect(progress, &QProgressDialog::canceled, process, [process]() {
        process->setProperty("zenfixCanceled", true);
        process->kill();
    });

    QObject::connect(process, qOverload<int, QProcess::ExitStatus>(&QProcess::finished),
                     qApp, [process, progress, parent, output](int exitCode, QProcess::ExitStatus exitStatus) {
        const bool canceled = process->property("zenfixCanceled").toBool();
        const QString diagnostics = QString::fromLocal8Bit(process->readAllStandardError()).right(2500);

        progress->close();
        progress->deleteLater();

        if (!canceled)
        {
            const QFileInfo result(output);
            if (exitStatus == QProcess::NormalExit && exitCode == 0 && result.exists() && result.size() > 0)
            {
                QMessageBox::information(parent, qtr("Video trim completed"),
                                         qtr("Video saved to:\n%1").arg(QDir::toNativeSeparators(output)));
            }
            else
            {
                QMessageBox::warning(parent, qtr("Video trim failed"),
                                     qtr("The trim process failed.\n\n%1").arg(diagnostics));
            }
        }

        process->deleteLater();
    });

    process->start(executable, arguments);
    if (!process->waitForStarted(3000))
    {
        progress->close();
        progress->deleteLater();
        QMessageBox::warning(parent, qtr("Video trim failed"), qtr("Could not start the VLC trim process."));
        process->deleteLater();
        return;
    }

    progress->show();
}

'''

replace_once(
    provider_cpp,
    "void DialogsProvider::synchroDialog()\n{\n",
    trim_method + "void DialogsProvider::synchroDialog()\n{\n",
)

menus_cpp = root / "modules/gui/qt/menus/menus.cpp"
replace_once(
    menus_cpp,
    "void VLCMenuBar::ToolsMenu( qt_intf_t *p_intf, QMenu *menu )\n{\n"
    "    addDPStaticEntry( menu, qtr( \"&Effects and Filters\"),",
    "void VLCMenuBar::ToolsMenu( qt_intf_t *p_intf, QMenu *menu )\n{\n"
    "    addDPStaticEntry( menu, qtr( \"Trim Video...\"), \"\",\n"
    "            &DialogsProvider::trimVideoDialog );\n"
    "    menu->addSeparator();\n\n"
    "    addDPStaticEntry( menu, qtr( \"&Effects and Filters\"),",
)

print("Zenfix extras applied: Russian localization overrides + Tools/Trim Video")
