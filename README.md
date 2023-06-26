# SSH-log-processing

Program z interfejsem graficznym (z użyciem biblioteki PySide6 ) do przeglądania logów serwera
lub SSH. 
Aby uruchowić program należy użyć polecenia `python main.py`
Program posiada następujące funkcjonalności:
- wczytywanie pliku z logami z pliku
- wyświetlanie wierszy zapisanych w pliku w formie listy
- wyświetlanie szczegółów dotyczących konkretnego loga
- filtrowanie listy logów ze względu na wybrany przedział czasowy
  
 Program jest wyposażony w przyciski “Następny” i “Poprzedni” pozwalające
przeglądać kolejne logi.  W przypadkupierwszego/ostatniego loga, przyciski są nieaktywne.
