<p>
    <strong>Task:</strong><br>
    Написать скрипт, который проверяет все страницы сайта на отсутствие pdf файлов больше 15 Мб.<br>
    <strong>Decision:</strong><br>
    Можно выполнить командой:<br>
    wget --no-check-certificate -r -l 1 -A pdf https://tdomain.ru/sveden/document<br>
    А можно выполнить скриптом:<br>
    chmod +x FileWeight.sh<br>
    ./FileWeight.sh<br>
    Enter a link to the site: https://tdomain.ru/sveden/document<br>
    Come up with a name for the directory where the files will be written: tdir<br>
    /home/tuser/tdir create<br>
    ...<br>
    cat /home/tuser/tdir/output<br>
    /home/tuser/tdir/tdomain.ru/Media/irk/Документы института/2018/tDoc1.pdf<br>
    ls -l /home/tuser/tdir/tdomain.ru/Media/irk/Документы\ института/2018/tDoc1.pdf<br>
    -rw-r--r--. 1 tuser tuser 20055320 июн 30 2018 '/home/tuser/tdir/tdomain.ru/Media/irk/Документы института/2018/tDoc1.pdf'
</p>
<p>
    <strong>Task:</strong><br>
    На странице https://tdomain.ru/sveden/education под поле "Образовательная программа, направленность, профиль, шифр и наименование научной специальности" в таблице "Образование" (информация по образовательным программам) необходимо добавить тег itemprop="eduProf". В данной таблице тег &lt;tr itemprop="eduOp"&gt;, который нужно заменить на &lt;tr itemprop="eduOprog"&gt;.<br>
    <strong>Decision:</strong><br>
    Алгоритм:<br>
    1. Программа будет запрашивать страницу для парсинга.<br>
    2. Парсинг страницы сайта по тегам<br>
    3. Поиск тега который нужно заменить<br>
    4. замена тега<br>
    5. Публикация изменения на сайт<br>
    ЗДЕСЬ БУДЕТ КОД
</p>