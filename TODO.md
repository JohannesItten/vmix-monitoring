# ЗАМЕТКА ДЛЯ РАБОТЫ

## TODO

1) Простые коллбэки: isOnAir(zastkey), lowBusLevel(duration, minLevel), checkInputMapping(bus_map), cutDelta(maxVal)
2) Exclude/include залов в конфиг
3) Второй сервак, который получает данные с компов, находящихся, не в одной сети
4) Несколько вариантов парсера
5) Устаканенное формирование сетки для фронтентда (1,4,9 и тд, pageMax)
6) Градусник??
7) Скрипт для отправки сообщений на сервак с тачек, где нет ремоута
8) Среднее время парса передавать в фронт!!!
9) Обработка ошибок (пинг, не пинг, закрыты и тд)
10) Вменяемый мануал и комментарии к коду
11) Переработать конфиг
12) Залить на гитхаб и раскидать
13) LXML??? для прямого создания правил
14) Скрипт запуска в 1 команду
15) Логирование с уровнями. От полной вербозности, до абсолютной тишины

16) Возможность посылать команды: fix/stopstream и тд

## VMIX RULES SIMPLIFIED DESC

RULE0
{
    ["keys"]:
        "online": ["zastkey", "shapkakey"]
        "towatch": ["testkey", "titlekey"]
    ["online"]
        ["isStreaming", "[params]", ERROR]
        ["isRecording", "[params]", ERROR]
        ["inputBusMapping", ["inputkey", "MABC"], WARNING]
        ["!isInputMuted", ["inputkey"], ERROR]
        ["isInputMuted", ["musickey"], ERROR]
    ["offline"]
        ["isInputMuted", ["inputkey"], ERROR]
        ["!isInputMuted", ["musickey"], WARN]
    ["always"]
        ["checkPreset", "", INFO]
}

RULEN
{
    ...
}

Custom Sort 1	This command will sort a given YAML with custom order. If some of the keys of customSortKeywords_1 will be found at the top level of the YAML, these will be put at the beginning of the YAML file (in the given order). You can use this e. g. to sort Kubernetes configmaps.
Custom Sort 2	Same as Custom Sort 1
Custom Sort 3	Same as Custom Sort 1
Format Document	Formats a yaml document without sorting it. Also possible using the shortcut (⇧⌥F on Mac).
Recursively sort YAML files	Sorts all .yaml and .yml files in a directory and all its subdirectories.
Sort YAML	Sorts a given YAML. You can either sort the whole YAML document or sort only a selection of the text.
Validate YAML	Validates a given YAML.